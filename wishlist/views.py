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
from django.views.generic import CreateView
from django.urls import reverse_lazy

@login_required
def my_wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    items = WishlistItem.objects.filter(wishlist=wishlist).order_by('priority')
    return render(request, 'wishlist/wishlist_detail.html', {
        'wishlist': wishlist,
        'items': items,
    })

def public_wishlist(request, username):
    user = get_object_or_404(User, username=username)
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    items = WishlistItem.objects.filter(wishlist=wishlist).order_by('priority')
    return render(request, 'wishlist/wishlist_public.html', {
        'wishlist': wishlist,
        'items': items,
    })

class ItemCreateView(CreateView):
    model = WishlistItem
    fields = ['name', 'description', 'links', 'priority', 'image']
    template_name = 'wishlist/item_form.html'
    success_url = reverse_lazy('my_wishlist')

    def form_valid(self, form):
        wishlist, _ = Wishlist.objects.get_or_create(user=self.request.user)
        form.instance.wishlist = wishlist
        return super().form_valid(form)


class ItemUpdateView(UpdateView):
    model = WishlistItem
    fields = ['name', 'description', 'links', 'priority', 'image']
    template_name = 'wishlist/item_form.html'
    success_url = reverse_lazy('my_wishlist')


class ItemDeleteView(DeleteView):
    model = WishlistItem
    success_url = reverse_lazy('my_wishlist')

    # skip confirmation page
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy('login')

@login_required
def mark_purchased_view(request, username, pk):
    item = get_object_or_404(WishlistItem, pk=pk)
    if item.purchased_by is None:
        item.purchased_by = request.user
        item.save()
    return redirect('user_wishlist', username=item.user.username)

@login_required
def select_user_view(request):
    # Exclude the current user from the list
    users = User.objects.exclude(id=request.user.id)
    return render(request, "wishlist/users.html", {"users": users})

@login_required
def user_wishlist_view(request, username):
    other_user = get_object_or_404(User, username=username)
    # Get all WishlistItems for all Wishlists belonging to this user
    items = WishlistItem.objects.filter(wishlist__user=other_user).select_related('purchased_by', 'wishlist')

    return render(request, "wishlist/user_wishlist.html", {
        "wishlist_user": other_user,
        "items": items
    })


