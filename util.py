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
    if hasattr(t, 'string') and t.string is not None:
        return str(t.string)
    elif hasattr(t, 'contents') and len(t.contents) > 0:
        return reduce(lambda t1, t2: t1 + t2, map(lambda x: tag_to_str(x), t.contents))
    else:
        return ''
