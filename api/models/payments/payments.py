from ..base import Base

class Payments(Base):
    """When a store accepts payment of any kind, a record is kept 
    along with its relation to an order or invoice. 

    For more information, see: https://developers.swell.is/backend-api/payments
    """
    
    def __init__(self, swell):
        super().__init__(swell, 'payments', required_field=['account_id', 'amount', 'method'])
        
        self._swell = swell


