# SwellPy - Headless ecommerce Python API wrapper

## Authors/ Maintainers
[Greg Hoskin](mailto:greg@swell.is)

[Mustafa Hoda](mailto:mustafa@swell.is)


## Overview
> This library implements a convenient wrapper for Swell's [Backend API](https://swell.store/docs/api) 
and is authorized with a private key making it ideal for server-side use. 

All Swell API endpoints and available actions are made available. 
In general, you can expect get(), list(), update(), create() and delete() 
methods for each resource. Additional methods (orders.convert_cart_to_order) 
will be documented while unavailable ones will throw an exception (events.delete).

Authentication only needs to be passed once, during initialization. Errors returned
from Swell are surfaced as log warnings while missing arguments will 
throw an exception. 

In terms of implementation, each resoure extends from a base model, and 
overwrites, adds or disables methods as needed. 

Otherwise, a non-opinionated approach is taken, allowing you to call the Swell API
as needed. For example, it's oftena a good idea to generate subscriptions from orders with 
a product containing that purchase option. However, subscription plans can also be 
generated directly using the /subscriptions endpoint, which is also available.

Rate limiting and caching (LRU) are also included for better performance.

Currently, all responses are python dictionaries generated from requests.json().
This may evolve to return individual classes with advanced processing and methods.



## Getting Setup
1. Clone SwellPy and build locally
```
git clone git@github.com:swellstores/swellpy.git

python -m build
```

2. Install and Import

```
pip install [relative path to swellpy]
```

```python
from swellpy import Swell
```

3. Instantiate a new Swell instance
```python
    swell = Swell({
        store_id: "SWELL_STORE_ID",
        api_key: "SWELL_API_KEY"
    )}
```

4. Request resource
```python
response = swell.products.create({'name': 'my-product-slug'})
print(response) # or setup logging (see below)
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