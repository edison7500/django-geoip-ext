# Django Geoip-ext

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d5170ab610804b6cac87663fc9832109)](https://app.codacy.com/app/edison7500/django-geoip-ext?utm_source=github.com&utm_medium=referral&utm_content=edison7500/django-geoip-ext&utm_campaign=Badge_Grade_Dashboard)

## Requirement

* Python >= 3.5
* Django >= 1.11
* no support Python 2

## Install 
```.shell script
git clone https://github.com/edison7500/django-geoip-ext.git
cd path/to/django-geoip-ext
python setup.py install
```


## Usage
```.python

INSTALLED_APPS = [
    ...    
    "geoip_ext",
    ...
]

MIDDLEWARE = [
    ...
    "geoip_ext.middleware.GeoIPMiddleware",
    ...
]

```