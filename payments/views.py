import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from orders.models import Order
from .models import Payment
from orders.tasks import send_payment_success_email

stripe.api_key = settings.STRIPE_SECRET_KEY

# 💳 Create Razorpay Order
class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = Order.objects.get(id=order_id, user=request.user)

        amount = int(order.total_amount * 100)  # paise → cents

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='inr',
            metadata={"order_id": order.id}
        )

        Payment.objects.create(
            order=order,
            stripe_payment_intent=intent['id'],
            amount=order.total_amount,
            status='created'
        )

        return Response({
            "client_secret": intent['client_secret'],
            "payment_intent": intent['id']
        })
    
    
    
# ✅ Verify Payment
# class VerifyPaymentView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         payment_intent_id = request.data.get("payment_intent")

#         try:
#             intent = stripe.PaymentIntent.retrieve(payment_intent_id)

#             if intent.status == "succeeded":
#                 payment = Payment.objects.get(
#                     stripe_payment_intent=payment_intent_id
#                 )

#                 payment.status = "completed"
#                 payment.save()

#                 order = payment.order
#                 order.status = "completed"
#                 order.save()

#                 # 🔥 Celery Email Trigger
#                 send_payment_success_email.delay(order.id)

#                 return Response({"message": "Payment Successful"})

#             return Response({"error": "Payment not completed"}, status=400)

#         except Exception as e:
#             return Response({"error": str(e)}, status=400)
        
        
class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_intent_id = request.data.get("payment_intent")

        # ✅ Check input
        if not payment_intent_id:
            return Response({"error": "payment_intent is required"}, status=400)

        try:
            # ✅ Get payment from DB
            payment = Payment.objects.get(
                stripe_payment_intent=payment_intent_id
            )

            # 🔥 IMPORTANT: For Postman testing (skip Stripe verification)
            payment.status = "completed"
            payment.save()

            # 📦 Update order
            order = payment.order
            order.status = "completed"
            order.save()

            # 📧 Send email using Celery

            send_payment_success_email.delay(order.id)

            return Response({
                "message": "Payment Successful (Test Mode)",
                "order_id": order.id
            })

        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=400)