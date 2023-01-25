#! /usr/bin/env python

import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'metadata-organizer'))
import src.utils as utils


def convert_folder(folder_path, json_path):
    for elem in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, elem)):
            if not os.path.exists(os.path.join(json_path, elem)):
                try:
                    read_file = utils.read_in_yaml(os.path.join(folder_path, elem))
                    print(f'convert file {os.path.join(folder_path, elem)}')
                    json.dump(read_file, open(os.path.join(json_path, elem), 'w'))
                except AttributeError:
                    pass
            else:
                if os.path.getmtime(os.path.join(folder_path, elem)) > os.path.getmtime(os.path.join(json_path, elem)):
                    try:
                        read_file = utils.read_in_yaml(
                            os.path.join(folder_path, elem))
                        print(
                            f'convert file {os.path.join(folder_path, elem)}')
                        json.dump(read_file, open(os.path.join(json_path, elem), 'w'))
                    except AttributeError:
                        pass

        elif os.path.isdir(os.path.join(folder_path, elem)):
            if not os.path.exists(os.path.join(json_path, elem)):
                print(f'create folder {os.path.join(folder_path, elem)}')
                os.mkdir(os.path.join(json_path, elem))
            convert_folder(os.path.join(folder_path, elem), os.path.join(json_path, elem))


if __name__ == "__main__":
    convert_folder(os.path.join(os.path.dirname(__file__), '..', 'whitelists'), os.path.join(os.path.dirname(__file__), 'json'))