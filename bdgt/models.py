""" This module provides classes related to strength training. """

from __future__ import division

from sqlalchemy import Column, Integer, Unicode

from bdgt.storage.database import Base


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)

    def __init__(self, name):
        self.name = name
