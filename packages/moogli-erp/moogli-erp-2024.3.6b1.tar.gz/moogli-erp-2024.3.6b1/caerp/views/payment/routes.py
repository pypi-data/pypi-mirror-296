from caerp.views import caerp_add_route


INVOICE_PAYMENT_ADD = "/invoices/{id}/addpayment"
EXPENSE_PAYMENT_ADD = "/expenses/{id}/addpayment"
SUPPLIER_INVOICE_PAYMENT_ADD = "/supplier_invoices/{id}/add_supplier_payment"
SUPPLIER_INVOICE_USER_PAYMENT_ADD = "/supplier_invoices/{id}/add_user_payment"


def includeme(config):
    """
    Add module's related routes
    """
    # Invoice payments
    caerp_add_route(
        config,
        INVOICE_PAYMENT_ADD,
        traverse="/tasks/{id}",
    )
    config.add_route(
        "payment",
        r"/payments/{id:\d+}",
        traverse="/base_task_payments/{id}",
    )

    # Expense payments
    caerp_add_route(
        config,
        EXPENSE_PAYMENT_ADD,
        traverse="/expenses/{id}",
    )
    config.add_route(
        "expense_payment",
        r"/expense_payments/{id:\d+}",
        traverse="/expense_payments/{id}",
    )

    # Supplier invoice payments
    config.add_route(
        "supplier_payment",
        r"/supplier_payments/{id:\d+}",
        traverse="/supplier_payments/{id}",
    )
    caerp_add_route(
        config, SUPPLIER_INVOICE_PAYMENT_ADD, traverse="/supplier_invoices/{id}"
    )
    caerp_add_route(
        config, SUPPLIER_INVOICE_USER_PAYMENT_ADD, traverse="/supplier_invoices/{id}"
    )
