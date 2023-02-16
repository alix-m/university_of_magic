import services
import sims4

from sims4.resources import Types
from world.region import Region

from university_of_magic.utils.tuning import get_tuning
from university_of_magic.settings.save_data import update_preferred_region
from university_of_magic.tuning.magic_university import MagicUniversity
from university_of_magic.settings.save_data import get_region_id


logger = sims4.log.Logger('_MagicuDebug', default_owner='lala')


def get_premade_tuning(name):
    premade_sims = {
        'septimus': 12550360875999510183,
        'proserpine': 13875767949476076371,
        'artemis': 11057108383394242347,
        'aslan': 15561802839583287570}
    return get_tuning(premade_sims[name])


@sims4.commands.Command('magicu.make_premade_household', command_type=sims4.commands.CommandType.Live)
def _get_magic_resources(name, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    sim_tuning = get_premade_tuning(name)
    sim_tuning.create_premade_household()


@sims4.commands.Command('magicu.settings', command_type=sims4.commands.CommandType.Live)
def _get_magic_settings(_connection=None):
    output = sims4.commands.CheatOutput(_connection)

    logger.info('hi')
    output('hello')


@sims4.commands.Command('magicu.start', command_type=sims4.commands.CommandType.Live)
def _start(_connection=None):
    output = sims4.commands.CheatOutput(_connection)

    region_id = get_region_id()
    output(region_id)


@sims4.commands.Command('magicu.region', command_type=sims4.commands.CommandType.Live)
def _get_preferred_region_id(_connection=None):
    output = sims4.commands.CheatOutput(_connection)

    org_service = services.organization_service()

    event = services.get_instance_manager(Types.DRAMA_NODE) \
        .get(MagicUniversity.events[1])

    def get_preferred_venue():

        region_id = get_region_id()

        org_service = services.organization_service()
        venue_service = services.venue_service()

        drama_node_manager = services.get_instance_manager(sims4.resources.Types.DRAMA_NODE)
        node_type = drama_node_manager.get(event.guid64)

        event_venue_tuning = org_service.get_organization_venue_tuning(node_type)
        region = Region.REGION_DESCRIPTION_TUNING_MAP.get(region_id)
        logger.debug('scheduling events using preferred region: {}'.format(region_id), owner='Lala')
        preferred_zone_ids = venue_service.get_zones_for_venue_type_gen(event_venue_tuning,
                                                                        compatible_region=region,
                                                                        ignore_region_compatability_tags=True)
        preferred_zone = ''
        for z in preferred_zone_ids:
            preferred_zone = z
        return preferred_zone

    zone_id = get_preferred_venue()
    org_service._schedule_venue_organization_event(event, zone_id)

    region_id = get_region_id()
    output(str(region_id))
    output('ok')


@sims4.commands.Command('magicu.set_event_world', command_type=sims4.commands.CommandType.Live)
def _get_magic_settings(world_name, _connection=None):
    output = sims4.commands.CheatOutput(_connection)

    region_descriptions = {
        'sanmyshuno': 117425,
        'forgottenhollow': 146196,
        'oasissprings': 15740,
        'brindletonbay': 160112,
        'delsolvalley': 197663,
        'stangerville': 201699,
        'sulani': 216823,
        'britechester': 221598,
        'glimmerbrook': 222656,
        'evergreenharbor': 235805,
        'mtkomorebi': 246370,
        'henfordonbagley': 263602,
        'tartosa': 287506,
        'willowcreek': 8086,
        'newcrest': 93517,
        'windenburg': 99995
    }

    if world_name in region_descriptions:
        output(world_name)
        region_id = region_descriptions[world_name]
        update_preferred_region(region_id)
        output('k')
    else:
        output('World named "{}" not found'.format(world_name))
