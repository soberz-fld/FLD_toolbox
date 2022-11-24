import json
import os


def format_byte_to_dict(bytes_dict: bytes) -> dict:
    # TODO: Check if bytes can be translated to dict
    string = bytes_dict.decode('utf8').replace("'", '"')
    jsoned = json.loads(string)
    return jsoned


def save_list_of_dicts_to_csv(self, list_of_dicts: list[dict], path: str = 'saved_list.csv'):
    if not list_of_dicts:
        print('Error: List is empty')
    else:  # List is not empty
        filename, file_ext = os.path.splitext(path)
        list_of_all_keys = []
        for dict_obj in list_of_dicts:
            for key in dict_obj.keys():
                if key not in list_of_all_keys:
                    list_of_all_keys.append(key)
        file_exists = True
        index = ''
        while file_exists:
            if os.path.exists(filename + index + file_ext):
                index = str(int(index) + 1) if index != '' else '1'
            else:
                file_exists = False
                filename += index
        path = filename + file_ext
        with open(path, mode='w+') as csv:
            line = ''
            for key in list_of_all_keys:
                line += key
                line += ';'
            line += '\n'
            csv.write(line)
            for dict_obj in list_of_dicts:
                line = ''
                for key in list_of_all_keys:
                    try:
                        line += str(dict_obj[key])
                    except KeyError as e:
                        pass
                    line += ';'
                line += '\n'
                csv.write(line)
