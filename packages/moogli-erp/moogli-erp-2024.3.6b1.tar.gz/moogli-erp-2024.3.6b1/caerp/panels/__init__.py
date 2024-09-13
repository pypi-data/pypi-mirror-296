class BasePanel:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()
