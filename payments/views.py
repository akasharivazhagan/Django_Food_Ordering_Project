from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Payment
from orders.models import Order

class PaymentView(APIView):
    def post(self, request):

        order = Order.objects.get(id=request.data['order_id'])

        # Payment create
        Payment.objects.create(order=order,amount=order.total_price,status='Success')

        order.status = 'COMPLETED'
        order.save()

        return Response({'msg': 'Payment Success'})