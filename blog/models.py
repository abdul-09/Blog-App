from platform import architecture
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.search import index
from wagtail.admin.panels import FieldPanel
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from datetime import date

# Create your models here.

class BlogPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    template = "blog/blog_page.html"

    def get_context(self, request):
        tag = request.GET.get('tag')
        if tag:
            articles = ArticlePage.objects.filter(tags__name=tag).live().order_by('-first_published_at')
        else:
            articles = ArticlePage.objects.live().order_by('-first_published_at')
        context = super().get_context(request)
        context['articles'] = articles
        context['tag'] = tag
        return context

class ArticlePage(Page):
    intro = models.CharField(max_length=100)
    body = RichTextField(blank=True)
    date = models.DateField("Post date", default=date.today)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+'
    )

    caption = models.CharField(blank=True, max_length=100)

    tags = ClusterTaggableManager(through='ArticleTag', blank=True)

    views = models.PositiveIntegerField(default=0, editable=False)

    def image_url(self):
        return self.image.get_rendition('fill-1200x675|jpegquality-80').url
    
    def get_context(self, request):
        context = super().get_context(request)
        context["image_url"] = self.image_url()
        return context

    def increment_view_count(self):
        self.views += 1
        self.save(update_fields=["views"])

    def serve(self, request):
        session_key = f"article_viewed_{self.pk}"
        if not request.session.get(session_key, False):
            self.increment_view_count()
            request.session[session_key] = True
        return super().serve(request)

    def get_tags(self):
        return ", ".join(tag.name for tag in self.tags.all())
    def get_author(self):
        return self.owner.profile.name
    def get_author_username(self):
        return self.owner.username

    search_fields = Page.search_fields +[
        index.SearchField('intro'),
        index.SearchField('body'),
        index.SearchField('get_tags'),
        index.SearchField('get_author'),
        index.SearchField('get_author_username'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('image'),
        FieldPanel('caption'),
        FieldPanel('body'),
        FieldPanel('date'),
        FieldPanel('tags'),
    ]

    template_name = 'blog/article_page.html'

class ArticleTag(TaggedItemBase):
    content_object = ParentalKey(ArticlePage, on_delete=models.CASCADE, related_name='tagged')