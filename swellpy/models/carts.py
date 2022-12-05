from .base import Base

class Carts(Base):
    """
    A cart is a pending request to purchase products from your store. 

    Carts contain all the information needed to fulfill a purchase. 
    Once the customer is ready to complete their purchase, 
    call orders.convert_cart_to_order to convert a cart to an order.
    
    For more information, see: https://developers.swell.is/backend-api/carts"""

    def __init__(self, swell):
        super().__init__(swell, 'carts')
        
        self._swell = swell
