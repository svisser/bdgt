import datetime
import logging

from sqlalchemy.orm.exc import NoResultFound

from bdgt.models import BudgetItem, Category
from bdgt.storage.gateway import session_scope


_log = logging.getLogger(__name__)


class CmdSet(object):
    def __init__(self, category_name, period, amount):
        self.category_name = category_name
        self.period = period
        self.amount = amount

    def __call__(self):
        # Get the category if it already exists, or create a new one.
        with session_scope() as session:
            try:
                category = session.query(Category) \
                                  .filter_by(name=self.category_name) \
                                  .one()
            except NoResultFound:
                raise ValueError("{} not found".format(self.category_name))

            budget_item = BudgetItem(datetime.datetime.now().date(),
                                     self.period, self.amount)
            category.budget_items.append(budget_item)

            session.add(category)

        return 'Budget for "{}" is set to {} per {}'.format(self.category_name,
                                                            self.amount,
                                                            self.period)
