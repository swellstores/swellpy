from .base import Base

class PurchaseLinks(Base):
    """Purchase links allow you to configure a pre-selected group of products within a cart 
    and direct a customer to its checkout through a designated URL

    For more information, see: https://developers.swell.is/backend-api/purchase-links"""

    def __init__(self, swell):
        super().__init__(swell, 'purchase links', endpoint='purchaselinks', required_fields=['name'])
        
        self._swell = swell
