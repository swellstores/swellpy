from ..base import Base

class Giftcards(Base):
    """Gift cards are a store of value that can be spent on purchases or redeemed for account credit.
    
    For more information, see: https://developers.swell.is/backend-api/gift-cards"""

    def __init__(self, swell):
        super().__init__(swell, 'giftcards', required_fields=['amount'])

        self._swell = swell