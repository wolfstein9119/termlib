from elasticsearch_dsl import Document
from elasticsearch.exceptions import NotFoundError


class BaseDocument(Document):
    def generate_elastic_id(self):
        return getattr(self, 'id', None)

    def to_dict(self, include_meta=False, skip_empty=True):
        result = super().to_dict(
            include_meta=include_meta,
            skip_empty=skip_empty,
        )
        if include_meta:
            e_id = self.generate_elastic_id()
            if e_id is not None:
                result['_id'] = e_id
        return result

    @classmethod
    def reinit_index(cls):
        try:
            cls._index.delete()
        except NotFoundError:
            pass
        cls._index.create()


RUSSIAN_INDEX_SETTINGS = {
    "analysis": {
        "filter": {
            "russian_stop": {
                "type": "stop",
                "stopwords": "_russian_"
            },
            "russian_stemmer": {
                "type": "stemmer",
                "language": "russian"
            }
        },
        "analyzer": {
            "default": {
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "russian_stop",
                    "russian_stemmer"
                ]
            }
        }
    }
}
