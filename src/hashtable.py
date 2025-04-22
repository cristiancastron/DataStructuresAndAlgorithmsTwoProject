class HashTable:
    #Initializes size of hashtable
    def __init__(self, initial_size = 50):
        self.initial_size = initial_size
        self.table = []
        for i in range(initial_size):
            self.table.append([])

    #Inserts items into hashtable
    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        bucket_list.append([key, item])
    #Searches for object at key location
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for key_value in bucket_list:
            if key_value[0] == key:
                return key_value[1]
        else:
            return None
    #Removes object at key location
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for key_value in bucket_list:
            if key_value[0] == key:
                bucket_list.remove(key_value)