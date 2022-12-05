# SwellPy - Headless ecommerce Python API wrapper

## Maintainers:
[Greg Hoskin](mailto:greg@swell.is)

[Mustafa Hoda](mailto:mustafa@swell.is)

## Overview
> This library implements a convenient wrapper for Swell's [Backend API](https://swell.store/docs/api) 
and is authorized with a private key making it ideal for server-side use. 
You should only use the Backend API server-side, and keep your secret keys 
stored as environment variables.

The api-wrapper library is built broad and shallow, meaning the full set of 
Swell API endpoints are available and minimal processing is performed for each. 
In general, you can expect get(), list(), update(), create() and delete() 
methods for each resource. Additional methods (orders.convert_cart_to_order) 
will be documented while unavailable ones will throw an exception (events.delete).

Authentication only needs to be passed once, during initialization. Errors returned
from Swell and missing arguments pased to methods are loudly surfaced and will 
throw an exception. 

In terms of implementation, each resoure extends from the base model, and 
overwrites, adds or disables methods as needed. Only the minimum required fields
are checked and will throw an exception if missing.

Otherwise, a non-opinionated approach is taken to Swell implementation. For example,
it's usually a good idea to generate subscriptions indrectly from orders with 
products containing purchase options. However, subscription plans can also be 
generated directly using the /subscriptions endpoint, which is also included here.
A notable exception are the create/delete operations on events, which are always 
read-only, and have been disabled.


Currently, all responses are python dictionaries generated from requests.json().
This may evolve to return individual classes with advanced processing and methods.


## Getting Setup

1. Import SwellPy
```python
from swellpy import Swell
```

2. Instantiate a new Swell instance:
```python
    swell = Swell({
        store_id: "SWELL_STORE_ID",
        api_key: "SWELL_API_KEY"
    )}
```

3. Request resource
```python
response = swell.products.create({'name': '1234567'})
```

**About Swell**

[Swell](https://www.swell.is) is a customizable, API-first platform for powering 
modern B2C/B2B shopping experiences and marketplaces. Build and connect anything 
using your favorite technologies, and provide admins with an easy to use dashboard.

## Documentation

📖  [**View Swell Backend API Documentation**](https://developers.swell.is/backend-api/introduction)

## Handling log messages

SwellPy uses the standard Logging library to log HTTP requests (DEBUG level).
To capture these logs, a handler can be configured as shown:

```python
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)