from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base

from jet_bridge.filters.model import get_model_filter_class
from jet_bridge.serializers.model import get_model_serializer
from jet_bridge.views.mixins.model import ModelAPIViewMixin
from jet_bridge.db import engine


class ModelHandler(ModelAPIViewMixin):
    model = None

    def get_model(self):
        if self.model:
            return self.model

        metadata = MetaData()
        metadata.reflect(engine)
        Base = automap_base(metadata=metadata)

        Base.prepare()
        self.model = Base.classes[self.path_kwargs['model']]

        return self.model

    def get_serializer_class(self):
        Model = self.get_model()
        return get_model_serializer(Model)

    def get_filter_class(self):
        return get_model_filter_class(self.get_model())

    def get_queryset(self):
        Model = self.get_model()

        return self.session.query(Model)