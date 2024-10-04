import time
import pickle

class Cache():
    def __init__(self):
        self.cache = {}
        self.like = {}
    def get(self, key):
        if key in self.cache:
            self.cache[key][2] += 1
            if self.cache[key][1] < time.time():
                return None
            return self.cache[key][0]
        else:
            return None
    def set(self, key, value, ttl, like):
        self.cache[key] = [value, time.time() + ttl, 1]
        if like:
            self.like[key] = (value, time.time() + ttl)
    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump((self.cache, self.like), f)
    def load(self, filename):
        with open(filename, 'rb') as f:
            self.cache, self.like = pickle.load(f)
