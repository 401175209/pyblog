from markdown import markdown
from markdown import Markdown
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DeleteView

from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from .models import Post,Category,Tag
from comments.form import commentform
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

class IndexView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'post_list'
    paginate_by = 10

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)

class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(create_time__year=year,
                                                               create_time__month=month
                                                               )
class PostDetailView(DeleteView):
    model = Post
    template_name = 'detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)

        md = Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify)
        ])
        post.content = md.convert(post.content)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = commentform()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context
def search(request):
    q=request.GET.get('q')
    error_msg=''
    if not q:
        error_msg='请输入关键词'
        return render(request,'index.html',{'error_msg':error_msg})
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
    return render(request, 'index.html', {'error_msg': error_msg,'post_list': post_list})

def about(request):
    return render(request,'about.html')
# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     # 记得在顶部引入 markdown 模块
#     post.content = markdown(post.content,
#                                   extensions=[
#                                      'markdown.extensions.extra',
#                                      'markdown.extensions.codehilite',
#                                      'markdown.extensions.toc',
#                                   ])
#     form=commentform()
#     comment_list = post.comment_set.all()
#     context = {'post': post,
#                'form': form,
#                'comment_list': comment_list
#                }
#     return render(request, 'detail.html', context=context)
#
# def archives(request,year,month):
#     post_list=Post.objects.filter(create_time__year=year,create_time__month=month).order_by('-create_time')
#
#     return render(request,'index.html',context={'post_list':post_list})
#
# def category(request,pk):
#     cate=get_object_or_404(Category, pk=pk)
#     post_list=Post.objects.filter(category=cate).order_by('-create_time')
#     return  render(request,'index.html',context={'post_list':post_list})