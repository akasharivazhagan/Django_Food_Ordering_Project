import razorpay

client = razorpay.Client(auth=("KEY","SECRET"))

payment = client.order.create({
    "amount": 50000,
    "currency": "INR",
    "payment_capture": 1
})