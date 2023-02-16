import os
import json
import services
import sims4
from json.decoder import JSONDecodeError

from zone import Zone

from university_of_magic.utils.logging.logger import log
from university_of_magic.utils import injector

logger = sims4.log.Logger('_UniversityOfMagicSave', default_owner='lala')


file_name = 'UniversityOfMagic.json'
default = {
    'region_id': 222656
}


def update_preferred_region(region_id):

    save_data = get_save_data()
    save_guid = str(_save_guid())

    org_service = services.organization_service()
    org_service.clear_stored_organization_events()
    org_service.schedule_org_events()

    save_data[save_guid]['region_id'] = region_id
    write_to_settings(file_name, save_data)


def get_region_id():
    save_data = get_save_data()
    save_guid = str(_save_guid())

    settings = get_settings(save_guid, save_data)
    if settings:
        return settings['region_id']
    else:
        return 222656


def _save_guid():
    guid = services.get_persistence_service().get_save_game_data_proto().guid
    if guid:
        return guid
    else:
        return False


@injector.inject_to(Zone, 'on_loading_screen_animation_finished')
def load_settings(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)

    save_file = get_save_data()
    save_guid = str(_save_guid())

    settings = get_settings(save_guid, save_file)

    return result


def get_settings(save_guid, save_file):

    if save_guid in save_file:
        try:
            save_data = save_file[save_guid]
            return save_data
        except Exception as e:
            log('exception: {}'.format(e))
    else:
        new_save(save_guid)
        return False


def new_save(save_guid):
    save_data = get_save_data()
    if save_data:
        if save_guid not in save_data:
            save_data[save_guid] = default
            with open(os.path.join(get_save_directory(), file_name), 'w', buffering=1, encoding='utf-8') as file:
                json.dump(save_data, file, indent=4, sort_keys=True)


def get_save_data():
    with open(os.path.join(get_save_directory(), file_name)) as file:
        data = json.load(file)
        if data:
            return data
    return False


def get_save_directory():
    root_file = os.path.normpath(os.path.dirname(os.path.realpath(__file__)))
    root_file_split = root_file.split(os.sep)
    root_dir = str(os.sep).join(
        root_file_split[0:root_file_split.index('Mods')]) + os.sep + 'saves'
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    return root_dir


def write_to_settings(filename, data):
    save_directory = get_save_directory()
    with open(os.path.join(save_directory, filename), 'w', buffering=1, encoding='utf-8') as file:
        json.dump(data, file, indent=4, sort_keys=True)


def _write_to_settings(filename, data):
    save_directory = get_save_directory()
    with open(os.path.join(save_directory, filename), 'w+', buffering=1, encoding='utf-8') as file:
        json.dump(data, file, indent=4, sort_keys=True)


def update_settings(data, save):
    if str(save) not in data:
        data[str(save)] = {}
        data[str(save)]['region_id'] = 222656


def _create_new_save_file(filename, data=None):
    save_directory = get_save_directory()
    try:
        with open(os.path.join(save_directory, filename), buffering=1, encoding='utf-8') as file:
            try:
                data = json.load(file)
                return
            except JSONDecodeError:
                pass
    except FileNotFoundError:
        pass
    if data is None:
        data = {}
    with open(os.path.join(save_directory, filename), 'w', buffering=1, encoding='utf-8') as file:
        json.dump(data, file, indent=4, sort_keys=True)


def _populate_settings_proto(filename):
    try:
        save_directory = get_save_directory()
        persistence_service = services.get_persistence_service()
        save_game_proto = persistence_service.get_save_game_data_proto()
        save_guid = save_game_proto.guid
        with open(os.path.join(save_directory, filename), buffering=1, encoding='utf-8') as file:
            data = json.load(file)
            update_settings(data, str(save_guid))
        with open(os.path.join(save_directory, filename), 'w+', buffering=1, encoding='utf-8') as f:
            json.dump(data, f, indent=4, sort_keys=True)
    except Exception as e:
        sims4.log.exception('Function', '_populate_settings_proto function failure.', exc=e)


_create_new_save_file(file_name)
