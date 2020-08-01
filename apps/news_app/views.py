from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .form import ContentFrom, ArticleForm
from .models import News, Category
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    articles = News.objects.all()
    new_articles = articles[0:5]

    limit = 3
    paginator = Paginator(articles, limit)
    page = request.GET.get('page')

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    categories = Category.objects.all()
    context = {
        'articles': articles,
        'new_articles': new_articles,
        'categories': categories,
    }
    return render(request, 'article/index.html', context=context)


def article_detail(request, article_id):
    article = News.objects.get(pk=article_id)
    new_articles = News.objects.filter()[0:5]
    categories = Category.objects.all()
    context = {
        'article': article,
        'new_articles': new_articles,
        'categories': categories,
    }
    return render(request, 'article/article_detail.html', context=context)


@login_required(login_url='/login/')
def write_article(request):
    if request.method == 'GET':
        user_id = request.user.pk
        user = User.objects.get(pk=user_id)
        articles = user.news_set.all()
        categories = Category.objects.all()
        context = {
            'content': ContentFrom(),
            'categories': categories,
            'articles': articles,
        }

        return render(request, 'article/write_article.html', context=context)
    else:
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            author_id = request.user.pk
            category_id = form.cleaned_data.get('category')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = request.POST.get('editor1')
            article = News(title=title, category_id=category_id, author_id=author_id, desc=desc, thumbnail=thumbnail, content=content)
            article.save()
            article_id = article.pk
            context = {
                'article_id': article_id,
            }
            return render(request, 'article/pub_success.html', context=context)
        else:
            return HttpResponse('这里的表单验证我懒得做了，返回上一页检查一下输入的内容')


@login_required(login_url='/login/')
def article_management(request, username):
    if username != request.user.username:
        raise Http404
    else:
        user = User.objects.get(username=username)
        articles = user.news_set.all()
        context = {
            'articles': articles,
        }
        return render(request, 'article/manage_article.html', context=context)


def delete_article(request, article_id):
    user = request.user
    article = user.news_set.filter(pk=article_id).first()
    if not article:
        raise Http404
    else:
        if request.method == 'GET':
            context = {
                'article': article,
            }
            return render(request, 'article/delete_confirm.html', context=context)
        else:
            News.objects.get(pk=article_id).delete()
            return redirect(reverse('news_app:article_management', kwargs={"username": request.user.username}))


@login_required(login_url='/login/')
def edit_article(request, article_id):
    user = request.user
    article = user.news_set.filter(pk=article_id).first()
    categories = Category.objects.all()
    articles = request.user.news_set.all()
    if not article:
        raise Http404
    else:
        if request.method == 'GET':
            context = {
                'article': article,
                'categories': categories,
                'articles': articles,
            }
            return render(request, 'article/edit_article.html', context=context)

        else:
            form = ArticleForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                author_id = request.user.pk
                category_id = form.cleaned_data.get('category')
                desc = form.cleaned_data.get('desc')
                thumbnail = form.cleaned_data.get('thumbnail')
                content = request.POST.get('editor1')
                News.objects.filter(pk=article_id).update(title=title, category_id=category_id, author_id=author_id, desc=desc, thumbnail=thumbnail, content=content)
                return redirect(reverse('news_app:article_detail', kwargs={'article_id': article_id}))
            else:
                return HttpResponse('fail')


def search(request):
    keyword = request.GET.get('keyword')
    if keyword:
        articles = News.objects.filter(title__icontains=keyword) or News.objects.filter(category__name__icontains=keyword)
    else:
        articles = News.objects.all()
        keyword = ""

    context = {
        'articles': articles,
        'keyword': keyword,
    }
    return render(request, 'article/search.html', context=context)


def category_page(request, category_name):
    try:
        category = Category.objects.get(name=category_name)
        articles = category.news_set.all()
        limit = 4
        paginator = Paginator(articles, limit)
        page = request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        context = {
            'category': category,
            'articles': articles,
        }
        return render(request, 'article/category.html', context=context)
    except:
        raise Http404


def about(request):
    return render(request, 'article/about.html')

