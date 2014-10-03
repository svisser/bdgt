from sqlalchemy import (Boolean, Column, Date, Float, ForeignKey, Integer,
                        Unicode)
from sqlalchemy.orm import relationship

from bdgt.storage.database import Base


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    number = Column(Unicode, nullable=False)
    transactions = relationship("Transaction", backref="account",
                                cascade='all, delete, delete-orphan')

    def __init__(self, name, number):
        self.name = name
        self.number = number


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)

    def __init__(self, name):
        self.name = name


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    date = Column(Date, nullable=False)
    description = Column(Unicode)
    amount = Column(Float, nullable=False)
    reconciled = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category")

    def __init__(self, account, date, description, amount,
                 reconciled=False):
        self.account = account
        self.date = date
        self.description = description
        self.amount = amount
        self.reconciled = reconciled
