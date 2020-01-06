from django.contrib.admin.widgets import FilteredSelectMultiple


class PermissionsSelectMultiple(FilteredSelectMultiple):

    def create_option(
        self,
        name,
        value,
        label,
        selected,
        index,
        subindex=None,
        attrs=None
    ):
        """
        Replaces Django standard permissions names <app>.<model>.<codename>
        with custom ones.

        Without this change, permissions will be displayed to the user in
        standard django way. Its ugly and not user friendly. In this method
        we just change the label of the permission (i.e. the way users)
        sees it - all other functionality stays same.

        Custome permissions i.e. ones created for vml application, have
        codename prefixed with vml_ and are associated with dummy model
        content type of core.models.Subscription
        """
        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        if attrs is None:
            attrs = {}
        option_attrs = self.build_attrs(
            self.attrs, attrs
        ) if self.option_inherits_attrs else {}
        if selected:
            option_attrs.update(self.checked_attribute)
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'], index)

        # here is the business
        label = label.replace("core | subscription |", "")
        return {
            'name': name,
            'value': value,
            'label': label,
            'selected': selected,
            'index': index,
            'attrs': option_attrs,
            'type': self.input_type,
            'template_name': self.option_template_name,
        }
