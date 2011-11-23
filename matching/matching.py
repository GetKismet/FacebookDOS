#!/usr/bin/env python

import os
import sys
import xmlrpclib

import MySQLdb

server = xmlrpclib.ServerProxy("http://kismet2.lognllc.com/services/xmlrpc")


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
	
def get_fb_likes_score(auth_token, uid, target_uid):	
	score = 0
	likes = server.fb_likes.get("SdGCrJNXxfxWeJytbUXfPVt3qFjcn6mkv5uYCcj6Qzzqq5RJWNwKpfbsZDTWUfCh", uid)

	print likes
	score = len(likes)
	if score > 10:
		score = 10

	return score

def get_fb_dos_score(auth_token, target_uid):
	score = 0
	output = server.fb.get_dos(auth_token, target_uid)
	print output
	return score
	

if __name__ == '__main__':
	global db
	global SERVER_PREFIX
	SERVER_PREFIX="http://kismet2.lognllc.com/admin/build/services/browse"

	db = MySQLdb.connect(host="localhost", passwd="", user="root", db="kismet")

	sql = "SELECT uid, token from services_authtoken_tokens"
	cursor = db.cursor()
	cursor.execute(sql)

	result_set = cursor.fetchall()
	rows = [(result[0], result[1]) for result in result_set]
	for data in rows:
		print data
		uid = data[0]
		auth_token = data[1]
		print "Uid is %s and auth_token is %s" %  (uid, auth_token)
		cursor.close() 
		service_score = get_service_score(uid) 
		print "service score is %d " % service_score
		for data2 in rows:
			target_uid = data2[0]	
			fb_likes_score = get_fb_likes_score(auth_token, uid, target_uid)
			print "fb likes score is %d" % fb_likes_score
			fb_dos_score = get_fb_dos_score(auth_token, target_uid)
			print "fb dos score is %d" % fb_dos_score
			total_score = service_score + fb_likes_score + fb_dos_score
			sql = "REPLACE INTO match_scores (uid, target_uid, service_score, fb_likes_score, fb_dos_score) values (%d, %d, %d, %d, %d)"  % (uid, target_uid, service_score, fb_likes_score, fb_dos_score)
			print sql 
			cursor = db.cursor()
			cursor.execute(sql)
		print cursor.fetchone()
		cursor.close() 
	db.close()
	

    
