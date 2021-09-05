import json
from os.path import getsize


class Utility:
    def __init__(self, items_file_name):
        self.items_file_name = items_file_name
        with open(items_file_name, 'a+') as items_file:  # initialise file
            if not getsize(items_file_name):  # only if file is brand new
                items_file.write('{}')

    def insert_new_item(self, item_name):
        with open(self.items_file_name, "r") as items_file:
            old_json = items_file.read()
            old = json.loads(old_json)

        old[item_name] = {"miss": 0}
        new_json = json.dumps(old)

        with open(self.items_file_name, "w") as items_file:
            items_file.write(new_json)

    def remove_item(self, item_name):
        with open(self.items_file_name, "r") as items_file:
            old_json = items_file.read()
            old = json.loads(old_json)

        if item_name not in old:
            raise Exception("Item to remove not found")

        del old[item_name]

        new_json = json.dumps(old)

        with open(self.items_file_name, "w") as items_file:
            items_file.write(new_json)

    def get_session_items(self, num_items):
        with open(self.items_file_name, "r") as items_file:
            old_json = items_file.read()
            old = json.loads(old_json)

        items_sorted = dict(sorted(old.items(), key=lambda item: item[1]['miss'], reverse=True))

        to_select = min(num_items, len(items_sorted))
        selected = list(items_sorted.keys())[:to_select]

        new = {}
        for k, v in old.items():
            new[k] = {}
            if k not in selected:
                new[k]['miss'] = v['miss'] + 1
            else:
                new[k]['miss'] = 0

        new_json = json.dumps(new)
        with open(self.items_file_name, "w") as items_file:
            items_file.write(new_json)
        return selected

    def get_all_items(self):
        with open(self.items_file_name, "r") as items_file:
            old_json = items_file.read()
            old = json.loads(old_json)
        return old

    def check_in_items(self, item_name):
        with open(self.items_file_name, "r") as items_file:
            old_json = items_file.read()
            old = json.loads(old_json)
        if item_name in old.keys():
            return True
        return False
