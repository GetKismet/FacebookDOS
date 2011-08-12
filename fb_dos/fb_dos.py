#!/usr/bin/env python

import os, sys, getopt, MySQLdb, phpserialize, math, time
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent+'/lib')
import fb_user
from fb_dos_thread import FbDosThread

def calculate_dos(target_uid, source_uid, max_threads, friends_per_thread, access_token):
    global db
    sql = "SELECT `data` FROM `cache_fb_dos` WHERE `cid`=%s"
    cursor = db.cursor()
    cursor.execute(sql, 'friends:'+source_uid)
    data = cursor.fetchone()
    cursor.close()
    
    if (data is None):
        sys.exit(2)
    friends = phpserialize.loads(data=data[0], object_hook=parse_user)
    friends_list = list()
    for k in friends.iterkeys():
        friends_list.append(friends[k].id)
    
    num_friends = len(friends_list)
    if (num_friends > max_threads*friends_per_thread):
        per_thread = math.ceil(num_friends/max_threads)
    else:
        per_thread = friends_per_thread
    
    thread_uids = list(array_chunk(friends_list, int(per_thread)))
    _calculate_dos(target_uid, source_uid, thread_uids, access_token)

def _calculate_dos(target_uid, source_uid, thread_uids, access_token):
    thread_list = list()
    for uids in thread_uids:
        thread = FbDosThread(access_token, target_uid, source_uid, uids)
        thread.start()
        thread_list.append(thread)
        
    keep_looking = True
    path = list()
    while keep_looking:
        all_threads_dead = True
        for thread in thread_list:
            if thread.isAlive():
               all_threads_dead = False
               
            if thread.found_path:
                path = thread.path
                keep_looking = False
                for thread in thread_list:
                    thread.stop()
            
        
        if (all_threads_dead): # means no path was found
            break
        if keep_looking:
            time.sleep(0.5)
    
    save_path(path, target_uid, source_uid)

def save_path(path, target_uid, source_uid):
    if (len(path) == 2):
        print phpserialize.dumps({
           "link": path[0],
           "path": path[1],
        });
    else:
        print ""

def parse_user(name, dict):
    return fb_user.FbUser(dict['id'], dict['name'])
    
def array_chunk(list_input, size_per_chunk):
    for i in xrange(0, len(list_input), size_per_chunk):
        yield list_input[i:i + size_per_chunk]

if __name__ == '__main__':
    global db
    
    options, args = getopt.getopt(sys.argv[1:], '', [
        'target_uid=', 'source_uid=',
        'max_threads=', 'friends_per_thread=',
        'access_token=',
        'db_host=', 'db_user=', 'db_pass=', 'db_name=']
    )
    target_uid = None
    souce_uid = None
    max_threads = None
    friends_per_thread = None
    access_token = None
    db_host = None
    db_user = None
    db_pass = ""
    db_name = None
    
    for opt, arg in options:
        if opt == "--target_uid":
            target_uid = arg
        elif opt == "--source_uid":
            source_uid = arg
        elif opt == "--max_threads":
            max_threads = int(arg)
        elif opt == "--friends_per_thread":
            friends_per_thread = int(arg)
        elif opt == "--access_token":
            access_token = arg
        elif opt == "--db_host":
            db_host = arg
        elif opt == "--db_user":
            db_user = arg
        elif opt == "--db_pass":
            db_pass = arg
        elif opt == "--db_name":
            db_name = arg
            
    if target_uid is None or source_uid is None:
        target_uid = "520903457"
        source_uid = "579417450"
    if db_host is None or db_user is None or db_name is None:
        db_host = "localhost"
        db_user = "root"
        db_name = "kismet"
        db_pass = ""
    if max_threads is None:
        max_threads = 10
    if friends_per_thread is None:
        friends_per_thread = 25
    if access_token is None:
        access_token = "166840593353700|a3d4ec4bff6496a965980421.3-520903457|yKbyjXt_WTRU_4643z2bglSb2Ts"
    
    db = MySQLdb.connect(host=db_host, passwd=db_pass, user=db_user, db=db_name)
    calculate_dos(target_uid, source_uid, max_threads, friends_per_thread, access_token)