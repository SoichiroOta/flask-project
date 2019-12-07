# project/server/api/views.py


from flask import Blueprint
from flask import jsonify, request

from ..models.expense import Expense, ExpenseSchema
from ..models.income import Income, IncomeSchema
from ..models.transaction_type import TransactionType


api_blueprint = Blueprint("api", __name__)

transactions = [
  Income('Salary', 5000),
  Income('Dividends', 200),
  Expense('pizza', 50),
  Expense('Rock Concert', 100)
]


@api_blueprint.route('/incomes')
def get_incomes():
  schema = IncomeSchema(many=True)
  incomes = schema.dump(
    filter(lambda t: t.type == TransactionType.INCOME, transactions)
  )
  return jsonify(incomes)


@api_blueprint.route('/incomes', methods=['POST'])
def add_income():
  print(request.get_json())
  income = IncomeSchema().load(request.get_json())
  transactions.append(income)
  return "", 204


@api_blueprint.route('/expenses')
def get_expenses():
  schema = ExpenseSchema(many=True)
  expenses = schema.dump(
      filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
  )
  return jsonify(expenses)


@api_blueprint.route('/expenses', methods=['POST'])
def add_expense():
  expense = ExpenseSchema().load(request.get_json())
  transactions.append(expense)
  return "", 204
