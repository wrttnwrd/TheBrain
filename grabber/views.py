# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
import grabber

def fetch(request, feedinfo):
	cmd = grabber.Command()
	go = cmd.handle(feedinfo)
	t = loader.get_template('grabber-output.html')
	smessage = go[1]
	feedname = go[2]
	feedback = go[0]
	
	c = Context({'smessage': smessage, 'feedname': feedname, 'feedback': feedback})
	
	return HttpResponse(t.render(c))