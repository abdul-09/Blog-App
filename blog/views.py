from operator import attrgetter
from django.shortcuts import render

from blog.models import ArticlePage

# Create your views here.
def article_search(request):
    search_query = request.GET.get('query', '').strip()
    if search_query:
        articles = ArticlePage.objects.live().search(search_query)
        articles = sorted(articles, key=attrgetter('first_published_at'), reverse=True)
    else:
        articles = ArticlePage.objects.live().order_by('-first_published_at')
    context = {
        'articles': articles,
        'search_query': search_query,
    }

    return render(request, 'blog/blog_page.html', context)