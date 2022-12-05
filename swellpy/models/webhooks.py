from .base import Base
from typing import Optional
class Webhooks(Base):
    """Use webhooks to get notified about events that happen in your Swell account. 
    
    Configuring a webhook involves setting up your own application to receive 
    incoming HTTP calls that contain data describing the event.

    For more information, see: https://developers.swell.is/backend-api/webhooks
    """
    
    def __init__(self, swell):
        super().__init__(swell, 'webhooks', endpoint=":webhooks", required_field=['url', 'events'])
        
        self._swell = swell

    def list_events(self, params: Optional[dict] = None):
        """List events related to webhook activity
        
        Args:
            params: filter based on provided parameters

        Returns:
            List of webhook events


        For more info, see: https://developers.swell.is/backend-api/webhooks/receiving-webhooks
        """

        response = self._swell._session.get(url=f'{self._swell._base_url}/events:webhooks/', params=params)
        
        return response.json()
