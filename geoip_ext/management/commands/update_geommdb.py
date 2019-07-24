import os
import shutil
import tempfile

import requests
import tarfile

from django.core.management.base import BaseCommand
from django.conf import settings

# logger = logging.getLogger("django")


db_link = "https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz"

geoip_path = getattr(settings, "GEOIP_PATH_MMDB", None)


class Command(BaseCommand):
    help = "update GeoLite2 Country db"

    def get_mmdb_file(self, members):
        for tarinfo in members:
            if os.path.splitext(tarinfo.name)[1] == ".mmdb":
                self.mmdb_filename = tarinfo.name
                yield tarinfo

    def handle(self, *args, **options):
        # logger.info(db_link)
        tmpdir = tempfile.mkdtemp()
        local_filename = "{}/{}".format(
            tmpdir,
            db_link.split("/")[-1]
        )

        self.stdout.write(self.style.NOTICE("start download %s" % local_filename))
        with requests.get(db_link, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            # logger.info(local_filename)
        self.stdout.write(self.style.SUCCESS("Download %s Success" % local_filename))

        tar = tarfile.open(local_filename)
        tar.extractall(path=tmpdir, members=self.get_mmdb_file(tar))
        tar.close()
        mmdb_src = "{}/{}".format(
            tmpdir,
            self.mmdb_filename
        )
        shutil.move(src=mmdb_src, dst=geoip_path)
        shutil.rmtree(tmpdir)
