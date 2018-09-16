import rastervision as rv
from rastervision.data import (LabelStore, LabelStoreConfig,
                               LabelStoreConfigBuilder,
                               ChipClassificationLabels)
from rastervision.protos.label_store_pb2 \
    import LabelStoreConfig as LabelStoreConfigMsg

NOOP_STORE = 'NOOP_STORE'


class NoopLabelStore(LabelStore):
    def save(self, labels):
        pass

    def get_labels(self):
        return ChipClassificationLabels()

    def empty_labels(self):
        return ChipClassificationLabels()

    def concatenate(self, labels1, labels2):
        labels1.extend(labels2)
        return labels1


class NoopLabelStoreConfig(LabelStoreConfig):
    def __init__(self):
        super().__init__(NOOP_STORE)

    def to_proto(self):
        msg = super().to_proto()
        msg.MergeFrom(LabelStoreConfigMsg(custom_config={}))
        return msg

    def create_store(self, task_config, crs_transformer, tmp_dir):
        return NoopLabelStore()

    def preprocess_command(self, command_type, experiment_config, context=[]):
        return (self, rv.core.CommandIODefinition())


class NoopLabelStoreConfigBuilder(LabelStoreConfigBuilder):
    def __init__(self, prev=None):
        super().__init__(NoopLabelStoreConfig, {})

    def from_proto(self, msg):
        return self


def register_plugin(plugin_registry):
    plugin_registry.register_config_builder(rv.LABEL_STORE, NOOP_STORE,
                                            NoopLabelStoreConfigBuilder)