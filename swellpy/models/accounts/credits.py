from ..base import Base

class AccountCredits(Base):
    """
   Account credits are a form of currency that is stored on a customer's account. 
   This balance can be awarded through actions such as refunds, or it can 
   additionally be increased by the redemption of gift cards.
    
    For more information, see: https://developers.swell.is/backend-api/account-credits
    """
    
    def __init__(self, swell):
        super().__init__(swell, 'credits', endpoint='accounts:credits', required_fields=['parent_id', 'amount'])
        
        self._swell = swell
