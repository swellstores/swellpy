from .base import Base

class Returns(Base):
    """A return is requested in order to return a product(s) previously purchased by a customer.

    They contain information about returning items that were previously fulfilled, the return 
    shipment details if applicable, and return value to apply to an order, which in turn may 
    prompt an administrator to issue a refund.

    For more information, see: https://developers.swell.is/backend-api/returns
    """
    
    def __init__(self, swell):
        super().__init__(swell, 'returns', required_fields=['items', 'order_id'])
        
        self._swell = swell
