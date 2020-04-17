import time
import threading

# Node class for the double linked list
class Node(): 
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
        self.creation_time = time.time()

# class for LRU Cache
# The implementation of this cache is composed of a hashmap and a double linked list
# to have insert(), get(), delete() at a complexity of O(1).
# The hashmap connects the key to a Node, while the double linked list keeps the list of 
# input based on their usage frequency. The head Node has the least recent key, and the
# tail Node has the most recent used key. So the head Node will be erased if a full-capacity   
# cache accepts a new value
# Every node has a parameter that stores their creation time. This time is used to verify
# if it is expired. The expire() function is run periodically in a thread to remove 
# expired keys. 

# When initializing the GeoLRUCache object, 'capacity' indicates the max capacity of the 
# cache and 'timeout' indicates the expiration time for all inputs
class GeoLRUCache(object):
    def __init__(self, capacity, timeout):
        self.head = None
        self.tail = None
        self.cache = dict()
        self.capacity = capacity
        self.threadlock = threading.RLock()
        self.timeout = timeout
        self.timer = None

        if self.timeout:
            self.clean()
    
    # insert a key-value pair into the cache
    # or update a key-value pair
    def insert(self, key, value):
        try:
            self.threadlock.acquire()
            
            if key in self.cache:
                node = self.cache[key]
                node.value = value

                self.removeNode(node)
                node.creation_time = time.time()
                self.offerNode(node)

            else:
                if len(self.cache) == self.capacity:
                    del self.cache[self.head.key]
                    self.removeNode(self.head)

                newNode = Node(key, value)
                self.offerNode(newNode)
                self.cache[key] = newNode

        finally:
            self.threadlock.release()
    
    # return the value for a specific key
    def get(self, key):
        try:
            self.threadlock.acquire()

            if key not in self.cache:
                return -1

            node = self.cache[key]

            self.removeNode(node)
            node.creation_time = time.time()
            self.offerNode(node)

            return node.value

        finally:
            self.threadlock.release()

    # delete a specific key-value pair
    def delete(self, key):
        try:
            self.threadlock.acquire()

            if key not in self.cache:
                return -1

            node = self.cache[key]
            self.removeNode(node)

        finally:
            self.threadlock.release()

    # remove a node from the double linked list
    def removeNode(self, node):
        if (node.prev != None):
            node.prev.next = node.next
        else:
            self.head = node.next

        if (node.next != None):
            node.next.prev = node.prev
        else:
            self.tail = node.prev

    # add a node in the double linked list
    def offerNode(self, node):
        if (self.tail != None):
            self.tail.next = node

        node.prev = self.tail
        node.next = None
        self.tail = node

        if (self.head == None):
            self.head = self.tail

    # functions to remove expired keys
    def expire(self):
        if len(self.cache) == 0:
            return

        try:
            self.threadlock.acquire()
            
            while self.tail and time.time() - self.tail.creation_time > self.timeout:
                tailnode = self.cache[self.tail.key]
                del self.cache[self.tail.key]
                self.removeNode(tailnode)
                
        finally:
            self.threadlock.release()

    def clean(self):
        self.expire()
        timer = threading.Timer(self.timeout, self.clean)
        timer.start()
        self.timer = timer
