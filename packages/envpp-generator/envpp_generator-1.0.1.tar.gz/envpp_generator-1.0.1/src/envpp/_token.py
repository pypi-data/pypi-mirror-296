import sys
from os import getenv
from pathlib import Path

base_path: str | None = None

match sys.platform:
	case 'darwin' | 'linux':
		base_path = getenv('HOME')
	case 'win32':
		base_path = getenv('APPDATA')
	case _:
		base_path = None

if not base_path:
	print('Your platform is not yet supported')
	sys.exit(1)

token_file = Path(base_path) / '.envpp' / 'token.txt'

token: str | None = None

try:
	token = token_file.read_text()
except FileNotFoundError:
	token = None

if not token:
	print('First you need to authorize through the client')
	sys.exit(1)
