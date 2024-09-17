## Getting Started

### Installation

1. Install package
    ```sh
    pip install django-gajo-utils
    ```

2. Add `GajoDebugUtilsMiddleware` to project settings before all other
   none-dev related middlewares.
    ```python
    MIDDLEWARE = [
        'gajo_utils.middleware.GajoDebugUtilsMiddleware',
        ...
    ]
    ```
3. Turn on any of the utils by settings its value to `True` (by
   default all utils are disabled)
    ```python
    GAJO_UTILS_CONFIG = {
        "REQUEST_TIMER": False,
        "REQUEST_DELAY": False,
        "REQUEST_COOKIES": False,
        "RESPONSE_COOKIES": False,
        "RESPONSE_CONTENT": False,
        "RESPONSE_QUERIES": False,
    }
    ```

## Usage

### Configuration

`"REQUEST_TIMER": True` prints in terminal how much time it needed
for request/response cycle to finish.

`"REQUEST_DELAY": True` adds random delay (50ms - 300ms) to every
request and than prints in terminal how much was request delayed. This
config is used to simulate latency on server.

`"REQUEST_COOKIES": True` prints in terminal request cookies.

`"RESPONSE_COOKIES": True` prints in terminal response cookies.

`"RESPONSE_CONTENT": True` prints in terminal response content.

`"RESPONSE_QUERIES": True` prints all queries that were made in
response/request cycle with time for each one. It also prints total
time for all queries and number of similar queries (queries that can
be probably optimized with `select_related` or `prefetch_related`).

### Decorators

Decorator for timing how much time took for view to run. If you want
to time whole request/response cycle than you should use
`REQUEST_TIMER` configuration.

```python
from gajo_utils.decorators import timeview


@timeview
def example_view(request):
    return ...
```

```shell
Function time (function_name): 43.22ms
```

### License

Distributed under the MIT License. See `LICENSE.txt` for more information.
