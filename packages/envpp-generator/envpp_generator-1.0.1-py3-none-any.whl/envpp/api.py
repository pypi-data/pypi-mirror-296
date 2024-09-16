import msgspec
import requests


class Item(msgspec.Struct):
	id_: int = msgspec.field(name='id')
	key: str
	value: str


class Api:
	def __init__(self, token: str) -> None:
		self.session = requests.Session()
		self.session.headers = {'Authorization': f'Bearer {token}'}
		self.base_url = 'https://envpp.onrender.com/api'

	def find_all_items(self) -> list[Item]:
		response = self.session.get(f'{self.base_url}/items')
		response_text = response.text

		if response.status_code != 200:
			raise Exception(response_text)

		return msgspec.json.decode(response_text, type=list[Item])

	def find_one(self, id_: int) -> Item:
		response = self.session.get(f'{self.base_url}/items/{id_}')
		response_text = response.text

		if response.status_code != 200:
			raise Exception(response_text)

		return msgspec.json.decode(response_text, type=Item)
