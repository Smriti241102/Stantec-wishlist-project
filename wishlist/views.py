from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Wishlist, WishlistItem

from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm

from django.views.generic import CreateView
from django.urls import reverse_lazy

from .utils import send_purchase_notification

@login_required
def my_wishlist(request):
    """
    Display the logged-in user's wishlist.
    If the wishlist does not exist, create it.
    Supports optional filtering:
        - 'purchased': items purchased by anyone
        - 'unpurchased': items not purchased yet
        - 'all': show All Items
    """
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    items = WishlistItem.objects.filter(wishlist=wishlist).order_by('priority')
    filter_value = request.GET.get("filter", "all")

    if filter_value == "purchased":
        items = items.filter(purchased_by__isnull=False)
    elif filter_value == "unpurchased":
        items = items.filter(purchased_by__isnull=True)

    return render(request, 'wishlist/wishlist_detail.html', {
        'wishlist': wishlist,
        'items': items,
        "filter_value": filter_value,
    })

@login_required
def public_wishlist(request, username):
    """
    View another user's public wishlist.
    """
    user = get_object_or_404(User, username=username)
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    items = WishlistItem.objects.filter(wishlist=wishlist).order_by('priority')
    return render(request, 'wishlist/wishlist_public.html', {
        'wishlist': wishlist,
        'items': items,
    })

class ItemCreateView(CreateView):
    """
    Create a new item in the current user's wishlist.
    Links are handled manually because they are provided
    as dynamic input fields (links[]).
    """
    model = WishlistItem
    fields = ['name', 'description', 'priority', 'image'] 
    template_name = 'wishlist/item_form.html'
    success_url = reverse_lazy('my_wishlist')

    def form_valid(self, form):
        # Assign wishlist
        wishlist, _ = Wishlist.objects.get_or_create(user=self.request.user)
        form.instance.wishlist = wishlist

        response = super().form_valid(form)

        # Handling link fields ("links[]")
        links = self.request.POST.getlist("links[]")
        cleaned_links = [l.strip() for l in links if l.strip()]

        self.object.links = cleaned_links
        self.object.save(update_fields=["links"])

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = None  # Required for template logic
        return context


class ItemUpdateView(UpdateView):
    """
    Update an existing wishlist item.
    Dynamic link fields are handled the same way as in creation.
    """
    model = WishlistItem
    fields = ['name', 'description', 'priority', 'image']
    template_name = 'wishlist/item_form.html'
    success_url = reverse_lazy('my_wishlist')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Handle dynamic links input
        links = self.request.POST.getlist("links[]")
        cleaned_links = [l.strip() for l in links if l.strip()]
        self.object.links = cleaned_links
        self.object.save(update_fields=['links'])

        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['object'] = self.object  # REQUIRED for prefill
        return ctx


class ItemDeleteView(DeleteView):
    """
    Delete an item from the wishlist.
    Automatically redirects back to the wishlist
    and skips the confirmation template.
    """
    model = WishlistItem
    success_url = reverse_lazy('my_wishlist')

    # skip confirmation page
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class SignUpView(CreateView):
    """
    Register a new user
    """
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """
        If the form is valid, save the user and optionally log them in
        """
        response = super().form_valid(form)
        # Optional: log in the user immediately after signup
        # login(self.request, self.object)
        return response


@login_required
def mark_purchased_view(request, username, pk):
    """
    Allow a user to mark someone else's item as purchased.
    Does nothing if already purchased.
    Redirects to the owner's wishlist page afterward.
    """
    item = get_object_or_404(WishlistItem, pk=pk)

    # Only mark if not already purchased
    if item.purchased_by is None:
        item.purchased_by = request.user
        item.save()
    # send email to the person
    send_purchase_notification(item, request.user)

    # Redirect to the wishlist of the item's owner
    return redirect('user_wishlist', username=item.wishlist.user.username)


@login_required
def select_user_view(request):
    # Exclude the current user from the list
    users = User.objects.exclude(id=request.user.id)
    return render(request, "wishlist/users.html", {"users": users})

@login_required
def user_wishlist_view(request, username):
    """
    View someone else's wishlist.
    """
    other_user = get_object_or_404(User, username=username)
    # Get all WishlistItems for all Wishlists belonging to this user
    items = WishlistItem.objects.filter(wishlist__user=other_user).select_related('purchased_by', 'wishlist')

    return render(request, "wishlist/user_wishlist.html", {
        "wishlist_user": other_user,
        "items": items
    })




