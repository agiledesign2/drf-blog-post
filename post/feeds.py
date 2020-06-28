from django.contrib.syndication.views import Feed
from .models import Post


class LastEntriesFeed(Feed):
    title = "Latest posts"
    link = "/"
    description = "Latest posts"

    def items(self):
        return Post.objects.published().order_by("-published")

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        words = item.content.split(" ")[:10]
        return " ".join(words) + "..."
