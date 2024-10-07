"""Cache module for caching data in memory with ttl and like feature."""

import time
import pickle

class Cache():
    """Cache class for caching data in memory with ttl and like feature."""
    def __init__(self):
        self.cache = {}
        self.like = {}
    def get(self, key):
        """Get value from cache by key."""
        if key in self.cache:
            self.cache[key][2] += 1
            if self.cache[key][1] < time.time():
                return None
            return self.cache[key][0]
        return None
    def set(self, key, value, ttl, like):
        """Set value to cache by key."""
        self.cache[key] = [value, time.time() + ttl, 1]
        if like:
            self.like[key] = (value, time.time() + ttl)
    def save(self, filename):
        """Save cache to file."""
        with open(filename, 'wb') as f:
            pickle.dump((self.cache, self.like), f)
    def load(self, filename):
        """Load cache from file."""
        with open(filename, 'rb') as f:
            self.cache, self.like = pickle.load(f)
