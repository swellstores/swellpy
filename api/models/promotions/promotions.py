from ..base import Base


class Promotions(Base):
    """Promotions are a way to offer customers a discount without a coupon code, 
    by automatically applying discounts to their cart.

    For more information, see: https://developers.swell.is/backend-api/promotions"""

    def __init__(self, swell):
        super().__init__(swell, 'promotions', required_fields=['discounts', 'name'])

        self._swell = swell
        