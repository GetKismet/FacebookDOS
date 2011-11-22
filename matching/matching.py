#!/usr/bin/env python

import os, sys, getopt, MySQLdb, phpserialize, math, time, urllib2,urllib
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
	API_URL = SERVER_PREFIX + "/fb_likes.get_common_likes"

	score = 0
	params = urllib.urlencode({'arg[0]': access_token, 'arg[1]': target_uid, 'arg[2]': uid, 'op': "Call method"})
	f = urllib2.urlopen(API_URL, params)
	print params
	print API_URL
	output = f.read()
	print "output is" + output


	

	if score > 10:
		score = 10

	return score

if __name__ == '__main__':
	global db
	global SERVER_PREFIX
	SERVER_PREFIX="http://kismet2.lognllc.com/admin/build/services/browse"


	db = MySQLdb.connect(host="localhost", passwd="", user="root", db="kismet")
	sql = "SELECT uid, access_token from fb_users where fb_uid=633267821"
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


    
