from ..base import Base
from .stock import ProductStock
from .variants import ProductVariants

class Products(Base):
    """Products represent items that can be sold to a customer, 
    either as one-off sales or as subscriptions.

    
    For more information, see: https://developers.swell.is/backend-api/products"""

    def __init__(self, swell):
        super().__init__(swell, 'products', required_fields=['name'])
        
        self._swell = swell
        self.stock = ProductStock(swell)
        self.variants = ProductVariants(swell)
