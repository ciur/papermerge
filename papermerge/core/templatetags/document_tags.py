from django import template


register = template.Library()


@register.simple_tag
def document_title(document):

    return document.keywords or "Document"


@register.simple_tag
def document_url(document):

    return document.url


@register.simple_tag
def document_keywords(document):
    """
        Returns a comma separated string with document associated
        keywords. E.g. 'tax, docura, blah'
    """

    return ','.join(
        [key.name for key in document.keywords.all()]
    )
