from __future__ import absolute_import
from mongoengine import queryset_manager, DoesNotExist, MultipleObjectsReturned, ValidationError
from flask_restful import abort
from cep_web_service.app import db


class Zipcode(db.Document):
    zip_code = db.IntField(required=True)
    address = db.StringField(required=False)
    neighborhood = db.StringField(required=False)
    city = db.StringField(required=True)
    state = db.StringField(required=True)
    meta = {
        'indexes': ['zip_code']
    }

    @classmethod
    def get_or_404(cls, *args, **kwargs):
        message = kwargs.pop('message', None)
        try:
            return cls.objects.get(*args, **kwargs)
        except (MultipleObjectsReturned, DoesNotExist, ValidationError):
            if message is not None:
                abort(404, message=message)
            abort(404)

    @queryset_manager
    def limit(cls, queryset, limit):
        return queryset[:limit]

    @classmethod
    def save_document(cls, zip_code, address, neighborhood, city, state):
        """
        Create or update a document
        returns True if created and False if only updated
        Update condition is based on zipcode. If zipcode already exists in db
        the the document is only updated. Otherwise the document is created
        """
        try:
            object_ = cls.objects.get(zip_code=zip_code)
            object_.update(
                address=address,
                neighborhood=neighborhood,
                city=city,
                state=state
            )
            return False
        except DoesNotExist:
            cls(
                zip_code=zip_code,
                address=address,
                neighborhood=neighborhood,
                city=city,
                state=state).save()
            return True

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
