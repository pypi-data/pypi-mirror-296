import os
import time
from unittest import TestCase

import requests

from .. import RegionApi
from ..cache import session

WAIT_TIME = 0.2


class TestRegion(TestCase):
    def setUp(self) -> None:
        self.api = RegionApi()
        return super().setUp()

    def test_regions(self) -> requests.Response:
        time.sleep(WAIT_TIME)

        if not os.environ.get("REQUEST_CACHE"):
            # deactivate test if locally defined sqlite or

            r = self.api.regions(limit=5)
            assert not r.from_cache

        r = self.api.regions(limit=5)
        assert r.from_cache

    def test_cache(self) -> None:
        # Get some debugging info about the cache
        print(session.cache)
        print("Cached URLS:")
        print("\n".join(session.cache.urls()))

        assert len(session.cache.urls()) > 0
