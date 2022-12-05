from .base import Base

class Orders(Base):
    """An order is a request to purchase products from a store.

    Orders contain all the information needed to fulfill a purchase. 
    Usually, customers create a cart to stage a purchase first and see it 
    converted to an order when it's finalized (use orders.convert_cart_to_order). 
    Besides being converted from a cart, it is possible to create an order directly.

    
    For more information, see: https://developers.swell.is/backend-api/orders"""

    def __init__(self, swell):
        super().__init__(swell, 'orders')
        
        self._swell = swell


    def convert_cart_to_order(self, cart_id: str):
        """Converts a cart into an order
        
        Args:
            cart_id: string id of the cart to convert

        Returns:
            JSON of the new order

        Returns an error if any of the required order properties are missing from the cart, 
        or if product stock is unavailable.

        For more info, see: https://developers.swell.is/backend-api/carts/convert-carts-to-orders
        """

        if not cart_id:
            raise ValueError("cart id must be included to convert to an order")
        elif not isinstance(cart_id, str):
            raise TypeError("cart id must be a string")

        response = self._swell._session.post(url=f'{self._swell._base_url}/orders/', params={"cart_id": cart_id})
        
        return response.json()
