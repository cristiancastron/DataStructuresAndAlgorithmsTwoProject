from enum import Enum

class DeliveryStatus(Enum):
    AT_HUB = 1
    EN_ROUTE = 2
    DELIVERED = 3
    DELAYED_ON_FLIGHT = 4