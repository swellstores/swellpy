from .base import Base

class Subscriptions(Base):
    """Subscriptions allow you to charge a customer on a recurring basis. 

    A subscription ties a customer to a particular subscription plan. 
    In addition to the plan, subscriptions can have line items that are 
    charged on a recurring basis or just once—depending on the use case.

    For more information, see: https://developers.swell.is/backend-api/subscriptions
    """
    
    def __init__(self, swell):
        super().__init__(swell, 'subscriptions', required_field=['account_id', 'product_id'])
        
        self._swell = swell
