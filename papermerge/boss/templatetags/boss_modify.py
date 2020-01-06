from django import template
from django.contrib.admin.templatetags import admin_modify


register = template.Library()


@register.inclusion_tag('boss/task/submit_line.html', takes_context=True)
def task_submit_row(context):
    return admin_modify.submit_row(context)


@register.inclusion_tag(
    'boss/document/submit_line.html',
    takes_context=True
)
def document_submit_row(context):
    return admin_modify.submit_row(context)


@register.inclusion_tag(
    'boss/dynamic_preferences_users/submit_line.html',
    takes_context=True
)
def preference_submit_row(context):
    return admin_modify.submit_row(context)

