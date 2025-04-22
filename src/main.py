#NAME: CRISTIAN CASTRONUEVO STUDENT ID: 001366761 PYTHON VERSION: 3.13
from datetime import timedelta, datetime

from src import truck
from src.data_loader import load_package_data, load_distance_data, load_address_data
from src.delivery_status import DeliveryStatus
from src.truck import Truck
from src.package_constraints import PackageConstraint
from src.time_tracker import TimeTracker

#Loads in data from CSV files
package_table = load_package_data('PackageDetails.csv')
distance_matrix = load_distance_data('DistanceData.csv')
address_list = load_address_data('AddressData.csv')

time_tracker = TimeTracker()

#sets truck objects
truck1 = Truck(1)
truck2 = Truck(2)

#Adds required truck constraint
package3 = package_table.search(3)
package3.add_required_truck(truck2.truck_id)
package18 = package_table.search(18)
package18.add_required_truck(truck2.truck_id)
package36 = package_table.search(36)
package36.add_required_truck(truck2.truck_id)
package38 = package_table.search(38)
package38.add_required_truck(truck2.truck_id)

#Adds delayed flight constraint
package6 = package_table.search(6)
package6.delivery_status = DeliveryStatus.DELAYED_ON_FLIGHT
package6.package_constraint = PackageConstraint.DELAYED_FLIGHT
package25 = package_table.search(25)
package25.package_constraint = PackageConstraint.DELAYED_FLIGHT
package25.delivery_status = DeliveryStatus.DELAYED_ON_FLIGHT
package28 = package_table.search(28)
package28.delivery_status = DeliveryStatus.DELAYED_ON_FLIGHT
package28.package_constraint = PackageConstraint.DELAYED_FLIGHT
package32 = package_table.search(32)
package32.delivery_status = DeliveryStatus.DELAYED_ON_FLIGHT
package32.package_constraint = PackageConstraint.DELAYED_FLIGHT

package9 = package_table.search(9)
package9.package_constraint = PackageConstraint.WRONG_ADDRESS

#Sets package address index for package objects to access address data csv
for i in range(package_table.initial_size):
    if package_table.search(i) is not None:
        package = package_table.search(i)
        for j in range(len(address_list)):
            if package.compare_addresses(address_list[j]):
                package.address_index = j

#Groups together all the packages that must be delivered together
dependent_packages = [package_table.search(13), package_table.search(14), package_table.search(15), package_table.search(16), package_table.search(19), package_table.search(20)]
for i in range(len(dependent_packages)):
    package = dependent_packages[i]
    package.package_constraint = PackageConstraint.DEPENDENT_PACKAGE

#Function that returns the distance between two addresses
def find_distance(address1, address2):
    address1_index = address_list.index(address1)
    address2_index = address_list.index(address2)
    distance = distance_matrix[address1_index][address2_index]
    return distance

#finds nearest address to current address in truck
def find_nearest_truck_address(address, truck):
    current_address = address
    truck = truck
    nearest_truck_address = truck.truck_address_list[0]
    if current_address is nearest_truck_address:
        nearest_truck_address = truck.truck_address_list[1]
    for i in range(truck.num_packages - 1):
        next_address = truck.truck_address_list[i]
        distance1 = find_distance(current_address, next_address)
        distance2 = find_distance(current_address, nearest_truck_address)
        if distance1 <= distance2 and next_address is not current_address:
            nearest_truck_address = next_address
    return nearest_truck_address

#Delivers all packages on given truck
def deliver_truck_packages(truck):
    truck = truck
    starting_address = address_list[0]
    nearest_address = find_nearest_truck_address(starting_address, truck)
    current_distance = find_distance(starting_address, nearest_address)
    truck.travel_distance += find_distance(starting_address, nearest_address)

    #Sets the delivery status to en route for packages on the current truck
    for i in range(package_table.initial_size):
        if truck.truck_inventory.search(i) is not None:
            truck_package = truck.truck_inventory.search(i)
            truck_package.delivery_status = DeliveryStatus.EN_ROUTE
    i = 0
    while truck.num_packages > 0 and truck.truck_address_list is not None:
        if truck.truck_inventory.search(i) is not None:
            package = truck.truck_inventory.search(i)
            if package.compare_addresses(nearest_address):

                #updates time
                time_to_deliver = timedelta(hours = current_distance / truck.travel_speed)
                time_tracker.current_time += time_to_deliver
                #print('truck id', truck.truck_id, 'time loaded', package.time_loaded, 'time to deliver:', time_to_deliver, 'current time', time_tracker.current_time, 'package deadline', package.deadline, 'package ID', package.package_id, 'address', package.address, 'Constraint', package.package_constraint)

                #Updates delivery status and time delivered for the current package
                package.delivery_status = DeliveryStatus.DELIVERED
                package.time_delivered = time_tracker.current_time
                truck.num_packages -= 1

                current_address = address_list[package.address_index]

                #delivers all packages that share the same address
                for j in range(truck.num_packages):
                    if truck.truck_inventory.search(truck.package_id_list[j]) is not None:
                        package2 = truck.truck_inventory.search(truck.package_id_list[j])
                        if package2.compare_addresses(current_address) and package2.package_id != package.package_id:
                            package2.delivery_status = DeliveryStatus.DELIVERED
                            package2.time_delivered = time_tracker.current_time
                            truck.num_packages -= 1
                            #print('truck id', truck.truck_id, 'time loaded', package2.time_loaded, 'time to deliver:', time_to_deliver, 'current time', time_tracker.current_time, 'package deadline', package2.deadline, 'package ID', package2.package_id, 'address', package2.address, 'Constraint', package.package_constraint)
                            truck.truck_address_list.remove(current_address)
                            truck.truck_inventory.remove(package2.package_id)

                #Sets the next delivery location
                if len(truck.truck_address_list) > 1:
                    nearest_address = find_nearest_truck_address(current_address, truck)

                #Updates the travel distance of the current truck
                truck.travel_distance += find_distance(current_address, nearest_address)

                current_distance = find_distance(current_address, nearest_address)

                truck.truck_address_list.remove(current_address)
                truck.truck_inventory.remove(package.package_id)

        if i >= package_table.initial_size:
            i = 0
        i += 1
    truck.package_id_list.clear()
    #Adds the distance from the last stop to the hub (returns the truck to the hub)
    truck.travel_distance += find_distance(current_address, address_list[0])
    return truck

#Loads packages onto a truck given a manually made load list
def load_truck_packages(truck, load_list):
    truck = truck
    load_list = load_list
    for i in load_list:
        if package_table.search(i) is not None:
            package = package_table.search(i)

            package.time_loaded = time_tracker.current_time
            package.required_truck_id = truck.truck_id
            truck.num_packages += 1
            truck.truck_address_list.append(address_list[package.address_index])
            truck.truck_inventory.insert(package.package_id, package)
            truck.package_id_list.append(package.package_id)
    return truck

#list of packages to be loaded
load_list1 = [1,13,14,15,16,19,20,29,30,31,34,37,40]
load_list2 = [3,6,7,8,10,11,12,17,18,23,25,28,32]
load_list3 = [2,4,5,9,21,22,24,26,27,33,35,36,38,39]

#loading and delivering the packages
truck1 = load_truck_packages(truck1, load_list1)
truck1 = deliver_truck_packages(truck1)
package9.address = '410 S State St'
package9.zip_code = '84111'
package9.address_index = 19
truck2 = load_truck_packages(truck2, load_list2)
truck2 = deliver_truck_packages(truck2)
truck2 = load_truck_packages(truck2, load_list3)
truck2 = deliver_truck_packages(truck2)

#USER INTERFACE
run_program = True

#Main menu of the program
def main_menu(run_program):
    print('Input the number associated with the action and press enter')
    print('[1] Check delivery status of all packages at a specified time')
    print('[2] Check Total Mileage of trucks')
    print('[3] Exit Program')
    user_input = input()
    match user_input:
        case '1':
            specify_time()
        case '2':
            output_total_mileage()
        case '3':
            run_program = False
            print('Program Terminated')
            return run_program
        case _:
            print('Invalid input')

#Outputs total mileage traveled by both trucks
def output_total_mileage():
    run_program = True
    print('Total distance traveled by both trucks:', truck1.travel_distance + truck2.travel_distance, 'miles')
    print('[1] Return to Menu')
    print('[2] Exit Program')
    user_input = input()
    match user_input:
        case '1':
            main_menu(run_program)
        case '2':
            print('Program Terminated')

#Gets inputted time from user that is used to find package info
def specify_time():
    print('Specify the time to be checked. Example: 09:25 AM')
    time_input = input('Enter the time in HH:MM AM/PM format \n')
    try:
        #Converts input time to timedelta object
        time_object = datetime.strptime(time_input, '%I:%M %p').time()
        datetime_obj = datetime.combine(datetime.min.date(), time_object)
        deltatime_obj = datetime_obj - datetime.min

        output_package_info(deltatime_obj)

    except ValueError:
        print('Invalid time. Please enter HH:MM AM/PM format')
        specify_time()

#Outputs the package info to the CLI
def output_package_info(deltatime_obj):
    deltatime_obj = deltatime_obj

    for i in range(package_table.initial_size):
        if package_table.search(i) is not None:
            package = package_table.search(i)
            #Handles wrong address for output
            if package.package_constraint.value == PackageConstraint.WRONG_ADDRESS.value:
                if deltatime_obj >= timedelta(hours=10, minutes=20):
                    package.address = '410 S State St'
                    package.zip_code = '84111'
                else:
                    package.address = '300 State St'
                    package.zip_code = '84103'

            #Finds the delivery status of the package (at hub, en route, delivered)
            if package.time_loaded > deltatime_obj:
                package.delivery_status = DeliveryStatus.AT_HUB

                if package.package_constraint.value == PackageConstraint.DELAYED_FLIGHT.value:
                    if deltatime_obj >= timedelta(hours=9, minutes=5):
                        package.delivery_status = DeliveryStatus.AT_HUB
                    else:
                        package.delivery_status = DeliveryStatus.DELAYED_ON_FLIGHT

            elif package.time_loaded <= deltatime_obj < package.time_delivered:
                package.delivery_status = DeliveryStatus.EN_ROUTE
            elif package.time_loaded < deltatime_obj >= package.time_delivered:
                package.delivery_status = DeliveryStatus.DELIVERED

            #Finds the delivery time and formats it for output
            if package.delivery_status.value == DeliveryStatus.DELIVERED.value:
                reference_time = datetime(2024, 1, 1, 0, 0, 0)  # Midnight
                delivered_time = reference_time + package.time_delivered
                formatted_time = delivered_time.strftime("%I:%M %p")
                print('Package ID:', package.package_id,'Delivery Address:', package.address, 'Delivery Status:', package.delivery_status.name, 'Delivery Deadline:', package.deadline, 'Package Constraint:', package.package_constraint.name, 'Truck Number:', package.required_truck_id, 'Time Delivered:', formatted_time)
            #Outputs the packages that havent been delivered yet and are en route
            elif package.delivery_status.value == DeliveryStatus.EN_ROUTE.value:
                print('Package ID:', package.package_id, 'Delivery Address', package.address, 'Delivery Status:', package.delivery_status.name, 'Delivery Deadline:', package.deadline, 'Package Constraint:', package.package_constraint.name, 'Truck Number:', package.required_truck_id)
            #Outputs the rest of the packages that are at hub or delayed on flight
            else:
                print('Package ID:', package.package_id, 'Delivery Address', package.address, 'Delivery Status:', package.delivery_status.name, 'Delivery Deadline:', package.deadline, 'Package Constraint:', package.package_constraint.name)

#Runs the program
while run_program is True:
    run_program = main_menu(run_program)

"""
#USER INTERFACE
run_program = True
user_input = None
time_input = None
truck_input = None

print('Input the number next to the action')
print('[1] Check delivery status of all packages on a specified truck at a specified time')
print('[2] Exit Program')
while run_program:
    user_input = input()
    match user_input:
        case '1':
            print('Specify the truck to be checked')
            print('[1] Truck 1')
            print('[2] Truck 2')
            user_input = input()
            if user_input == '1':
                truck = truck1
                print('Specify the time to be checked. Example: 09:25 AM')
                time_input = input('Enter the time in HH:MM AM/PM format \n')
                try:
                    time_object = datetime.strptime(time_input, '%H:%M %p').time()
                    print(time_object)

                except ValueError:
                    print('Invalid time. Please enter HH:MM AM/PM format')
                    
            elif user_input == '2':
                truck = truck2
            else:
                print('Invalid Input')
        case '2':
            run_program = False
            print('Program Terminated')

        case _:
            print('Invalid Input')
            print('Input the number next to the action')
            print('\n')
            print('[1] Check delivery status of all packages on a specified truck at a specified time')
            print('[2] Exit Program')
"""

#FIXME NEEDS TO BE ABLE TO RUN WITHOUT A FULL LOAD
"""
#ORIGINAL LOAD TRUCK FUNCTION
def load_truck_packages(truck_id):
    truck = Truck(truck_id)
    starting_address = address_list[0]
    i = 0
    while truck.num_packages < truck.truck_inventory.initial_size:
        if package_table.search(i) is not None:
            package = package_table.search(i)
            print(package.package_constraint, package.package_constraint.value, 'id:', package.package_id, 'NOT LOADED', time_tracker.current_time, package.check_package_constraint(truck, time_tracker.current_time))
            if package.delivery_status.value == DeliveryStatus.AT_HUB.value and package.check_package_constraint(truck, time_tracker.current_time):

                if package.package_constraint.value is PackageConstraint.DEPENDENT_PACKAGE.value:
                    print('TESTING DEPENDENT PACKAGE')

                truck.truck_inventory.insert(package.package_id, package)
                truck.truck_address_list.append(address_list[package.address_index])
                truck.num_packages += 1
                print(package.package_constraint, 'id:', package.package_id,'LOADED ON TRUCK')

        i += 1
    return truck
"""

"""
package_test = package_table.search(14)
print(package_test.package_constraint)
if package_test.package_constraint.value is PackageConstraint.DEPENDENT_PACKAGE.value:
    print('TEST DEPENDENT PACKAGE')
"""

"""
#FIXME TESTING LOADING AND DELIVERY FOR TRUCKS
truck1 = load_truck_packages(truck1.truck_id)
truck2 = load_truck_packages(truck2.truck_id)

truck1 = deliver_truck_packages(truck1)

truck2 = deliver_truck_packages(truck2)
print(truck1.travel_distance)
#print(truck2.travel_distance)
print(time_tracker.current_time)
"""

"""
#TESTS LOAD TRUCK FUNCTION FOR TRUCK 1
truck1 = load_truck_packages(truck1.truck_id)

for i in range(package_table.initial_size):
    if truck1.truck_inventory.search(i) is not None:
        package = truck1.truck_inventory.search(i)
        print('ID:', package.package_id, 'Address:', package.address, 'City:', package.city, 'Zip:', package.zip_code, 'Deadline:', package.deadline, 'Weight:', package.weight, 'Delivery Status:', package.delivery_status, 'Truck ID:', package.required_truck_id, 'Constraint:', package.package_constraint)

#print(truck1.truck_address_list)

#nearest_address = find_nearest_truck_address(truck1.truck_address_list[0], truck1)
#(truck1.truck_address_list[1])
#print(nearest_address)
#print(find_distance(truck1.truck_address_list[1], nearest_address))
"""

"""
#TESTS LOAD TRUCK FUNCTION FOR TRUCK 2
truck2 = load_truck_packages(truck2.truck_id)

for i in range(package_table.initial_size):
    if truck2.truck_inventory.search(i) is not None:
        package = truck2.truck_inventory.search(i)
        print('ID:', package.package_id, 'Address:', package.address, 'City:', package.city, 'Zip:', package.zip_code, 'Deadline:', package.deadline, 'Weight:', package.weight, 'Delivery Status:', package.delivery_status, 'Truck ID:', package.required_truck_id, 'Constraint:', package.package_constraint)
truck1 = deliver_truck_packages(truck1)
print('truck1  first delivery done')
truck2 = deliver_truck_packages(truck2)
print('truck2  first delivery done')

print('truck1 distance traveled', truck1.travel_distance, 'truck2 distance traveled', truck2.travel_distance)

truck1 = load_truck_packages(truck1.truck_id)
for i in range(package_table.initial_size):
    if truck1.truck_inventory.search(i) is not None:
        package = truck1.truck_inventory.search(i)
        print('ID:', package.package_id, 'Address:', package.address, 'City:', package.city, 'Zip:', package.zip_code, 'Deadline:', package.deadline, 'Weight:', package.weight, 'Delivery Status:', package.delivery_status, 'Truck ID:', package.required_truck_id, 'Constraint:', package.package_constraint)
"""

"""
#TESTING NEAREST ADDRESS FUNCTION
close_address_test = find_nearest_address(address_list[26])
print(close_address_test)
"""

"""
#TESTS COMPARE ADDRESSES FUNCTION
package_test = package_table.search(22)
print(package_test.compare_addresses(address_list[26]))
print(package_test.address)
"""

"""
TESTING ADDRESS LIST
for i in range(len(address_list)):
    print(address_list[i])
"""

"""
TESTING DISTANCE MATRIX
for i in range(len(distance_matrix)):
    print(distance_matrix[i])
"""

"""
TESTING TRUCK INVENTORY TABLE
for i in range(16):
    if package_table.search(i) is not None:
        package = package_table.search(i)
        truck1.truck_inventory.insert(package.package_id, package)
for i in range(16):
    if truck1.truck_inventory.search(i) is not None:
        package = truck1.truck_inventory.search(i)
        print('ID:', package.package_id, 'Address:', package.address, 'City:', package.city, 'Zip:', package.zip_code, 'Deadline:', package.deadline, 'Weight:', package.weight, 'Delivery Status:', package.delivery_status)
"""

"""
#TESTING PACKAGE TABLE
for i in range(42):
    if package_table.search(i) is not None:
        #if package.delivery_status.value != DeliveryStatus.DELIVERED.value:
        package = package_table.search(i)
        if package.delivery_status.value == DeliveryStatus.DELIVERED.value:
            print('ID:', package.package_id, 'Address:', package.address, 'City:', package.city, 'Zip:', package.zip_code, 'Deadline:', package.deadline, 'Weight:', package.weight, 'Delivery Status:', package.delivery_status, 'Time Delivered:', package.time_delivered, 'Required Truck:', package.required_truck_id)
"""

"""
#TESTING PACKAGE OBJECT
package = Package(1 ,'12415 22nd ave se', '10:30 AM', 'Everett', '98208', 45)
test_table = HashTable()
test_table.insert(package.package_id, package)
print(test_table.search(package.package_id))

print(package.address)
print(package.deadline)
print(package.city)
print(package.zip_code)
print(package.weight)
print(f'{package.delivery_status.name}')
package.delivery_status = DeliveryStatus.EN_ROUTE
print(f'{package.delivery_status.name}')
"""