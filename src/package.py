from unittest import case

from delivery_status import DeliveryStatus
from package_constraints import PackageConstraint

class Package:
    #Initializes the package
    def __init__(self, package_id: int, address: str, city: str, zip_code: str, deadline, weight: int):
        self.package_id = package_id
        self.address = address
        self.address_index = None
        self.city = city
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.delivery_status = DeliveryStatus.AT_HUB
        self.required_truck_id = 0
        self.package_constraint = PackageConstraint.NO_CONSTRAINT
        self.time_loaded = None
        self.time_delivered = None

    def add_required_truck(self, truck_id):
        self.required_truck_id = truck_id
        self.package_constraint = PackageConstraint.SPECIFIED_TRUCK

    # checks if address from package file is equal to address in csv file
    def compare_addresses(self, csv_address):
        self.address = self.address.strip()
        self.address = self.address.strip('"')

        csv_address = str(csv_address)
        csv_address = csv_address.strip()
        csv_address = csv_address.strip('[]')
        csv_address = csv_address.strip("'")

        if self.address == csv_address:
            return True

    """
    def check_package_constraint(self, input_time):
        input_time = input_time
        match self.package_constraint:
            case PackageConstraint.DELAYED_FLIGHT:
                if input_time >= timedelta(hours=9, minutes=5):
                    if self.time_loaded > input_time:
                        self.delivery_status = DeliveryStatus.AT_HUB
                    elif self.time_loaded <= input_time < self.time_delivered:
                        self.delivery_status = DeliveryStatus.EN_ROUTE
                    elif self.time_delivered >= input_time:
                        self.delivery_status = DeliveryStatus.DELIVERED
                else:
                    self.delivery_status = DeliveryStatus.DELAYED_ON_FLIGHT
                    print('ttest')

            case PackageConstraint.WRONG_ADDRESS:
                if input_time >= timedelta(hours=10, minutes=20):
                    self.address = '410 S State St'
                    self.zip_code = '84111'
                else:
                    self.address = '300 State St'
                    self.zip_code = '84103'
    """

    """
    def check_package_constraint(self, truck, time_tracker):
        truck = truck
        time_tracker = time_tracker
        match self.package_constraint:
            case PackageConstraint.NO_CONSTRAINT:
                return True

            case PackageConstraint.SPECIFIED_TRUCK:
                if self.required_truck_id == truck.truck_id or self.required_truck_id == 0:
                    return True

            #FIXME
            case PackageConstraint.DELAYED_FLIGHT:
                if time_tracker.current_time >= timedelta(hours=9,minutes=5):
                    return True
            #FIXME
            case PackageConstraint.WRONG_ADDRESS:
                if time_tracker.current_time >= timedelta(hours=10,minutes=20):
                    self.address = '410 S State St'
                    self.zip_code = '84111'
                    return True
            #FIXME
            case PackageConstraint.DEPENDENT_PACKAGE:
                return True and print('test')
    """



