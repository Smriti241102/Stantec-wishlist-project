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
    template_name = 'wishlist/item_confirm_delete.html'
    success_url = reverse_lazy('my_wishlist')

@login_required
def mark_purchased(request, username, pk):
    item = get_object_or_404(WishlistItem, pk=pk)
    item.purchased = True
    item.purchased_by = request.user
    item.purchased_at = timezone.now()
    item.save()
    return redirect('public_wishlist', username=username)

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy('login')
