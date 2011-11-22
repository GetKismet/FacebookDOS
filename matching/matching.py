#!/usr/bin/env python

import os, sys, getopt, MySQLdb, phpserialize, math, time, urllib2, urllib, httplib
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent+'/lib')
import fb_user


def get_service_score(uid): 
	score = 0 
	cursor = db.cursor()

    # if twitter is enabled add 2
	SQL = "select * from %s_users where uid=" + str(uid)
	SERVICES = {"twitter":2, "instagram":4, "goodreads":8, "pandora":4, "flickr":5, "picplz":4, "foursquare":3}

	for service in  SERVICES.keys():
		SQL2 = SQL % service
		cursor.execute(SQL2)
		data = cursor.fetchone()

		if data:
			score = score + SERVICES[service]

	if score > 20:
		score = 20
	return score
	
def get_fb_likes_score(uid, target_uid, access_token):	
	print "Access token is " + access_token
	API_URL = SERVER_PREFIX + "/fb_likes.get"

	score = 0
	params = urllib.urlencode({'arg[0]': "SdGCrJNXxfxWeJytbUXfPVt3qFjcn6mkv5uYCcj6Qzzqq5RJWNwKpfbsZDTWUfCh", 'arg[1]': target_uid, 'arg[2]': uid, 'op': "Call method", "auth_token": "SdGCrJNXxfxWeJytbUXfPVt3qFjcn6mkv5uYCcj6Qzzqq5RJWNwKpfbsZDTWUfCh"})
	print params
	print API_URL
	f = None
	try:
		f = urllib2.urlopen(API_URL, params)
		output = f.read()
	except:
		print "error"
	finally:
		if f:
			f.close()
	#print "output is" + output

	if score > 10:
		score = 10

	return score

def get_fb_dos_score(auth_token, target_uid):
	score = 0
	API_URL = SERVER_PREFIX + "/fb.get_dos"

	score = 0
	params = urllib.urlencode({'auth_token': "SdGCrJNXxfxWeJytbUXfPVt3qFjcn6mkv5uYCcj6Qzzqq5RJWNwKpfbsZDTWUfCh", 'target_uid': target_uid})
	h = httplib.HTTPConnection('kismet2.lognllc.com:80')
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	h.request('POST', '/admin/build/services/browse/fb.get_dos', params, headers)
	r = h.getresponse()
	output = r.read()
	print "output is " +  output
	print "output is %s" % r.status
	return score
	

if __name__ == '__main__':
	global db
	global SERVER_PREFIX
	SERVER_PREFIX="http://kismet2.lognllc.com/admin/build/services/browse"


	db = MySQLdb.connect(host="localhost", passwd="", user="root", db="kismet")
	sql = "SELECT uid, access_token from fb_users where fb_uid=506200023"
	cursor = db.cursor()
	cursor.execute(sql)
	data = cursor.fetchone()
	uid = data[0]
	access_token = data[1]
	cursor.close() 
	service_score = get_service_score(uid) 
	print "service score is %d " % service_score
	fb_likes_score = get_fb_likes_score(uid, uid, access_token)
	print "fb likes score is %d" % fb_likes_score
	fb_dos_score = get_fb_dos_score("", 138)
	print "fb dos score is %d" % fb_dos_score


    
