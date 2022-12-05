from ..base import Base

class ProductVariants(Base):
    """
    Product variants represent unique variations of a product that support stock tracking. 
    
    Each variant is a combination of one or more options, for example, Size or Color.
    
    Note: Normally, variants are automatically created when product options are set.
    
    For more information, see: https://developers.swell.is/backend-api/variants
    """
    
    def __init__(self, swell):
        super().__init__(swell, 'variants', endpoint='products:variants', required_fields=['parent_id', 'name'])
        
        self._swell = swell
