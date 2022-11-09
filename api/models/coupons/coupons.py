from ..base import Base
from .generations import CouponGenerations
from .uses import CouponUses

class Coupons(Base):
    """Coupons are a way to offer customers a discount with a coupon code. 
    
    For more information, see: https://developers.swell.is/backend-api/coupons"""
    
    def __init__(self, swell):
        super().__init__(swell, 'coupons', required_fields=['discounts', 'name', 'codes'])

        self._swell = swell
        