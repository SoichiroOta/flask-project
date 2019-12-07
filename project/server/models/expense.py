from marshmallow import fields

from .transaction import Transaction, TransactionSchema
from .transaction_type import TransactionType


class Expense(Transaction):
  def __init__(self, description, amount):
    super(Expense, self).__init__(
      description, -abs(amount), TransactionType.EXPENSE)

  def __repr__(self):
    return '<Expense(name={self.description!r})>'.format(self=self)


class ExpenseSchema(TransactionSchema):
  __envelope__ = {"single": "expense", "many": "expenses"}
  __model__ = Expense
  description = fields.Str()
  amount = fields.Number()
  created_at = fields.Date()
  type = fields.Str()
