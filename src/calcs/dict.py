import json
import os

def format_byte_to_dict(bytelist: bytes) -> dict:
    #TODO: Check if bytes can be translated to dict
    string = bytelist.decode('utf8').replace("'", '"')
    jsoned = json.loads(string)
    return jsoned

def save_list_of_dicts_to_csv(self, list_of_dicts: list[dict], path: str = 'saved_list.csv'):
    if not list_of_dicts:
        print('Error: List is empty')
    else:  # List is not empty
        filename, fileext = os.path.splitext(path)
        list_of_all_keys = []
        for dict in list_of_dicts:
            for key in dict.keys():
                if key not in list_of_all_keys:
                    list_of_all_keys.append(key)
        file_exists = True
        index = ''
        while file_exists:
            if os.path.exists(filename + index + fileext):
                index = str(int(index) + 1) if index != '' else '1'
            else:
                file_exists = False
                filename += index
        path = filename + fileext
        with open(path, mode='w+') as csv:
            line = ''
            for key in list_of_all_keys:
                line += key
                line += ';'
            line += '\n'
            csv.write(line)
            for dict in list_of_dicts:
                line = ''
                for key in list_of_all_keys:
                    try:
                        line += str(dict[key])
                    except KeyError as e:
                        pass
                    line += ';'
                line += '\n'
                csv.write(line)
