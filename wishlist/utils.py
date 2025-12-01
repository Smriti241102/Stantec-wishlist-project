# wishlist/utils.py (or wherever you prefer)
from django.core.mail import send_mail
from django.conf import settings

def send_purchase_notification(item, buyer):
    """
    Notify the wishlist owner that someone purchased their item
    """
    subject = f"Your wishlist item '{item.name}' was purchased!"
    message = f"Hi {item.wishlist.user.first_name},\n\n" \
              f"{buyer.first_name} {buyer.last_name} has purchased '{item.name}' from your wishlist.\n\n" \
              f"Description: {item.description}\n\n" \
              f"Thank you for using Wishlist App!"
    recipient_list = [item.wishlist.user.email]

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'no-reply@example.com',
        recipient_list,
        fail_silently=False
    )
