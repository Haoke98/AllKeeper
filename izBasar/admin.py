from django.utils.safestring import mark_safe

LIST_DISPLAY = ['id', 'updatedAt', 'createdAt', 'deletedAt']


def showUrl(url):
    if url:
        tag = mark_safe('''<a href="%s" target="blank" class="button" title="%s">URL</a>''' % (url, url))
    else:
        tag = "-"
    return tag
