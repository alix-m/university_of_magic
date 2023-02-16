import services
import sims4
from organizations.organization_service import OrganizationService
from world.region import Region

from university_of_magic.utils import injector
from university_of_magic.tuning.magic_university import MagicUniversity
from university_of_magic.settings.save_data import get_region_id

logger = sims4.log.Logger('_UniversityOfMagic', default_owner='lala')

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


@injector.inject_to(OrganizationService, '_schedule_venue_organization_event')
def _schedule_venue_organization_event(original, self, org_drama_node, zone_id):

    def get_preferred_venue():

        region_id = get_region_id()

        org_service = services.organization_service()
        venue_service = services.venue_service()

        drama_node_manager = services.get_instance_manager(sims4.resources.Types.DRAMA_NODE)
        node_type = drama_node_manager.get(org_drama_node.guid64)

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

    if org_drama_node.guid64 in MagicUniversity.events:
        zone_id = get_preferred_venue()
    original(self, org_drama_node, zone_id)


"""
@injector.inject_to(TimedAspirationData, 'send_timed_aspiration_to_client')
def send_timed_aspiration(original, self, update_type):
    if services.current_zone().is_zone_shutting_down:
        return
    owner = self._tracker.owner_sim_info
    msg = Sims_pb2.TimedAspirationUpdate()
    msg.update_type = update_type
    msg.sim_id = owner.id
    msg.timed_aspiration_id = self._aspiration.guid64
    if update_type == Sims_pb2.TimedAspirationUpdate.ADD:
        msg.timed_aspiration_end_time = self._end_time.absolute_ticks()
    distributor = Distributor.instance()
    distributor.add_op(owner, GenericProtocolBufferOp(Operation.TIMED_ASPIRATIONS_UPDATE, msg))
"""


