#!/usr/bin/env python
# -*- coding: utf-8 -*-
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.tm = 0
        self.cache = {}
        self.lru = {}

    def get(self, key):
        if key in self.cache:
            self.lru[key] = self.tm
            self.tm += 1
            return self.cache[key]
        return None

    def set(self, key, value):
        if len(self.cache) >= self.capacity:
            # find the LRU entry
            old_key = min(self.lru.keys(), key=lambda k:self.lru[k])
            self.cache.pop(old_key)
            self.lru.pop(old_key)

        self.cache[key] = value
        self.lru[key] = self.tm
        self.tm += 1

    def remove(self, key):
        if key in self.cache.keys():
            del self.cache[key]
            self.lru[key] = self.tm
            self.tm += 1

    
if __name__ == "__main__":
    c = LRUCache(10)
    d = c.get("ckey")
    print d
    c.set('ckey',111)
    d = c.get("ckey")
    print d
    c.remove("ckey")
    d = c.get("ckey")
    print d