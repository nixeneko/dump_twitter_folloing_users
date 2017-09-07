#!/usr/bin/env python
#coding:utf-8
import twitter
import os, codecs
import json
import copy
import datetime

JSONDUMPDIR = "dump_json"

consumerKey = ''
consumerSecret = ''
accessToken = ''
accessSecret = ''

consumerkeyfile = 'consumerkey'
accesstokenfile = 'accesstoken'

# load consumerKey from file
# consumerKey file should be: "<consumerKey>\n<consumerSecret>\n"
consumerKey, consumerSecret = twitter.read_token_file(consumerkeyfile)

if not os.path.exists(accesstokenfile):
    twitter.oauth_dance("Dump List of Following Users", consumerKey, consumerSecret,
                accesstokenfile)

accessToken, accessSecret = twitter.read_token_file(accesstokenfile)

tw = twitter.Twitter(auth=twitter.OAuth(
    accessToken, accessSecret, consumerKey, consumerSecret))


def dumpjson(data, destpath):
    if not os.path.exists(os.path.dirname(destpath)):
        os.makedirs(os.path.dirname(destpath))
    with codecs.open(destpath, 'w', 'utf-8') as w:
        json.dump(data, w)

def get_users(next_cursor=None):
    # this function may fail if the number of following is higher than 3000
    # because of the API limit
    if next_cursor:
        ret = tw.friends.list(count=200, skip_status=True, cursor=next_cursor)
    else:
        ret = tw.friends.list(count=200, skip_status=True)
    
    users = ret['users']
    
    if ret['next_cursor']: # if pages remain, get the next page
        users.extend(get_users(ret['next_cursor']))

    return users

def main():
    cred = tw.account.verify_credentials(
                include_entities=False, skip_satus=False, include_email=False)
    screenname = cred["screen_name"]
    
    users = get_users()
    # dump with filename "<screen_name>_<time>.json"
    strtime = "{:%Y%m%d-%H%M%S}".format(datetime.datetime.now())
    filename = "{}_{}.json".format(screenname, strtime)
    dest = os.path.join(JSONDUMPDIR, filename)
    dumpjson(users, dest)
    print("{} has {} user(s). dumped to {}".format(screenname, len(users), dest))

if __name__ == '__main__':
    main()