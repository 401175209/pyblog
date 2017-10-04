from django import template
from ..models import Post,Category,Tag
from django.db.models.aggregates import Count
'''自定义最新文章标签'''

register=template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by("-create_time")[:num]

'''自定义归档标签'''
@register.simple_tag
def archives():
    return Post.objects.dates('create_time','month',order='DESC')

'''自定义分类标签'''
@register.simple_tag
def categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

'''自定义分类标签'''
@register.simple_tag
def tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)