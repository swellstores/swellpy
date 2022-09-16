from ..base import Base

class ProductStock(Base):
    """
    Stock adjustments are used to keep track of inventory changes over time.
    
    For more information, see: https://developers.swell.is/backend-api/stock
    """
    
    def __init__(self, swell):
        super().__init__(swell, 'stock', endpoint='products:stock', required_fields=['parent_id', 'quantity', 'message'])
        
        self._swell = swell
