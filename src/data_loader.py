import csv
from package import Package
from hashtable import HashTable

package_data_table = HashTable()
def load_package_data(file_name):
    #Reads through csv file
    with open(file_name) as package_details:
        package_data = csv.reader(package_details, delimiter=',')
        next(package_data)

        for package in package_data:
            package_id = int(package[0])
            address = package[1]
            city = package[2]
            zip_code = package[3]
            deadline = package[4]
            weight = int(package[5])

            package = Package(package_id, address, city, zip_code, deadline, weight)

            package_data_table.insert(package_id, package)
    return package_data_table

distance_data_list = []
def load_distance_data(file_name):
    with open(file_name) as distance_data:
        distance_data = csv.reader(distance_data, delimiter=',')
        next(distance_data)
        for distance in distance_data:
            distance_data_list.append([float(distance[0]), float(distance[1]), float(distance[2]), float(distance[3]), float(distance[4]), float(distance[5]), float(distance[6]), float(distance[7]), float(distance[8]), float(distance[9]), float(distance[10]), float(distance[11]), float(distance[12]), float(distance[13]), float(distance[14]), float(distance[15]), float(distance[16]), float(distance[17]), float(distance[18]), float(distance[19]), float(distance[20]), float(distance[21]), float(distance[22]), float(distance[23]), float(distance[24]), float(distance[25]), float(distance[26]) ])
    return distance_data_list

address_data_list = []
def load_address_data(file_name):
    with open(file_name) as address_data:
        address_data = csv.reader(address_data, delimiter=',')
        next(address_data)
        for address in address_data:
            address_data_list.append(address)
    return address_data_list