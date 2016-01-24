# -*- coding: utf-8 -*- 
"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, request
from textblob import TextBlob, exceptions

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

reply_start = '''<?xml version="1.0" encoding="UTF-8"?><Response><Sms>'''
reply_end = '''</Sms></Response>'''
lang_list = ['en','zh','fr']
error_message = u'''sorry there's err, plz provide at least 3 chars\n出错了,请提供至少3个字'''

def get_xml_return(str):
    return reply_start + str + reply_end

@app.route('/')
def translate():
	try:
		msg = unicode(request.args.get('Body'))
		blob = TextBlob(msg)

		s = '\n'
		for lang in lang_list:
			try:
				translated = blob.translate(to=lang)
			except exceptions.NotTranslated:
				translated = msg
			s += (unicode(translated)+'\n')

		return get_xml_return(s)
	except Exception as e:
		return get_xml_return(error_message)
# def hello():
#     """Return a friendly HTTP greeting."""
#     return 'Hello World!'


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

if __name__ == '__main__':
	app.debug = True
	app.run()
