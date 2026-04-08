import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from orders.models import Order
from .models import Payment
from orders.tasks import send_order_email

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# 💳 Create Razorpay Order
class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = Order.objects.get(id=order_id, user=request.user)

        amount = int(order.total_amount * 100)  # paise

        razorpay_order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        payment = Payment.objects.create(
            order=order,
            razorpay_order_id=razorpay_order['id'],
            status='created'
        )

        return Response({
            "razorpay_order_id": razorpay_order['id'],
            "amount": amount,
            "key": settings.RAZORPAY_KEY_ID
        })


# ✅ Verify Payment
class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })

            payment = Payment.objects.get(
                razorpay_order_id=data['razorpay_order_id']
            )

            payment.razorpay_payment_id = data['razorpay_payment_id']
            payment.razorpay_signature = data['razorpay_signature']
            payment.status = 'success'
            payment.save()

            # ✅ update order
            order = payment.order
            order.status = 'completed'
            order.save()
            
            send_order_email.delay(order.id)

            return Response({"message": "Payment Successful"})

        except:
            return Response({"error": "Payment Failed"})