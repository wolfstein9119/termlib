from elasticsearch_dsl import Integer, Text, Keyword

from .base import BaseDocument


class Term(BaseDocument):
    id = Integer()
    name = Text()
    definitions = Text(multi=True)

    class Index:
        name = 'terms'
        doc_type = 'term'

    class Meta:
        doc_type = 'term'
