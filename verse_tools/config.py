import requests
import json
import os


def save_config(pref_path, pref):
    with open(pref_path, 'w', encoding='utf8') as f:
        json.dump(pref, f, indent=2, sort_keys=True)

    return


def default_config(pref_path):
    config_string = """{"default_language": "English",
  "git_languages": []}"""
    config = json.loads(config_string)

    save_config(pref_path, config)
    return


def refresh(pref_path, pref):
    git = requests.get(
        'https://api.github.com/repos/CrudeRags/Bible-database/commits')
    # url of tree in the latest commit
    trl = git.json()[0]['commit']['tree']['url']
    trl_get = requests.get(trl)

    my_languages = []

    for x in trl_get.json()['tree']:
        if x['path'][-2:] == 'db':
            my_languages.append(x['path'].split('Bible')[0])

    pref['git_languages'] = my_languages
    save_config(pref_path, pref)
    return


def set_resource_path(pref_path, pref):
    print("\nResource path should not contain spaces. Use _ instead\
            \ncurrent resources will be moved to the new directory")
    print("If you uninstall this package, resource directory has\
            \nto be manually removed")
    new_resource_path = input("\nEnter resource path: ")

    if not os.path.exists(new_resource_path):
        os.makedirs(new_resource_path)

    pref['resource_path'] = new_resource_path

    save_config(pref_path, pref)

    return


def main():
    file_path = os.path.abspath(os.path.dirname(__file__))
    _pref_path_ = os.path.join(file_path, 'config.json')

    if not os.path.isfile(_pref_path_):
        default_config(_pref_path_)

    with open(_pref_path_, 'r') as p:
        pref = json.load(p)

    refresh(_pref_path_, pref)
    set_resource_path(_pref_path_, pref)


if __name__ == "__main__":
    main()
