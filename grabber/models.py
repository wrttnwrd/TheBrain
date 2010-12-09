from django.db import models
from django.contrib import admin


# Create your models here.
class Feed(models.Model):
	feedid = models.AutoField(primary_key=True)
	url = models.CharField(max_length=250)
	feedname = models.CharField(max_length=200)
	etag = models.CharField(max_length=200)
	date_added = models.DateField(auto_now=True)
	modified = models.CharField(max_length=200)
	tagID = models.ManyToManyField('Tags', verbose_name='Tags')
	topicID = models.ManyToManyField('Topic', verbose_name='Topic')
	def __unicode__(self):
		return self.feedname
	def refreshLink(self):
		link = '<a href="../fetch/' + str(self.feedid) + '">Update</a>'
		return link
	refreshLink.allow_tags = True
	
		
class Tags(models.Model):
	tagid = models.AutoField(primary_key=True)
	tag = models.CharField(max_length=50)
	def __unicode__(self):
		return self.tag

class Topic(models.Model):
	topicID = models.AutoField(primary_key=True)
	topicname = models.CharField(max_length=150)
	date_added = models.DateField(auto_now=True)
	def __unicode__(self):
		return self.topicname
	
class Items(models.Model):
	itemID = models.AutoField(primary_key=True)
	def __unicode__(self):
		return self.title
	title = models.CharField(max_length=250)
	body = models.TextField()
	date_added = models.DateField(auto_now=True)
	added_by = models.IntegerField()
	url = models.URLField(verify_exists=False,max_length=250)
	itemdate = models.CharField(max_length=75)
	feedID = models.ForeignKey('Feed', verbose_name='Feed')
	topicID = models.ManyToManyField('Topic', verbose_name='Topic')
	tagID = models.ManyToManyField('Tags', verbose_name='Tags')

	
class FeedAdmin(admin.ModelAdmin):
	fields = ['url','feedname', 'tagID', 'topicID']
	list_display = ('feedname','url','refreshLink')
	
class ItemAdmin(admin.ModelAdmin):
	fields = ['title','body','url','itemdate','feedID','tagID','topicID']

class TopicAdmin(admin.ModelAdmin):
	fields = ['topicname']
	
class TagsAdmin(admin.ModelAdmin):
	fields = ['tag']
