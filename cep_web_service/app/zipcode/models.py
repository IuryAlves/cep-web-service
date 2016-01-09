from __future__ import absolute_import
from mongoengine import queryset_manager
from cep_web_service.app import db


class Zipcode(db.Document):
    zip_code = db.IntField(required=True)
    address = db.StringField(required=True)
    neighborhood = db.StringField(required=True)
    city = db.StringField(required=True)
    state = db.StringField(required=True)
    meta = {
        'indexes': ['zip_code']
    }

    def get_or_404(self, *args, **kwargs):
        return super(self.__class__, self).get_or_404(*args, **kwargs)

    @queryset_manager
    def limit(doc_cls, queryset, limit):
        return queryset[:limit]

    @classmethod
    def save_document(cls, zipcode, address, neighborhood, city, state):
        return cls(
            zip_code=zipcode,
            address=address,
            neighborhood=neighborhood,
            city=city,
            state=state).save()

    def to_dict(self):
        return {
            'zip_code': self.zip_code,
            'address': self.address,
            'neighborhood': self.neighborhood,
            'city': self.city,
            'state': self.state
        }

    def __unicode__(self):
        return self.zip_code

    __str__ = __unicode__
