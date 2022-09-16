from ..base import Base

class CouponUses(Base):
    """
    Coupon uses track the instances for which coupon codes are generated for 
    a particular coupon. 
    
    Each batch of uses is tied to an entry and is stored on the coupon model. 
    
    For more information, see: https://developers.swell.is/backend-api/coupon-uses
    """
    
    def __init__(self, swell):
        super().__init__(swell, 'uses', endpoint='coupons:uses', required_fields=['parent_id', 'code', 'code_id'])
        
        self._swell = swell
