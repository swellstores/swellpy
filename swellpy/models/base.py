from ..utilities import handle_requests_response
from typing import Optional
from ratelimit import limits, sleep_and_retry

class Base():
    """A set of common, public request methods from which all module-specific classes extend.

    Subclasses may override existing methods or define their own (ie orders.convert_cart_to_order)

    Args:
        Required fields (required): required fields for creating a new instance
        Endpoint: optional parameter to specify API endpoint, otherwise defaults to the model name.

    """

    def __init__(self, swell, name, **kwargs):
        self._swell = swell
        self.name = name
        self.endpoint = kwargs['endpoint'] if 'endpoint' in kwargs else self.name
        self.required_fields = kwargs['required_fields'] if 'required_fields' in kwargs else None
        

    @sleep_and_retry
    # TODO: modify these values and place into a configuration file
    @limits(calls=2, period=1)
    def check_limit(self):
        return

    def list(self, params: Optional[dict] = None) -> dict:
        """Lists all items in the collection

        An object containing query parameters can be passed to filter the collection's results. In addition, 
        'expand' and 'include' parameters can be passed to include linked collections and additional data.

        For more information, see https://developers.swell.is/backend-api/querying/query-parameters

        Args:
            params

        Returns:
            JSON response, including results array and item count.

        """
        self.check_limit()

        response = self._swell._session.get(
            url=f'{self._swell._base_url}/{self.endpoint}', params=params)

        return handle_requests_response(self._swell, response)
        

    def get(self, id: str, params: Optional[dict] = None) -> dict:
        """Retrieve a specific item in a collection

        An id (or slug if available) is passed to retrieve a specific item in a collection.

        Args:
            id (string, required): id of the item in the collection.
            params (optional): additional params (ie expand)

        Returns:
            JSON response for the item

        """

        if not id:
            raise Exception(f"id must be included to get a {self.name}")
        elif not isinstance(id, str):
            raise TypeError("id must be a string")

        self.check_limit()

        response = self._swell._session.get(
            url=f'{self._swell._base_url}/{self.endpoint}/{id}', params=params)

        return handle_requests_response(self._swell, response)

    def create(self, payload: dict) -> dict:
        """Create a new item in the collection

        Args:
            Payload: object containing necessary fields for creating a new item in the collection

        Returns:
            JSON representation of the newly-created item with initiatlized fields
        """

        if not payload:
            raise ValueError("Payload must be provided")

        if self.required_fields:
            for field in self.required_fields:
                if not field in payload:
                    raise ValueError(
                        f"'{field}' must be provided to create a {self.name}")

        self.check_limit()

        response = self._swell._session.post(
            url=f'{self._swell._base_url}/{self.endpoint}/', json=payload)

        return handle_requests_response(self._swell, response)


    def update(self, payload: dict) -> dict:
        """Update a specific item in the collection

        Args:
            id: (string, required) id of the item in the collection to update
            payload: object containing the fields to update

        Returns:
            JSON representation of the updated item

        """

        if not payload or 'id' not in payload:
            raise Exception(f"id must be included for {self.name} update")
        elif not isinstance(payload['id'], str):
            raise TypeError("id must be a string")

        self.check_limit()

        response = self._swell._session.put(
            url=f'{self._swell._base_url}/{self.endpoint}/{payload["id"]}', json=payload)


        return handle_requests_response(self._swell, response)
        

    def delete(self, id: str) -> dict:
        """Delete a specific item in the collection

        Args:
            id: (string, required) id of the item in the collection to delete

        Returns:
            JSON representation of the deleted item
        """

        if not id:
            raise ValueError(f"id must be included for {self.name} deletion")
        elif not isinstance(id, str):
            raise TypeError("id must be a string")

        self.check_limit()

        response = self._swell._session.delete(
            url=f'{self._swell._base_url}/{self.endpoint}/{id}')

        return handle_requests_response(self._swell, response)
