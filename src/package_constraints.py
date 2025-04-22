from delivery_status import DeliveryStatus
from enum import Enum

#Specifies the constraint for the package
class PackageConstraint(Enum):
    NO_CONSTRAINT = 0
    SPECIFIED_TRUCK = 1
    DELAYED_FLIGHT = 2
    WRONG_ADDRESS = 3
    DEPENDENT_PACKAGE = 4