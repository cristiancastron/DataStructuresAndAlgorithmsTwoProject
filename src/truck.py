from src.hashtable import HashTable

class Truck:
    def __init__(self, truck_id: int):
        self.truck_id = truck_id
        #number of packages that can be stored
        self.truck_inventory = HashTable(16)
        #travel speed in MPH
        self.travel_speed = 18
        #distance traveled in miles
        self.travel_distance = 0
        #number of packages currently on the truck
        self.num_packages = 0
        #addresses to visit
        self.truck_address_list = []
        #package ID list
        self.package_id_list = []










"""
truck = Truck()
print(truck.truck_inventory.table)
"""