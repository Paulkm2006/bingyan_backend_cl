import time
import pickle

class Cache():
    def __init__(self):
        self.cache = {}
    def get(self, key):
        if key in self.cache:
            if self.cache[key][1] < time.time():
                del self.cache[key]
                return None
            print(f"Cache hit for {key}")
            return self.cache[key][0]
        else:
            return None
    def set(self, key, value, ttl):
        self.cache[key] = (value, time.time() + ttl)
    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.cache, f)
    def load(self, filename):
        with open(filename, 'rb') as f:
            self.cache = pickle.load(f)