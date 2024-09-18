# djnacos

A Django tool of Nacos

Nacos OpenAPI see: https://nacos.io/docs/latest/guide/user/open-api/

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/nacos-group/nacos-sdk-python/blob/master/LICENSE)

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

#### **More Elegant Configuration**

* Step 1: Create a file named `env.py` in the project, in the same directory as `settings.py`, and put the following content in the file.
    ```python
    from djnacos.nacos import get_json_config
    # create a file named `env_default.py`, in the same directory
    # from .env_default import DEFAULT_SETTINGS   # if not djnacos config, use default settings
   
    NACOS_SETTINGS = get_json_config()
    
    
    def env(key: str):
        return NACOS_SETTINGS.get(key)
        # return NACOS_SETTINGS.get(key) or DEFAULT_SETTINGS.get(key)  # if not djnacos config, use default settings
    ```
* Step 2: Update the `settings.py` file.
    ```python
    # django project settings.py
    # Get it through djnacos
    NACOS_SERVER_ADDRESSES = 'server addresses split by comma'
    NACOS_SERVER_NAMESPACE = 'namespace id'
    # NACOS_SERVER_USERNAME = 'username'
    # NACOS_SERVER_PASSWORD = 'password'
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

## **Service Liveness Probe**

#### **Beat Check**
```bash
curl -X GET http://127.0.0.1:8000/check/beat/
```
Liveness Response:
   http status code 200