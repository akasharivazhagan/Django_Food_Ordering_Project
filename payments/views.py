from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Order, Payment
from orders.tasks import process_payment


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            order_id = request.data.get('order_id')

            order = Order.objects.get(id=order_id, user=request.user)

            # ✅ Create Payment
            Payment.objects.create(
                order=order,
                amount=order.total_price,
                status='SUCCESS'
            )

            # ✅ Change status to CONFIRMED (NOT COMPLETED)
            order.status = 'CONFIRMED'
            order.save()

            #send_payment_email.delay(order.user.email, order.id)

            # ✅ Trigger Celery
            process_payment.delay(order.id)

            return Response({
                'message': 'Payment Success',
                'order_id': order.id,
                'status': order.status
            })

        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)

        except Exception as e:
            return Response({'error': str(e)}, status=400)