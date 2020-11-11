
class SidebarPartField:
    """
    Performs introspection into document part fields.
    """

    def __init__(self, document, model, field_name):
        """
        `document` = papermerge.core.models.document instance
        `model` = document part model class as provided by 3rd party app
        `field_name` name of the field we are interested in
        """

        self.document = document
        self.model = model
        self.field_name = field_name

        fields = [
            field
            for field in self.model._meta.fields
            if field.name == field_name
        ]
        if fields:
            # django field matching given field_name
            self.field = fields[0]

    def to_json(self):
        pass

    def get_internal_type(self):
        return self.field.get_internal_type()

    def get_value(self):
        parts = getattr(self.document, 'parts')
        value = getattr(parts, self.field_name)
        return value


class SidebarPart:
    """
    Wrapper class for managing/rendering document parts
    on sidebar.
    """

    fields = None
    exclude = None
    readonly_fields = ()
    # model class of the document part
    model = None

    def __init__(self, document):
        # papermerge.core.models.document instance
        self.document = document

        if not self.model:
            raise ValueError("SidebarPart: missing model attribute")
        self.opts = self.model._meta

    def to_json(self):
        fields = [
            field.to_json()
            for field in self.fields
        ]
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

