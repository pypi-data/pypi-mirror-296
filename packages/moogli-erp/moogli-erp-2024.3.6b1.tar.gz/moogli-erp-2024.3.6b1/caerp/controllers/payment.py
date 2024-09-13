import logging
from typing import Union

from caerp.models.task import Invoice, BaseTaskPayment
from caerp.models.expense import ExpenseSheet, ExpensePayment
from caerp.models.supply import SupplierInvoice, BaseSupplierInvoicePayment

logger = logging.getLogger(__name__)


def record_payment(
    request,
    node: Union[Invoice, ExpenseSheet, SupplierInvoice],
    payment: Union[BaseTaskPayment, ExpensePayment, BaseSupplierInvoicePayment],
):
    """
    Record a payment for the given node
    """
    logger.debug(f"Recording a payment of {payment.amount} for {node.type_} {node.id}")
    node.payments.append(payment)
    return node
