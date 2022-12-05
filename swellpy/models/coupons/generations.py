from ..base import Base

class CouponGenerations(Base):
    """
    Coupon generations track the instances for which coupon codes are generated for 
    a particular coupon. 
    
    Each batch of generations is tied to an entry and is stored on the coupon model. 
    
    For more information, see: https://developers.swell.is/backend-api/coupon-generations
    """
    
    def __init__(self, swell):
        super().__init__(swell, 'generations', endpoint='coupons:generations', required_fields=['parent_id', 'count'])
        
        self._swell = swell
