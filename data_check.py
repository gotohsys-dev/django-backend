import json
import os

# data.json のパスを正確に指定してください
# プロジェクトのルートディレクトリを基準にするか、現在のスクリプトからの相対パスを指定します
# 例: dmm_dev/backend/dmm_items/fixtures/data.json
# このスクリプトが backend ディレクトリにあると仮定すると、以下のパスが適切かもしれません
input_filepath = os.path.join('dmm_items', 'fixtures', 'data.json')
output_filepath = os.path.join('dmm_items', 'fixtures', 'data_fixed.json') # 修正後の新しいファイル名

fields_to_remove = ['sample_image_small', 'sample_image_large']

print(f"Loading data from: {input_filepath}")
try:
    with open(input_filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{input_filepath}' was not found. Please check the path.")
    exit()
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{input_filepath}'. Please check if it's a valid JSON file.")
    exit()

modified_count = 0
for item in data:
    if 'fields' in item and isinstance(item['fields'], dict):
        original_keys = list(item['fields'].keys()) # 変更前のキーを保持
        for field in fields_to_remove:
            if field in item['fields']:
                del item['fields'][field]
                modified_count += 1
        if list(item['fields'].keys()) != original_keys:
            print(f"Modified item with pk: {item.get('pk', 'N/A')}")


print(f"Removed '{', '.join(fields_to_remove)}' from {modified_count} entries.")

print(f"Saving modified data to: {output_filepath}")
try:
    with open(output_filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Data successfully saved.")
except Exception as e:
    print(f"Error saving file: {e}")