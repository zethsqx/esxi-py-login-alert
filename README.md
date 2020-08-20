# esxi-py-login-alert

## Overview
Similar concept to my other esxi project. This will send alert when there is a login and logout on the esxi.

#### My Environment
Tested on ESXi 6.7

**Good for**
- When you need to track your ESXi in a network you have no control
- When you know paying for ESXi is too expensive
- When you dont mind tweaking the ESXi 

**Bad for**
- Everything
- Consider using alternative, it probably violates some policy

## Prerequisite

- A ESXi running on free
- Secure Boot disable in BIOS
- Root account for ESXi
- Can SSH into the ESXi
- Enable ruleset on the ESXi
- Telegram

## Setting up

### ESXi
Step 1: Enable remoteSerialPort so python urllib.request can hit Local Server  
Step 2: Enable httpClient so python urllib.request can hit External Server (Optional)

SSH into ESXi and run the following
```
esxcli network firewall ruleset list
esxcli network firewall ruleset set --ruleset-id=remoteSerialPort --enabled true  
esxcli network firewall ruleset set --ruleset-id=httpClient --enabled true
```
Testing to Local Server
```
# python3
>>> import urllib.request
>>> req = urllib.request.Request('http://192.168.100.10/')
>>> response = urllib.request.urlopen(req)
>>> print(response.read())
```
Testing to External Server
```
# python3
>>> import urllib.request
>>> req = urllib.request.Request('https://github.com/')
>>> response = urllib.request.urlopen(req)
>>> print(response.read())
```
If you encounter errors such as; *No route to host*, *Name or service not known*  
Try disabling the firewall and run again
```
esxcli network firewall set --enabled false
```

Step 3: Transfer the script to the datastore. Easier to use UI to upload  

### About Telegram
Refer to links for information how to create bot -
- https://core.telegram.org/bots/faq#how-do-i-create-a-bot
- https://docs.microsoft.com/en-us/azure/bot-service/bot-service-channel-connect-telegram?view=azure-bot-service-4.0 (Useful steps-by-steps to create bot)

The end goal is to get your  
1) Bot Token
2) Chat Id

```
1. Send a message to your bot

2. Go to following url: https://api.telegram.org/botXXX:YYYY/getUpdates
replace XXX:YYYY with your bot token

3. Look for “chat”:{“id”:zzzzzzzzzz,
zzzzzzzzzz is your chat id (with the negative sign).
```

## Wrapping up script to Persistent Cronjob

Setup a persistent cronjob for the script. I set it to run at every 10th minute, do change according to your liking.  
Change <$DATASTORE> path to the one you uploaded at ESXi Step 2  
```
1. Edit /etc/rc.local.d/local.sh, insert this before the exit 0 line:
/bin/kill $(cat /var/run/crond.pid)  
/bin/python3 /vmfs/volumes/datastore1/loginalert.py &  
/usr/lib/vmware/busybox/bin/busybox crond  

2. Run the script:
/bin/sh /etc/rc.local.d/local.sh

3. Make the changes persistent:
/bin/auto-backup.sh
```
In case, you need to turn off the annoying cronjob temporarily
```
1. Edit corn jobs
vi /var/spool/cron/crontabs/root

2. Check crond pross id
cat /var/run/crond.pid

3. Kill old crond
/bin/kill $(cat /var/run/crond.pid)

4. Restart cron jobs
/usr/lib/vmware/busybox/bin/busybox crond 
```
