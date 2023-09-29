from django import template
import markdown
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter
def sub(value, arg):
    return value - arg

'''
markdown 모듈과 mark_safe 함수를 이용하여 입력 문자열을 HTML로 변환하는 필터 함수
좀 더 확장가능
'''
@register.filter
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))
