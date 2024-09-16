from pathlib import Path

from ._api import api

items = api.find_all_items()

package_folder = Path(__file__).parent
items_file = package_folder / '_items.py'
items_template_file = package_folder / '_items.py.template'

items_file.write_text(
	items_template_file.read_text().format_map(
		{
			'<items_keys>': ','.join([f"'{item.key}'" for item in items]),
			'<items_key_and_id>': ','.join(
				[f"'{item.key}: {item.id_}'" for item in items]
			),
		}
	)
)

print('✅ Successfully!')
