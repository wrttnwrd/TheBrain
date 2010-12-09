from thebrain.grabber.models import Feed
from thebrain.grabber.models import FeedAdmin
from thebrain.grabber.models import Items
from thebrain.grabber.models import ItemAdmin
from thebrain.grabber.models import Tags
from thebrain.grabber.models import TagsAdmin
from thebrain.grabber.models import Topic
from thebrain.grabber.models import TopicAdmin
from django.contrib import admin

admin.site.register(Items, ItemAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Tags, TagsAdmin)
