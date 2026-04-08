from celery import shared_task
from .models import Order
from payments.models import Payment

# 👉 Order processing task
@shared_task
def process_order(order_id):
    print(f"🔥 Order Processing Started: {order_id}")

    order = Order.objects.get(id=order_id)

    # Only update if still processing
    if order.status == 'PROCESSING':
        order.status = 'PROCESSING'
        order.save()

    print(f"✅ Order {order_id} moved to PROCESSING")


# 👉 Payment processing task
@shared_task
def process_payment(order_id):
    print(f"💰 Payment Processing Started: {order_id}")

    order = Order.objects.get(id=order_id)

    # Final status update
    if order.status == 'CONFIRMED':
        order.status = 'COMPLETED'
        order.save()
        
    print(f"✅ Order {order_id} is COMPLETED")