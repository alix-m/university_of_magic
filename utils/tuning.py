import services
import sims4
from server_commands.tuning_commands import get_managers
from sims4 import callback_utils
from sims4.callback_utils import CallbackEvent
from sims4.localization import _create_localized_string
from sims4.resources import get_resource_key, Types

logger = sims4.log.Logger('_MagicuTuning', default_owner='lala')


def get_tuning(tuning_id):
    managers = get_managers()
    for name in managers:
        if name != 'objects':
            instance_manager = managers.get(name, None)
            key = get_resource_key(tuning_id, instance_manager.TYPE)
            tuning = instance_manager.get(key)
            if tuning:
                return tuning


def get_tuning_from_ids(resource_ids: ()):
    tuning = []
    for resource_id in resource_ids:
        tuning.append(get_tuning(resource_id))
    return tuple(tuning)


def get_string_with_tokens(string_id, *tokens):
    return lambda *_, **__: _create_localized_string(string_id)


def run_once(function):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return function(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


@run_once
def university_tuning_fixup():
    try:
        instance_manager = services.get_instance_manager(Types.UNIVERSITY)
        university = instance_manager.get(7138212260552408781)
        non_prestige_degrees = (16638230036003861568, 17576022952080021639, 14755478482111351888, 14576452643036066751, 16272640704480863433)
        prestige_degrees = (15339126893294765170, 10734878208566826997, 11201297329448829701)
        all_degrees = non_prestige_degrees + prestige_degrees

        university._all_degree_ids = all_degrees
        university._prestige_degree_ids = prestige_degrees
        university._non_prestige_degree_ids = non_prestige_degrees

        university.prestige_degrees = get_tuning_from_ids(prestige_degrees)
        university.non_prestige_degrees = get_tuning_from_ids(non_prestige_degrees)
        university.all_degrees = get_tuning_from_ids(all_degrees)

    except Exception as Argument:
        logger.error('Error during university_tuning_fixup: {}'.format(Argument))


callback_utils.add_callbacks(CallbackEvent.PROCESS_EVENTS_FOR_HOUSEHOLD_EXIT, university_tuning_fixup)
