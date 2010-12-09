from django.core.management.base import BaseCommand, CommandError
from thebrain.grabber.models import Feed
from thebrain.grabber.models import Items
from thebrain.grabber.models import Tags
from thebrain.grabber.models import Topic

import sys
import string
import feedparser
import MySQLdb
from time import time

class Command(BaseCommand):
	args = '<feedinfo>'
	help = 'Goes out and grabs specified feed items, then stores in the database'

	def handle(self,*args, **options):
		for arg in args:
			feedid = int(arg)
		feedback = []
		print "starting run"
		db = MySQLdb.connect("localhost","root","","thebraindjango" )

		cursor = db.cursor()

		#grab the basic feed data
		sql = "SELECT feedid,url,feedname,etag,modified FROM grabber_feed WHERE feedid = %s"
		cursor.execute(sql,(feedid))
		results = cursor.fetchall()
		
		#grab any tags and topics for this feed, too
		sql = "SELECT topic_id FROM grabber_feed_topicid WHERE feed_id = %s"
		y = cursor.execute(sql,(feedid))
		topics = cursor.fetchall()
			
		sql = "SELECT tags_id FROM grabber_feed_tagid WHERE feed_id = %s"
		y = cursor.execute(sql,(feedid))
		tags = cursor.fetchall()
		

		for f in results:
			feedid = f[0]
			thisurl = f[1]
			thisfeed = thisurl.strip()
			feedname = f[2]
			etag = f[3]
			modified = f[4]
			#check to see if the feed already has an etag - if so, check if updates
			if (etag):
				feed = feedparser.parse(thisfeed,etag=etag)
				status = int(feed.status)
			#if no etag, try modified date - if neither, just run anyway
			elif (modified):
				status = 0
				feed = feedparser.parse(thisfeed, modified=modified)
			else:
				feed = feedparser.parse(thisfeed)
				try:
					etag = feed.etag
				except AttributeError:
					etag = ''
				try:
					modified = feed.modified
				except AttributeError:
					modified = ''
				status = 0
			sql = "UPDATE grabber_feed SET etag = %s,modified = %s WHERE feedid = %s"
			cursor.execute(sql,(etag,modified,feedid))	
			if (status != 304):
				for i in feed["items"]:
					itemdate = i["date"]
					title = i["title"]
					title = title.encode('utf-8')
					try:
						body = i["summary"]
					except KeyError:
						body = "Couldn't get body for some reason"
					body = body.encode('utf-8')
					url = i["link"]
					feedID_id = feedid
					added_by = 1
					sql = "SELECT feedID_id FROM grabber_items WHERE title = %s AND feedID_id = %s AND itemdate = %s"
					cursor.execute(sql,(title,feedID_id,itemdate))
					counter = cursor.fetchone()
					if (counter):
						fb = title + " <em>was not added - it is already in db</em>"
						feedback.append(fb)
						
					else:
						fb = title + " " + str(url) + " stored<br />"
						feedback.append(fb)
						sql = "INSERT INTO grabber_items(title,feedID_id,body,added_by,url,itemdate) VALUES(%s,%s,%s,%s,%s,%s)"
						cursor.execute(sql,(title,feedID_id,body,added_by,url,itemdate))
						#grab the id of the new item
						sql = "SELECT MAX(itemID) from grabber_items"
						cid = cursor.execute(sql)
						cid = cursor.fetchone()
						iid = cid[0]
						if (tags):
							for t in tags:
								tagsid = t[0]
								sql = "INSERT INTO grabber_items_tagid(items_id,tags_id) VALUES(%s,%s)"
								cursor.execute(sql,(iid,tagsid))
								
						if (topics):
							for t in topics:
								topicid = t[0]
								sql = "INSERT INTO grabber_items_topicid(items_id,topic_id) VALUES(%s,%s)"
								cursor.execute(sql,(iid,topicid))
						
				smessage = True
			else:
				smessage = False
						
		
		return(feedback,smessage,feedname)