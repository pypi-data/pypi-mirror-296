from typing import Generic, TypeVar

from .api import Api

T = TypeVar('T')


class Envpp(Generic[T]):
	def __init__(self, api: Api, items_key_and_id: dict[T, int]):
		self.api = api
		self.items_key_and_id = items_key_and_id

	def __getitem__(self, item_key: T) -> str:
		return self.api.find_one(self.items_key_and_id[item_key]).value
