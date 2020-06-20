from django import template
from django.template import Node, TemplateSyntaxError

register = template.Library()


def search_excerpt(
    text,
    phrases,
    context_words=None,
    ignore_case=None,
    word_boundary=None
):
    pass


class Proxy(Node):

    def __init__(self, nodelist, args, variable_name=None):
        self.nodelist = nodelist
        self.args = args
        self.variable_name = variable_name

    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        text = self.nodelist.render(context)
        value = self.get_value(text, *args)

        if self.variable_name:
            context[self.variable_name] = value
            return ""
        else:
            return self.string_value(value)

    def get_value(self, *args):
        raise NotImplementedError

    def string_value(self, value):
        return value


class SearchExcerptNode(Proxy):

    def get_value(self, *args):
        return search_excerpt(*args)

    def string_value(self, value):
        return value['excerpt']


@register.tag
def search_excerpt_tag(parser, token):
    """
        {%
            search_excerpt_tag \
                search_terms \
                [context_words] \
                [ignore_case] \
                [word_boundary] \
                [as name]
        %}
        ...text...
        {% endsearchexcerpt %}
    """
    try:
        # split_contents() knows not to split quoted strings.
        bits = list(token.split_contents())

    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0]
        )

    if not 3 <= len(bits) <= 8:
        usage = search_excerpt_tag.__doc__.strip()
        raise TemplateSyntaxError(
            f"{bits[0]} expected usage: {usage}"
        )

    if len(bits) > 4 and bits[-2] == "as":
        args, name = bits[1:-2], bits[-1]
    else:
        args, name = bits[1:], None

    nodelist = parser.parse(('endsearch_excerpt_tag',))
    parser.delete_first_token()

    return SearchExcerptNode(nodelist, map(parser.compile_filter, args), name)
