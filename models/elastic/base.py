from elasticsearch_dsl import Document


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
