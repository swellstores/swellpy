from ..base import Base

class PromotionUses(Base):
    """
    Promotion uses track the instances for which promotion codes are generated for 
    a particular promotion. 
    
    Each batch of uses is tied to an entry and is stored on the promotion model. 
    
    For more information, see: https://developers.swell.is/backend-api/promotion-uses
    """
    
    def __init__(self, swell):
        super().__init__(swell, 'uses', endpoint='promotions:uses', required_fields=['parent_id'])
        
        self._swell = swell
