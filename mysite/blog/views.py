from django.shortcuts import render, redirect
from django.db.models import Q, Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Article
from . import forms
from datetime import datetime, date

def get_rank_article_list():
    return Article.objects.filter(show=True).order_by('-views')[:10]

def get_category_dict():
    article_caterogy_dict = Article.objects.filter(show=True).values('category')
    category_set = {category for category_dict in article_caterogy_dict for category in category_dict['category'].split(";") if category != ''}
    category_dict = {}
    for category in sorted(category_set):
        category_count = 0
        for article_caterogy in article_caterogy_dict:
            if category in article_caterogy['category']:
                category_count += 1
        category_dict[category] = category_count
    return category_dict

def get_archive_dict():
    archive_dict = {}
    for created_date in Article.objects.values_list('created_date', flat=True).filter(show=True):
        key = str(created_date.year) + '-' + str(created_date.month)
        archive_dict[key] = (archive_dict.get(key, 0) + 1)
    return {key:value for key, value in sorted(archive_dict.items(), key=lambda x:x[0], reverse=True)}

def paginate_query(request, queryset, count=5):
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginatot.page(paginator.num_pages)
    return page_obj

def index(request):
    articles = Article.objects.filter(show=True)
    form = forms.SearchForm()

    if request.GET.get('q'):
        query_str = request.GET.get('q')
        articles = articles.filter(
            Q(title__contains = query_str) |
            Q(body__contains = query_str)
        )

    articles = paginate_query(request, articles)
    return render(request, 'blog/index.html', {
        'articles': articles,
        'rank_articles': get_rank_article_list(),
        'category_dict': get_category_dict(),
        'archive_dict': get_archive_dict(),
        'form': form
    })

def article(request, pk):
    article = Article.objects.get(id=pk)
    article.views += 1
    article.save()

    return render(request, 'blog/article.html', {
        'article': article,
        'rank_articles': get_rank_article_list(),
        'category_dict': get_category_dict(),
        'archive_dict': get_archive_dict()
    })

def search_category(request, category):
    articles = Article.objects.filter(show = True, category__contains = category)

    articles = paginate_query(request, articles)
    return render(request, 'blog/index.html', {
        'articles': articles,
        'rank_articles': get_rank_article_list(),
        'category_dict': get_category_dict(),
        'archive_dict': get_archive_dict()
    })

def search_archive(request, year_month):
    articles = Article.objects.filter(show = True)
    split_y_m = year_month.split("-")
    if len(split_y_m) > 1:
        articles = paginate_query(request, articles.filter(created_date__year=split_y_m[0], created_date__month=split_y_m[1]))
    else:
        articles = paginate_query(request, articles.filter(created_date__year=split_y_m[0]))

    return render(request, 'blog/index.html', {
        'articles': articles,
        'rank_articles': get_rank_article_list(),
        'category_dict': get_category_dict(),
        'archive_dict': get_archive_dict()
    })