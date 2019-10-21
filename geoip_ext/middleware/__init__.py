import logging
import os
import warnings
import geoip2.database
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from geoip2.errors import AddressNotFoundError

logger = logging.getLogger("django")

mmdb_path = getattr(settings, "GEOIP_PATH_MMDB", None)


class GeoIPMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None):
        # logger.info(mmdb)
        self.get_response = get_response
        # assert mmdb is not None
        mmdb = "{path}/GeoLite2-Country.mmdb".format(path=mmdb_path)

        if mmdb and os.path.isfile(mmdb):
            try:
                self.reader = geoip2.database.Reader(mmdb)
            except FileNotFoundError as e:
                self.reader = None
            except Exception as e:
                logger.error(e)
                self.reader = None
        else:
            warnings.warn("django settings GEOIP_PATH_MMDB not configured")
            self.reader = None

    def process_request(self, request):
        if "HTTP_X_FORWARDED_FOR" in request.META.keys():
            _client_ip = request.META["HTTP_X_FORWARDED_FOR"]
            logger.info(_client_ip)
        else:
            _client_ip = request.META["REMOTE_ADDR"]
            logger.info(_client_ip)

        _client_ip = '36.104.15.42, 112.34.110.28'
        try:
            _client_ip = _client_ip.split(",")[0]
        except IndexError:
            _client_ip = None

        if self.reader is not None and _client_ip is not None:
            try:
                _client_ip = _client_ip.strip()
                res = self.reader.country(_client_ip)
                logger.info(res.country.iso_code)
                request.iso_code = res.country.iso_code
            except AddressNotFoundError as e:
                logger.info(e)
