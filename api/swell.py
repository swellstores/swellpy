import requests
import logging

from requests_toolbelt import sessions

from .models.products import Products
from .models.accounts import Accounts
from .models.carts import Carts
from .models.orders import Orders
from .models.coupons import Coupons
from .models.promotions import Promotions
from .models.giftcards import Giftcards
from .models.categories import Categories
from .models.attributes import Attributes
from .models.purchase_links import PurchaseLinks
from .models.invoices import Invoices
from .models.events import Events
from .models.subscriptions import Subscriptions
from .models.payments import Payments
from .models.returns import Returns
from .models.shipments import Shipments
from .models.webhooks import Webhooks

class Swell:
    """
    The Swell class provides convenient access to Swell's API

    To instantiate a new instance, call:

    swellpy.Swell({
        store_id= "SWELL_STORE_ID",
        api_key= "SWELL_API_KEY"
    )}
    """

    def __init__(
        self,
        params
    ):
        """
        Initialize a Swell class instance
        """
        store_id = params['store_id']
        api_key = params['api_key']

        class APIKeyMissingError(Exception):
            pass

        if store_id is None or api_key is None:
            raise APIKeyMissingError(
                "All Swell API methods require a store id and API key."
                "See https://developers.swell.is/backend-api/authentication"
                "for how to retrieve an API key from Swell"
        )

        s = sessions.BaseUrlSession(base_url=f'https://{store_id}:{api_key}@api.swell.store')
        self._base_url = s.base_url

        session = requests.Session()
        session.auth = (store_id, api_key)
        self._session = session

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.NullHandler())


        self.products = Products(self)
        self.accounts = Accounts(self)
        self.carts = Carts(self)
        self.orders = Orders(self)
        self.coupons = Coupons(self)
        self.promotions = Promotions(self)
        self.giftcards = Giftcards(self) 
        self.categories = Categories(self)
        self.attributes = Attributes(self)
        self.purchase_links = PurchaseLinks(self)
        self.invoices = Invoices(self)
        self.events = Events(self)
        self.subscriptions = Subscriptions(self)
        self.payments = Payments(self)
        self.returns = Returns(self)
        self.shipments = Shipments(self)
        self.webhooks = Webhooks(self)