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
        'aakash.ar07@gmail.com',
        [order.user.email]
    )

    return "Email Sent"





@shared_task
def send_payment_success_email(order_id):
    try:
        order = Order.objects.get(id=order_id)

        subject = "Payment Successful 🎉"
        message = f"""
Hi {order.user.username},

Your payment for Order #{order.id} is successful.

Amount Paid: ₹{order.total_amount}

Thank you for ordering with us ❤️
"""

        send_mail(
            subject,
            message,
            'your_email@gmail.com',   # sender
            [order.user.email],       # receiver
            fail_silently=False
        )

        return "Email Sent Successfully"

    except Exception as e:
        return str(e)