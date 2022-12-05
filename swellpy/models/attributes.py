from .base import Base

class Attributes(Base):
    """Product attributes are additional characteristics of a product that can be used in different ways.

    For more information, see: https://developers.swell.is/backend-api/attributes
    """
    
    def __init__(self, swell):
        super().__init__(swell, 'attributes', required_fields=['name'])
        
        self._swell = swell
