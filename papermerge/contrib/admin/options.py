

class SidebarPart:
    """
    Wrapper class for managing/rendering document parts
    on sidebar.
    """

    fields = None
    exclude = None
    readonly_fields = ()
    model = None

    def __init__(self, document):
        # papermerge.core.models.document instance
        self.document = document

        if not self.model:
            raise ValueError("SidebarPart: missing model attribute")
        self.opts = self.model._meta

    def to_json(self):
        fields = []
        ret = {
            'label': self.get_label(),
            'verbose_name': self.get_verbose_name(),
            'fields': fields
        }
        return ret

    def get_label(self):
        if hasattr(self, 'label'):
            return getattr(self, 'label')

        return self.opts.app_config.label

    def get_verbose_name(self):
        if hasattr(self, 'verbose_name'):
            return getattr(self, 'verbose_name')

        return self.opts.app_config.verbose_name

