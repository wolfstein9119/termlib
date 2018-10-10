from elasticsearch_dsl import Integer, Text

from .base import BaseDocument, RUSSIAN_INDEX_SETTINGS


class Term(BaseDocument):
    id = Integer()
    name = Text()
    definitions = Text(multi=True)

    class Index:
        name = 'terms'
        doc_type = 'term'
        settings = RUSSIAN_INDEX_SETTINGS

    class Meta:
        doc_type = 'term'
