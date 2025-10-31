# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Airport(db.Model):

    __tablename__ = 'Airport'

    id = db.Column(db.Integer, primary_key=True)

    #__Airport_FIELDS__
    iata = db.Column(db.String(255),  nullable=True)
    icao = db.Column(db.String(255),  nullable=True)
    name = db.Column(db.String(255),  nullable=True)
    phone = db.Column(db.String(255),  nullable=True)
    website = db.Column(db.String(255),  nullable=True)
    location = db.Column(db.String(255),  nullable=True)
    country = db.Column(db.String(255),  nullable=True)
    postalcode = db.Column(db.String(255),  nullable=True)
    city = db.Column(db.String(255),  nullable=True)
    street = db.Column(db.String(255),  nullable=True)
    streetnumber = db.Column(db.String(255),  nullable=True)
    latitude = db.Column(db.String(255),  nullable=True)
    longitude = db.Column(db.String(255),  nullable=True)

    #__Airport_FIELDS__END

    def __init__(self, **kwargs):
        super(Airport, self).__init__(**kwargs)


class Configuration(db.Model):

    __tablename__ = 'Configuration'

    id = db.Column(db.Integer, primary_key=True)

    #__Configuration_FIELDS__
    url = db.Column(db.String(255),  nullable=True)
    user = db.Column(db.String(255),  nullable=True)
    password = db.Column(db.String(255),  nullable=True)
    token = db.Column(db.String(255),  nullable=True)

    #__Configuration_FIELDS__END

    def __init__(self, **kwargs):
        super(Configuration, self).__init__(**kwargs)



#__MODELS__END
