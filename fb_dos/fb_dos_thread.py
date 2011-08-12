#!/usr/bin/env python
import threading, urllib, json, types

class FbDosThread (threading.Thread):
    def __init__(self, access_token, target_uid, source_uid, uids):
        super(FbDosThread, self).__init__()
        
        self.access_token = access_token
        self.target_uid = target_uid
        self.source_uid = source_uid
        self.uids = uids
        self._stop = threading.Event();
        self.found_path = False;
        self.path = None
        
    def run(self):
        for uid in self.uids:
            if (self.stopped()):
                return;
            
            res = self.facebook_request(uid)
            if res == "[]":
                continue;
            
            j = json.loads(res)
            if type(j).__name__ == "dict" and j['error_code'] is not None:
                return
            
            self.found_path = True
            self.path = [uid, j]
        
    def stop(self):
        self._stop.set()
        
    def stopped(self):
        return self._stop.isSet()
        
    def facebook_request(self, uid):
        url = "https://api.facebook.com/method/friends.getMutualFriends?format=json&access_token="+self.access_token+"&source_uid="+self.target_uid+"&target_uid="+uid
        
        conn = urllib.urlopen(url)
        data = conn.read()
        conn.close()
        
        return data