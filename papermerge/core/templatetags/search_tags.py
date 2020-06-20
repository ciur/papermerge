from django import template
from django.template import TemplateSyntaxError

register = template.Library()


def search_excerpt(
    text,
    phrases,
    context_words_count=None,
):
    return "blah blah"


class SearchExcerptNode(template.Node):

    def __init__(self, content, search_terms, context_words_count):
        self._content = template.Variable(content)
        self._search_terms = template.Variable(search_terms)
        self._context_words_count = context_words_count

    def render(self, context):
        try:
            content = self._content.resolve(context)
            search_terms = self._search_terms.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        return search_excerpt(
            text=content,
            phrases=search_terms,
            context_words_count=self._context_words_count
        )


@register.tag(name='search_excerpt_tag')
def search_excerpt_tag(parser, token):
    """
        {% search_excerpt_tag content search_terms [context_words_count] %}
    """
    try:
        # split_contents() knows not to split quoted strings.
        bits = list(token.split_contents())

    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0]
        )

    if len(bits) != 4:
        usage = search_excerpt_tag.__doc__.strip()
        raise TemplateSyntaxError(
            f"{bits[0]} expected usage: {usage}"
        )

    return SearchExcerptNode(
        content=bits[1],
        search_terms=bits[2],
        context_words_count=bits[3]
    )
