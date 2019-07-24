import geoip_ext
from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()


install_requires = [
                       'Django >= 1.11',
                       'geoip2 == 2.9.0',
                   ],



setup(
    name='django-geoip-ext',
    version=geoip_ext.__version__,
    description="""Django GeoIP""",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    license='GNU License',
    zip_safe=False,
    keywords="django-geoip",
)
