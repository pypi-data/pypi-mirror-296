## Getting Started

### Installation

1. Install package
    ```sh
    pip install django-gajo-utils
    ```

2. Add `GajoDebugUtilsMiddleware` to project settings before all other **none-dev**
   related middlewares.
    ```python
    MIDDLEWARE = [
        'gajo_utils.middleware.GajoDebugUtilsMiddleware',
        ... other apps
    ]
    ```
3. Add `gajo_utils` to `INSTALLED_APPS`.
    ```python
    INSTALLED_APPS = [
        ...other apps
        'gajo_utils',
    ]
    ```

4. Turn on any of the utils by settings its value to `True` (by default all utils are
   disabled)
    ```python
    GAJO_UTILS_CONFIG = {
        "REQUEST_TIMER": False,
        "REQUEST_DELAY": False,
        "REQUEST_COOKIES": False,
        "RESPONSE_COOKIES": False,
        "RESPONSE_CONTENT": False,
        "RESPONSE_QUERIES": False,
        "DUMP_FIXTURES": [
            "dummy.Model1",
            "dummy.Model2",
        ],
        "LOAD_FIXTURES": [
            "dummy.Model1",
            "dummy.Model2",
        ],
    }
    ```

## Usage

### Middleware Configuration

- `"REQUEST_TIMER": True` prints in terminal how much time it needed for
  request/response
  cycle to finish.

- `"REQUEST_DELAY": True` adds random delay (50ms - 300ms) to every request and than
  prints in terminal how much was request delayed. This config is used to simulate
  latency
  on server.

- `"REQUEST_COOKIES": True` prints in terminal request cookies.

- `"RESPONSE_COOKIES": True` prints in terminal response cookies.

- `"RESPONSE_CONTENT": True` prints in terminal response content.

- `"RESPONSE_QUERIES": True` prints all queries that were made in response/request cycle
  with time for each one. It also prints total time for all queries and number of
  similar queries (queries that can be probably optimized with `select_related`
  or `prefetch_related`).

### Decorators

Decorator for timing how much time took for view to run. If you want to time whole
request/response cycle than you should use `REQUEST_TIMER` configuration.

```python
from gajo_utils.decorators import timeview


@timeview
def example_view(request):
    return ...
```

```shell
Function time (function_name): 43.22ms
```

### Management Commands

`gajo_utils` adds three extra commands to your django app.

- `./manage.py testsingle {test_name}` offers you option to test single function test or
  test single TestCase class without needing to providing full path to test
  like `apps.dummy.tests.test_dummies.DummyTest.test_dummy`. You can instead just
  specify `DummyTest` or `test_dummy`.

  > If command finds two functions or classes with same name in
  > different app it will test both separately (with two commands
  > executed).

- `./manage.py dumpfixtures` this management command needs extra configuration
  in `settings.py`. You can specify which models you want to be dumped into database
  in `GAJO_UTILS_CONFIG`. Every model is than dumped in json format
  at `ROOT_DIR/fixtures/app_name/ModelName.json`.
    ```python
    GAJO_UTILS_CONFIG = {
        "DUMP_FIXTURES": [
            "dummy.Model1",
            "dummy.Model2",
        ]
    }
    ```

- `./manage.py loadfixtures` this management command needs extra configuration
  in `settings.py`. You can specify which models you want to be loaded into database
  in `GAJO_UTILS_CONFIG`. There must be file created at correct
  path: `ROOT_DIR/fixtures/app_name/ModelName.json`
    ```python
    GAJO_UTILS_CONFIG = {
        "LOAD_FIXTURES": [
            "dummy.Model1",
            "dummy.Model2",
        ]
    }
    ```

### Versioning

This package is using Semantic Versioning. You can find informations about it
here: https://semver.org/.

### License

Distributed under the MIT License. See `LICENSE.txt` for more information.
