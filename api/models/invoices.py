from .base import Base

class Invoices(Base):
    """Invoices are created automatically when a subscription is charged. 
    
    An invoice captures the billing period of a subscription, including the 
    subscription plan and line items prices. Payments are applied directly to an invoice.

    For more information, see: https://developers.swell.is/backend-api/invoices
    """
    
    def __init__(self, swell):
        super().__init__(swell, 'invoices')
        
        self._swell = swell
