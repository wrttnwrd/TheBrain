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
	args = '<feedid feedid ...>'
	help = 'Goes out and grabs specified feed items, then stores in the database'

	def handle(self,*args, **options):
		for feedid in args:

			print "starting run"

			db = MySQLdb.connect("localhost","root","","thebraindjango" )

			cursor = db.cursor()

			sql = "SELECT feedid,url,feedname,etag,modified FROM grabber_feed WHERE feedid = %s order by feedid"
			cursor.execute(sql,(feedid))
			results = cursor.fetchall()

			for f in results:
				feedid = f[0]
				thisurl = f[1]
				thisfeed = thisurl.strip()
				etag = f[3]
				modified = f[4]
				#check to see if the feed already has an etag - if so, check if updates
				if (etag):
					feed = feedparser.parse(thisfeed, etag=etag)
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
						topicID_id = 1
						sql = "SELECT feedID_id FROM grabber_items WHERE title = %s AND feedID_id = %s AND itemdate = %s"
						cursor.execute(sql,(title,feedID_id,itemdate))
						counter = cursor.fetchone()
						if (counter):
							print title,"is already in db"
						else:
							print feedID_id,"\t",title,"\t",url,"\t",itemdate,"\t",topicID_id
							sql = "INSERT INTO grabber_items(title,feedID_id,body,added_by,url,itemdate,topicID_id) VALUES(%s,%s,%s,%s,%s,%s,%s)"
							cursor.execute(sql,(title,feedID_id,body,added_by,url,itemdate,topicID_id))
