# djnacos

A Django tool of Nacos

Nacos OpenAPI see: https://nacos.io/docs/latest/guide/user/open-api/

[![Pypi Version](https://badge.fury.io/py/djnacos.svg)](https://badge.fury.io/py/djnacos)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/lcoolcool/djnacos/blob/main/LICENSE)

### **Supported Nacos version:**

Nacos 0.8.0+ 
Nacos 1.x 
Nacos 2.x with http protocol

### **Supported Django version:**

Django 2.2+

### **Installation**

```shell
pip install djnacos
```
## Unified Configuration Management
#### **Getting Started**

```python
# django project settings.py

# Get it through djnacos
NACOS_SERVER_ADDRESSES = 'server addresses split by comma'
NACOS_SERVER_NAMESPACE = 'namespace id'
NACOS_SERVER_USERNAME = 'username'
NACOS_SERVER_PASSWORD = 'password'
NACOS_SERVER_GROUP = 'group id' # default group is DEFAULT_GROUP
CONFIG_SERVER_DATA_ID = "data id"

from djnacos.nacos import get_config
config = get_config()  # return Dict
print(config)

# Example
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config.get('DATABASES_NAME'),
        'USER': config.get('DATABASES_USER'),
        'PASSWORD': config.get('DATABASES_PASSWORD'),
        'HOST': config.get('DATABASES_HOST')
    }
}
```

#### **In Django projects, use a more elegant configuration method.**

* Step 1: Update the `settings.py` file.
    ```python
    # django project settings.py
    # Get it through djnacos
    NACOS_SERVER_ADDRESSES = 'server addresses split by comma'
    NACOS_SERVER_NAMESPACE = 'namespace id'
    NACOS_SERVER_USERNAME = 'username'
    NACOS_SERVER_PASSWORD = 'password'
    CONFIG_SERVER_DATA_ID = "data id"
    
    from .env import env
    
    # Example
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env('DATABASES_NAME'),
            'USER': env('DATABASES_USER'),
            'PASSWORD': env('DATABASES_PASSWORD'),
            'HOST': env('DATABASES_HOST')
        }
    }
    ```
* Step 2: Create a file named `env.py` in the project, in the same directory as `settings.py`, and put the following content in the file.
    ```python
    from djnacos.nacos import get_config
    from .env_default import DEFAULT_SETTINGS
   
    NACOS_SETTINGS = get_config()
    
    
    def env(key: str):
        return NACOS_SETTINGS.get(key) or DEFAULT_SETTINGS.get(key)
    ```

* Step 3: Create a file named `env_default.py` in the project as the default settings, in the same directory as `env.py`, and put the following content in the file.
    ```python
    # if not djnacos config, use default settings
    DEFAULT_SETTINGS = {
        'DATABASES_NAME': 'db_name',
        'DATABASES_USER': 'db_user',
        'DATABASES_PASSWORD': 'db_password',
        'DATABASES_HOST': 'db_host',
        # ...
    }
    ```