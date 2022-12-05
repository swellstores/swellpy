from .base import Base


class Events(Base):
    """Various events are tracked accross Swell. Basic events of .created, 
    .updated, and .deleted that are available regardless of the model 
    (these events are also created for custom models). 
    Additionally, some models also feature events specific to their functionality.
    
    For more information, see: https://developers.swell.is/backend-api/events/the-events-model
    
    For a list of all event types, see: https://developers.swell.is/backend-api/events/event-types"""

    
    def __init__(self, swell):
        super().__init__(swell, 'events')
        
        self._swell = swell

    def create(*args):
        raise NotImplementedError("This method is not supported")

    def update(*args):
        raise NotImplementedError("This method is not supported")

    def delete(*args):
        raise NotImplementedError("This method is not supported")
