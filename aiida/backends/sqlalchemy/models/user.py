# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Boolean, DateTime

from aiida.utils import timezone
from aiida.backends.sqlalchemy.models.base import Base


class DbUser(Base):
    __tablename__ = "db_dbuser"

    id = Column(Integer, primary_key=True)
    email = Column(String(254), unique=True, index=True)
    password = Column(String(128))  # Clear text password ?
    first_name = Column(String(254), nullable=True)
    last_name = Column(String(254), nullable=True)
    institution = Column(String(254), nullable=True)

    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    last_login = Column(DateTime(timezone=True), default=timezone.now)
    date_joined = Column(DateTime(timezone=True), default=timezone.now)

    is_active = True

    def __init__(self, email, first_name, last_name, institution, **kwargs):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.institution = institution

        for field in ['is_staff', 'is_active', 'date_joined']:
            if field in kwargs:
                setattr(self, field, kwargs[field])

    def get_full_name(self):
        if self.first_name and self.last_name:
            return "{} {} ({})".format(self.first_name, self.last_name,
                                       self.email)
        elif self.first_name:
            return "{} ({})".format(self.first_name, self.email)
        elif self.last_name:
            return "{} ({})".format(self.last_name, self.email)
        else:
            return "{}".format(self.email)

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email