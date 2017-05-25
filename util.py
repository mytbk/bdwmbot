from functools import reduce


def item_to_md_html(item):
    markdown_strs = list(
        map(lambda t: '[{}]({})'.format(t['title'], t['url']), item))
    md = reduce(lambda s, t: s + '  \n' + t, markdown_strs)
    html_strs = list(
        map(lambda t: '<a href="{}">{}</a>'.format(t['url'], t['title']), item))
    html = reduce(lambda s, t: s + '<br />\n' + t, html_strs)
    return md, html


def tag_to_str(t):
    if hasattr(t, 'string'):
        s = t.string
        if s is None:
            s = ''
        return s
    else:
        return ''
