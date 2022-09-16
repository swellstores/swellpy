from ..base import Base

class AccountCards(Base):
    """
    The account cards collection houses a customer's card information used for payments and 
    transactions—allowing for storing multiple cards on a customer account.
    
    For more information, see: https://developers.swell.is/backend-api/account-cards
    """
    
    def __init__(self, swell):
        super().__init__(swell, 'cards', endpoint='accounts:cards', required_fields=['parent_id', 'token'])
        
        self._swell = swell
