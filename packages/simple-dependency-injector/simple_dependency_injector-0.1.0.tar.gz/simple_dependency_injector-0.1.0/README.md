
# Dependency Injector for Python

A simple and flexible dependency injection framework for Python projects. This library allows you to define services, manage their lifecycle, and inject dependencies into your applications in a clean and structured way.

## Installation

You can install this library using pip:

```bash
pip install simple-dependency-injector
```

## Basic Usage

### Loading and Compiling Services

First, load your service definitions from a YAML file or Python module and compile them:

```python
from simple_dependency_injector import DependencyInjector

# Create an injector and load the service definitions
injector = DependencyInjector(base_path='config_path')
injector.load('services.yaml')
injector.compile()

# Access a service
service = injector.get('my_service')
```


### Service Definition Example (`services.yaml`)

You can define services in a YAML file:

```yaml
services:
  my_service:
    class: 'tests/services/my_module.py#MyService'
    arguments:
      - '@another_service'
    scope: singleton

  another_service:
    class: 'tests/services/another_module.py#AnotherService'
    scope: transient
```

- `class`: The fully qualified class name to instantiate.
- `arguments`: The list of dependencies to inject.
    - **Service Reference** (`@service_name`): This resolves to another service defined in the injector.
    - **Tagged Services** (`!tagged:tag_name`): This resolves to a list of services that have the specified tag.
    - **Context Reference** (`!context`): This resolves to the current DI context.

- `scope`: The lifecycle of the service. Options are `singleton`, `transient`, `request`, or `ambivalent`.

### Example of Argument Resolution:

```yaml
services:
  my_service:
    class: 'tests/services/my_service.py#MyService'
    arguments:
      - '@another_service'
      - '!tagged:logging'
      - '!context'
    scope: singleton
```

When `my_service` is instantiated, the `@another_service` argument will resolve to the instance of `another_service`, `!tagged:logging` will resolve to a list of services tagged with `logging`, and `!context` will resolve to the current DI context.

### Accessing Services by Tags

You can assign tags to services and resolve them by tag:

```yaml
services:
  tagged_service:
    class: 'tests/services/tagged_service.py#TaggedService'
    tags:
      - 'my_tag'
    scope: singleton
```

You can then retrieve all services that have a specific tag:

```python
services_with_tag = injector.get_list_with_tag('my_tag')
```

### Linking Services

You can link services during runtime. For example, you can retrieve one service and assign its instance to another service:

```python
injector.link('source_service', 'target_service')
```

This is useful when you need to dynamically replace or redirect service instances.

## Using the Dependency Injector in Django

To use the dependency injector in Django, you can inject services into requests by creating a custom middleware.

### 1. Middleware for Dependency Injection Context

Create a middleware to add a new dependency injection context for each request:

```python
# middlewares.py
from simple_dependency_injector import DependencyInjector

injector = DependencyInjector(base_path='config_path')
injector.load('services.yaml')
injector.compile()


class DependencyInjectorMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    request.container = injector.create_context()
    response = self.get_response(request)
    return response
```

### 2. Middleware for Logger Service

You can also create a middleware to inject services like a logger into the request context:

```python
# middlewares.py
from .logger_service import DjangoLoggerService

class LoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.container.set("logger_service", DjangoLoggerService(request))
        response = self.get_response(request)
        return response
```

### 3. Register the Middlewares in Django Settings

Add the middlewares to your `MIDDLEWARE` setting in `settings.py`:

```python
# settings.py
MIDDLEWARE = [
    # Other middlewares
    'myapp.middlewares.DependencyInjectorMiddleware',
    'myapp.middlewares.LoggerMiddleware',
]
```

### 4. Accessing Services in Django Views

Now you can access the services from the request container in your Django views:

```python
# views.py
from django.http import JsonResponse

def my_view(request):
    # Get the logger service from the DI container
    logger = request.container.get('logger_service')

    # Use the logger
    logger.log('This is a log message')

    return JsonResponse({'status': 'success'})
```

## Advanced Features

### Using Factories

You can define services using factory methods. This is useful when the service creation logic is more complex:

```yaml
services:
  factory_service:
    factory:
      class: 'tests/services/my_module.py#MyFactory'
      method: create_service
    arguments:
      - 'config_value'
    scope: singleton
```

### Contextual Dependency Injection

For services that need to maintain a request-specific state, you can create a new context per request and resolve services within that context:

```python
# Create a context for each request
context = injector.create_context()

# Access services within that context
service = context.get('my_service')
```


## Development

### Setting Up a Development Environment

To set up a local development environment for this project, follow these steps:

1. Fork this repository and clone it:

```bash
git clone https://github.com/yourusername/python-simple-dependency-injector.git
cd simple-dependency-injector
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

  ```bash
  source venv/bin/activate
  ```

4. Install the development dependencies:

```bash
pip install -r requirements-dev.txt
```

Now you are ready to start working on the project. You can run tests, add new features, or fix bugs.

## Check the code style

```bash
black simple_dependency_injector tests && pylint simple_dependency_injector tests
```

## Tests

This project includes a suite of unit tests to ensure that all functionality works as expected. The tests are located in the `tests` directory, and you can run them using:

```bash
python -m unittest discover tests
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
