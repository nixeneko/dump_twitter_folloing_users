#!/usr/bin/env python
#coding:utf-8
import codecs
import json
import sys


def get_difference(olderjson, newerjson):
    older = loadjson(olderjson)
    newer = newerjson(newerjson)

class DiffUsers(object):
    def __init__(self, olderjsonpath, newerjsonpath):
        self.older = self._load_idkeyed_dict(olderjsonpath)
        self.newer = self._load_idkeyed_dict(newerjsonpath)
        
    def _load_idkeyed_dict(self, jsonpath):
        users = dict()
        for user in self._loadjson(jsonpath):
            users[ user['id'] ] = user
        return users
        
    def _loadjson(self, path):
        with codecs.open(path, 'r', 'utf-8') as f:
            data = json.load(f)
        return data
        
    def get_newbies(self):
        return self.get_difference_set(self.newer, self.older)
    
    def get_disappeared(self):
        return self.get_difference_set(self.older, self.newer)
    
    def get_difference_set(self, a, b): # a\b
        # a, b are dict, returns list of difference set a\b
        diff = set(a.keys()) - set(b.keys())
        return [a[key] for key in diff]

def main():
    if len(sys.argv) != 3:
        print("Usage: python compare.py <older.json> <newer.json>")
        print("specify two JSON files contianing Twitter user data")
        sys.exit(1)
    
    d = DiffUsers(sys.argv[1], sys.argv[2])
    print("New users:", d.get_newbies())
    print("Disappeared:", d.get_disappeared())
    
if __name__ == '__main__':
    main()