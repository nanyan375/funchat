# -*- coding: utf-8 -*-

from bleach import clean, linkify
from flask import flash
from markdown import markdown

def to_html(raw):
    # 过滤标签白名单
    allowed_tags = ['a', 'abbr', 'b', 'br', 'blockquote', 'code', 
                    'del', 'div', 'em', 'img', 'p', 'pre', 'strong',
                    'span', 'ul', 'li', 'ol',]
    # 过滤属性白名单
    allowed_attributes = ['src', 'title', 'alt', 'href', 'class']
    html = markdown(raw, output_format='html',
                    extensions=['markdown.extensions.fenced_code',
                    'markdown.extensions.codehilite'])
    clean_html = clean(html, tags=allowed_tags, attributes=allowed_attributes)
    # 将文本里的URL转化为链接形式
    return linkify(clean_html)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u'Error in the %s field - %s'%(
                getattr(form, field).label.text, error
            ))