from ..base import Base

class Debits(Base):
    """
    Gift card debits keep a record of transactions for which a gift card is used for 
    payment in order to ensure that a gift card balance is updated with each use. 
    
    For more information, see: https://developers.swell.is/backend-api/gift-card-debits
    """
    
    def __init__(self, swell):
        super().__init__(swell, 'debits', endpoint='giftcards:debits', required_fields=['parent_id', 'amount'])
        
        self._swell = swell
