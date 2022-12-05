from ..base import Base
from .addresses import AccountAddresses
from .credits import AccountCredits
from .cards import AccountCards

class Accounts(Base):
    """Accounts represent a customer's current information and their interactions with your store.

    Contains the accounts:addresses subclass methods:
        i.e. accounts.addresses.list()
    
    For more information, see: https://developers.swell.is/backend-api/accounts"""
    
    def __init__(self, swell):
        super().__init__(swell, 'accounts', required_fields=['email'])

        self._swell = swell