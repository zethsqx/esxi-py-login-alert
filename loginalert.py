import urllib.request
import ssl
import os
import json
import sys
import subprocess

#Import env values for telegram
chatid = '00000000' #replace if hardcode needed
teleid = 'aaabbbcccddeeff' #replace if hardcode needed
telelink = "https://api.telegram.org/bot" + teleid + "/{}?{}"

#Broadcast message to the telegram chat of
def broadcastMessage(elink,einfo):
   headers = {"Accept": "application/json"}
   myssl = ssl._create_unverified_context()
   params = {"text": einfo}
   params.update({"chat_id": chatid})
   url = elink.format("sendMessage", urllib.parse.urlencode(params))
   request = urllib.request.Request(url, None, headers)
   with urllib.request.urlopen(request, context=myssl) as r:
     r.read()

#Send telegram msg
f = subprocess.Popen(['tail','-F', '/var/log/hostd.log'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
while True:
    line = f.stdout.readline()
    if b'logged' in line:
         broadcastMessage(telelink, line)
#         print(line)
