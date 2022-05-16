from email import message
from io import BytesIO
from celery.decorators import task
import weasyprint

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

@task
def payment_completed(order_id):
    """Task to send mail when the successfully created.

    Args:
        order_id (id): order_id of payment
    """
    order = Order.objects.get(id=order_id)
    # subject invoice mail
    subject = f'My shop - EE Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your purchase.'
    email = EmailMessage(
        subject,
        message,
        'admin@myshop.com',
        [order.email]
    )
    # pdf invoice
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # attach pdf file
    email.attach(f'order_{order.id}.pdf',
        out.getvalue(),
        'application/pdf'
    )
    email.send()