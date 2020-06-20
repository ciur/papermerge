import re

from django import template
from django.template import TemplateSyntaxError
from django.utils.safestring import mark_safe

register = template.Library()

# https://djangosnippets.org/snippets/661/


def _merge(lists):
    merged = []
    for words in lists:
        if merged:
            merged[-1] += words[0]
            del words[0]
        merged.extend(words)
    return merged


def highlight(
    text,
    phrases,
    class_name='success'
):
    if isinstance(phrases, str):
        phrases = [phrases]

    phrases = map(re.escape, phrases)
    flags = re.I
    re_template = r"\b(%s)\b" or r"(%s)"
    expr = re.compile(re_template % "|".join(phrases), flags)
    template = '<span class="%s">%%s</span>' % class_name
    matches = []

    def replace(match):
        matches.append(match)
        return template % match.group(0)

    highlighted = mark_safe(expr.sub(replace, text))

    return dict(
        original=text,
        highlighted=highlighted,
    )


def search_excerpt(
    text,
    phrases,
    context_words_count=5,
):
    if isinstance(phrases, str):
        phrases = [phrases]

    flags = re.I
    exprs = [
        re.compile("^%s$" % p, flags) for p in phrases
    ]
    whitespace = re.compile(r"\s+")
    re_template = r"\b(%s)\b" or r"(%s)"

    pattern = re_template % "|".join(phrases)
    pieces = re.compile(pattern, flags).split(text)
    matches = {}
    word_lists = []

    for i, piece in enumerate(pieces):
        word_lists.append(whitespace.split(piece))
        if i % 2:  # matched piece
            for expr in exprs:
                if expr.match(piece):
                    matches.setdefault(expr, []).append(i)

    i = 0
    merged = []
    for j in map(min, matches.values()):
        merged.append(
            _merge(word_lists[i:j])
        )
        merged.append(word_lists[j])
        i = j + 1

    merged.append(
        _merge(word_lists[i:])
    )

    output = []
    for i, words in enumerate(merged):
        omit = None
        if i == len(merged) - 1:
            omit = slice(max(1, 2 - i) * context_words_count + 1, None)
        elif i == 0:
            omit = slice(-context_words_count - 1)
        elif not i % 2:
            omit = slice(context_words_count + 1, -context_words_count - 1)
        if omit and words[omit]:
            words[omit] = ["..."]

        output.append(" ".join(words))

    return dict(
        original=text, excerpt="".join(output)
    )


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
