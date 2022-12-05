from .base import Base

class Categories(Base):
    """Categories are used to organize products and can be nested, 
    creating a hierarchy that resembles a tree structure.
    
    For more information, see: https://developers.swell.is/backend-api/categories"""
    
    def __init__(self, swell):
        super().__init__(swell, 'categories', required_fields=['name'])
        
        self._swell = swell
