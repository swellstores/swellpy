# SwellPy - Headless ecommerce Python API wrapper

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

## Prerequisites

1. Install [pyenv](https://github.com/pyenv/pyenv#installation)

## Getting Setup

1. Clone SwellPy and build the project
```bash
git clone git@github.com:swellstores/swellpy.git
cd swellpy
pyenv install -s

pip3 install -r requirements.txt
python3 -m build
```

2. Install and import the package locally

```bash
pip3 install dist/swellpy-0.0.1.tar.gz
```

## Initialization Options
When creating a Swell instance, you can pass initialization options for the
desired amount of rate limiting (by # of calls and period)

```python
from swellpy import Swell

swell = Swell({
  "store_id": "SWELL_STORE_ID",
  "api_key": "SWELL_API_KEY",
  "options": {
    "rate_limit_calls": 2,
    "rate_limit_period": 1,
  },
})
```

### List

```python
query = {
  "date_created": {
    "$gte": "2022-09-25T00:00:00.000Z"
  },
  "expand": ["items.product", "shipments:100"],
}
response = swell.orders.list(query)
print(response)
```

### Create

```python
data = {
  "name": "T-Shirt",
  "price": 99.00,
  "active": True,
  "options": [
    {
      "name": "Size",
      "values": [
        { "name": "Small" },
        { "name": "Large" },
      ],
    },
  ],
}
response = swell.products.create(data)
print(response)
```

## Logging

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
```

## Documentation

📖  [**View Swell Backend API Documentation**](https://developers.swell.is/backend-api/introduction)

**About Swell**

[Swell](https://www.swell.is) is a customizable, API-first platform for powering
modern B2C/B2B shopping experiences and marketplaces. Build and connect anything
using your favorite technologies, and provide admins with an easy to use dashboard.
