# store/utils/email_utils.py

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_order_confirmation_email(order, user_email):
    items = order.orderitem_set.all()
    context = {
        'order': order,
        'items': items
    }
    message = render_to_string('emails/order_confirmation.html', context)

    email = EmailMessage(
        subject='Order Confirmation',
        body=message,
        from_email='rahiepatel03@example.com',
        to=[user_email]
    )
    email.content_subtype = "html"
    email.send(fail_silently=False)