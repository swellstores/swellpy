from ..base import Base

class Refunds(Base):
    """To issue a refund, create a refund with the amount and method to return 
    to the customer. 

    A refund can be issued with a different method than the original payment. 
    The total amount refunded can't exceed the total payment amount. 

    For more information, see: https://developers.swell.is/backend-api/refunds/issue-a-refund
    """
    
    def __init__(self, swell):
        super().__init__(swell, 'refunds', endpoint='payments:refunds', required_field=['parent_id', 'amount'])
        
        self._swell = swell



