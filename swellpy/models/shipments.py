from .base import Base

class Shipments(Base):
    """A shipment represents physical fulfillment of a number of items after an order is placed. 
    
    Shipments contain information about items being fulfilled, and shipping details such as 
    address and tracking number.

    For more information, see: https://developers.swell.is/backend-api/shipments
    """
    
    def __init__(self, swell):
        super().__init__(swell, 'shipments', required_fields=['items', 'order_id'])
        
        self._swell = swell
