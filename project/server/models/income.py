from marshmallow import fields

from .transaction import Transaction, TransactionSchema
from .transaction_type import TransactionType


class Income(Transaction):
  def __init__(self, description, amount):
    super(Income, self).__init__(description, amount, TransactionType.INCOME)

  def __repr__(self):
    return '<Income(name={self.description!r})>'.format(self=self)


class IncomeSchema(TransactionSchema):
  __envelope__ = {"single": "income", "many": "incomes"}
  __model__ = Income
  description = fields.Str()
  amount = fields.Number()
  created_at = fields.Date()
  type = fields.Str()
