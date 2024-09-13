def business_type_label(context, request, business_type):
    return dict(business_type=business_type)


def includeme(config):
    config.add_panel(
        business_type_label,
        "business_type_label",
        renderer="caerp:templates/panels/project/business_type_label.mako",
    )
