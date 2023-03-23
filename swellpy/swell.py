import requests
import logging

from requests_toolbelt import sessions

from .models.products import Products
from .models.products.stock import ProductStock
from .models.products.variants import ProductVariants
from .models.accounts import Accounts
from .models.accounts.addresses import AccountAddresses
from .models.accounts.cards import AccountCards
from .models.accounts.credits import AccountCredits
from .models.carts import Carts
from .models.orders import Orders
from .models.coupons import Coupons
from .models.coupons.uses import CouponUses
from .models.coupons.generations import CouponGenerations
from .models.promotions import Promotions
from .models.promotions.uses import PromotionUses
from .models.giftcards import Giftcards
from .models.giftcards.debits import Debits
from .models.categories import Categories
from .models.attributes import Attributes
from .models.purchase_links import PurchaseLinks
from .models.invoices import Invoices
from .models.events import Events
from .models.subscriptions import Subscriptions
from .models.payments import Payments
from .models.payments.refunds import Refunds
from .models.returns import Returns
from .models.shipments import Shipments
from .models.webhooks import Webhooks


class Swell:
    """
    The Swell class provides convenient access to Swell's API

    """

    def __init__(
        self,
        params  # TODO: Add type hinting here
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

        s = sessions.BaseUrlSession(
            base_url=f'https://{store_id}:{api_key}@api.swell.store')
        self._base_url = s.base_url

        session = requests.Session()
        session.auth = (store_id, api_key)
        self._session = session
        self.rate_limit_calls = 1
        self.rate_limit_period = 1

        if ("options" in params):
            options = params["options"]
            if ("rate_limit_calls" in options):
                self.rate_limit_calls = options["rate_limit_calls"]
            if ("rate_limit_period" in options):
                self.rate_limit_period = options["rate_limit_period"]

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.NullHandler())


        self.accounts = Accounts(self)
        self.attributes = Attributes(self)
        self.addresses = AccountAddresses(self)
        self.cards = AccountCards(self)
        self.carts = Carts(self)
        self.categories = Categories(self)
        self.coupons = Coupons(self)
        self.coupon_generations = CouponGenerations(self)
        self.coupon_uses = CouponUses(self)
        self.credits = AccountCredits(self)
        self.debits = Debits(self)
        self.events = Events(self)
        self.giftcards = Giftcards(self) 
        self.invoices = Invoices(self)
        self.orders = Orders(self)
        self.payments = Payments(self)
        self.products = Products(self)
        self.promotions = Promotions(self)
        self.promotion_uses = PromotionUses(self)
        self.purchase_links = PurchaseLinks(self)
        self.refunds = Refunds(self)
        self.returns = Returns(self)
        self.shipments = Shipments(self)
        self.stock = ProductStock(self)
        self.subscriptions = Subscriptions(self)
        self.variants = ProductVariants(self)
        self.webhooks = Webhooks(self)
