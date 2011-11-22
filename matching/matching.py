#!/usr/bin/env python

import os, sys, getopt, MySQLdb, phpserialize, math, time
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent+'/lib')
import fb_user

def get_service_score(uid): 
	service_score = 0 
	cursor = db.cursor()

    # if twitter is enabled add 2
	SQL = "select * from %s_users where uid=" + str(uid)
	SERVICES = {"twitter":2, "instagram":4, "goodreads":8, "pandora":4, "flickr":5, "picplz":4, "foursquare":3}

	for service in  SERVICES.keys():
		SQL2 = SQL % service
		print "SQL is " + SQL2
		cursor.execute(SQL2)
		data = cursor.fetchone()

		if data:
			print "hit"
			service_score = service_score + SERVICES[service]

	if service_score > 20:
		service_score = 20
	return service_score
	
	

if __name__ == '__main__':
	global db


	db = MySQLdb.connect(host="localhost", passwd="", user="root", db="kismet")
	sql = "SELECT uid from fb_users where fb_uid=633267821"
	cursor = db.cursor()
	cursor.execute(sql)
	data = cursor.fetchone()
	uid = data[0]
	cursor.close() 
	service_score = get_service_score(uid) 
	print "service score is %d " % service_score


    
