from copy import deepcopy

import rastervision as rv
from rastervision.data.vector_source.vector_source_config import (
    VectorSourceConfig, VectorSourceConfigBuilder)
from rastervision.data.vector_source.geojson_vector_source import GeoJSONVectorSource


class GeoJSONVectorSourceConfig(VectorSourceConfig):
    def __init__(self, uri, class_id_to_filter=None):
        self.uri = uri
        super().__init__(
            rv.GEOJSON_SOURCE, class_id_to_filter=class_id_to_filter)

    def to_proto(self):
        msg = super().to_proto()
        msg.geojson.uri = self.uri
        return msg

    def create_source(self, crs_transformer=None, extent=None, class_map=None):
        return GeoJSONVectorSource(
            self.uri, class_map=class_map, class_id_to_filter=self.class_id_to_filter)

    def update_for_command(self,
                           command_type,
                           experiment_config,
                           context=None,
                           io_def=None):
        io_def = io_def or rv.core.CommandIODefinition()
        io_def.add_input(self.uri)
        return io_def


class GeoJSONVectorSourceConfigBuilder(VectorSourceConfigBuilder):
    def __init__(self, prev=None):
        config = {}
        if prev:
            config = {
                'class_id_to_filter': prev.class_id_to_filter,
                'uri': prev.uri
            }

        super().__init__(GeoJSONVectorSourceConfig, config)

    def validate(self):
        if self.config.get('uri') is None:
            raise rv.ConfigError('GeoJSONVectorSourceConfigBuilder requires uri which '
                                 'can be set using "with_uri".')

        super().validate()

    def from_proto(self, msg):
        b = super().from_proto(msg)
        b = b.with_uri(msg.geojson.uri)
        return b

    def with_uri(self, uri):
        b = deepcopy(self)
        b.config['uri'] = uri
        return b
