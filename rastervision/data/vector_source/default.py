from abc import (ABC, abstractmethod)
import os

import rastervision as rv


class VectorSourceDefaultProvider(ABC):
    @staticmethod
    @abstractmethod
    def handles(s):
        """Returns True of this provider is a default for this string"""
        pass

    @abstractmethod
    def construct(s):
        """Constructs a default VectorSource based on the
           string.
        """
        pass


class GeoJSONVectorSourceDefaultProvider(VectorSourceDefaultProvider):
    @staticmethod
    def handles(uri):
        ext = os.path.splitext(uri)[1]
        return ext.lower() in ['.json', '.geojson']

    @staticmethod
    def construct(uri):
        return rv.VectorSourceConfig.builder(rv.GEOJSON_SOURCE) \
                                    .with_uri(uri) \
                                    .build()


class MBTilesVectorSourceDefaultProvider(VectorSourceDefaultProvider):
    @staticmethod
    def handles(uri):
        ext = os.path.splitext(uri)[1]
        return ext.lower() in ['.mbtiles']

    @staticmethod
    def construct(uri):
        return rv.VectorSourceConfig.builder(rv.MBTILES_SOURCE) \
                                    .with_uri(uri) \
                                    .build()
