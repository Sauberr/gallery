from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from images.models import Images


@registry.register_document
class ImagesDocument(Document):
    '''Elasticsearch document for the Images model'''

    class Index:
        name = "images"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Images
        fields = ["title", "author", "description"]
