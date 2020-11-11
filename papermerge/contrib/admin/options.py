
class SidebarPartField:
    """
    Performs introspection into document part fields.
    """

    def __init__(
        self,
        document,
        model,
        field_name,
        options={}
    ):
        """
        `document` = papermerge.core.models.document instance
        `model` = document part model class as provided by 3rd party app
        `field_name` name of the field we are interested in
        """

        self.document = document
        self.model = model
        self.field_name = field_name
        self.options = options

        fields = [
            field
            for field in self.model._meta.fields
            if field.name == field_name
        ]
        if fields:
            # django field matching given field_name
            self.field = fields[0]

    def to_json(self):
        ret = {}

        internal_type = self.get_internal_type()
        ret['class'] = internal_type
        ret['value'] = self.get_value()

        if internal_type == 'ForeignKey':
            ret['choices'] = []
            if self.options and self.options[self.field_name]:
                opts = self.options[self.field_name]
                remote_model_objects = getattr(
                    self.field.remote_field.model, 'objects'
                )
                for r_model_inst in remote_model_objects.all():
                    ret['choices'].append(
                        (
                            getattr(r_model_inst, opts['choice_fields'][0]),
                            getattr(r_model_inst, opts['choice_fields'][1]),
                        )
                    )
            else:
                _f = self.field_name
                msg = f"Field {_f} is foreignkey. You provide field_options"
                raise ValueError(
                    msg
                )

        return ret

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
    field_options = {}

    def __init__(self, document):
        # papermerge.core.models.document instance
        self.document = document

        if not self.model:
            raise ValueError("SidebarPart: missing model attribute")
        self.opts = self.model._meta

    def to_json(self):
        fields = [
            SidebarPartField(
                document=self.document,
                field_name=field,
                model=self.model,
                options=self.field_options
            ).to_json()
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

