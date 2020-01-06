from django.forms import widgets


class UploadFile(widgets.FileInput):

    template_name = 'boss/widgets/upload.html'
