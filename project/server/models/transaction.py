import datetime as dt

from marshmallow import Schema, post_dump, post_load


class Transaction():
  def __init__(self, description, amount, type):
    self.description = description
    self.amount = amount
    self.created_at = dt.datetime.now()
    self.type = type

  def __repr__(self):
    return '<Transaction(name={self.description!r})>'.format(self=self)


class TransactionSchema(Schema):
    # Custom options
    __envelope__ = {"single": None, "many": None}
    __model__ = object

    def get_envelope_key(self, many):
        """Helper to get the envelope key."""
        key = self.__envelope__["many"] if many else self.__envelope__[
          "single"]
        assert key is not None, "Envelope key undefined"
        return key

    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many, **kwargs):
        key = self.get_envelope_key(many)
        return {key: data}

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)
