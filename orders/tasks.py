from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def send_order_email(order_id):
    order = Order.objects.get(id=order_id)

    subject = "Order Confirmation"
    message = f"Your order #{order.id} is placed successfully. Total: {order.total_amount}"

    send_mail(
        subject,
        message,
        'your_email@gmail.com',
        [order.user.email]
    )

    return "Email Sent"