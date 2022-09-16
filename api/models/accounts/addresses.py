from ..base import Base

class AccountAddresses(Base):
    """
    The account addresses collection is stored on the account model. 
    It houses a customer's address information and supports several entries 
    which can be used for shipping and billing purposes.
    
    For more information, see: https://developers.swell.is/backend-api/account-addresses
    """
    
    def __init__(self, swell):
        super().__init__(swell, 'addresses', endpoint='accounts:addresses', required_fields=['parent_id', 'address1'])
        
        self._swell = swell
