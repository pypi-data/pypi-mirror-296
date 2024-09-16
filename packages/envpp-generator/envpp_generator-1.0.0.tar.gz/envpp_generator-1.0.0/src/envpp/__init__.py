from ._api import api
from ._items import ItemsKeys, items_key_and_id
from .envpp import Envpp

envpp = Envpp[ItemsKeys](api, items_key_and_id=items_key_and_id)
