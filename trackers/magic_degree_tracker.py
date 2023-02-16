import itertools
import random
from collections import defaultdict
import sims4
import services
from distributor.ops import GenericProtocolBufferOp
from distributor.rollback import ProtocolBufferRollback
from distributor.system import Distributor
from event_testing.resolver import SingleSimResolver
from sims.university.university_loot_ops import UniversityLootOp

from university_of_magic.resources.enums import MagicUniversityTraits
from protocolbuffers.UI_pb2 import UniversityEnrollmentData
from protocolbuffers.DistributorOps_pb2 import Operation
from sims.university.degree_tracker import DegreeTracker
from sims.university.university_enums import UniversityMajorStatus, UniversityInfoType
from sims.university.university_scholarship_tuning import ScholarshipTuning
from sims.university.university_telemetry import UniversityTelemetry
from sims.university.university_tuning import University
from sims4 import math
from sims4.resources import Types, get_resource_key\

from university_of_magic.tuning.magic_university import MagicUniversity
from university_of_magic.utils import injector
from university_of_magic.utils.tuning import get_tuning

log_file = '_magic_degree_tracker'

logger = sims4.log.Logger('_MagicDegreeTracker', default_owner='lala')


def use_magic_tracker(sim_info):
    trait_manager = services.get_instance_manager(Types.TRAIT)
    applied = trait_manager.get(get_resource_key(MagicUniversityTraits.APPLIED, Types.TRAIT))
    accepted = trait_manager.get(get_resource_key(MagicUniversityTraits.ACCEPTED, Types.TRAIT))
    current = trait_manager.get(get_resource_key(MagicUniversityTraits.CURRENT, Types.TRAIT))
    return sim_info.has_trait(applied) or sim_info.has_trait(accepted) or sim_info.has_trait(current)


@injector.inject_to(UniversityLootOp._UniversityDynamicSignView._FromSimInfo, 'get_string')
def get_string(original, self, sim_info):

    degree_tracker = sim_info.degree_tracker
    uni = self.university

    manager = services.get_instance_manager(sims4.resources.Types.UNIVERSITY_MAJOR)
    try:
        degree_ids = degree_tracker.get_available_degrees_to_enroll()[uni.guid64]

        if self.info_type == UniversityInfoType.PRESTIGE_DEGREES:
            bullet_points = (manager.get(i).display_name for i in degree_ids if i in uni.prestige_degree_ids)

    except Exception as Argument:
        logger.error('Error in UniversityLootOp._UniversityDynamicSignView._FromSimInfo - get_string(): {}'.format(Argument))

    return original(self, sim_info)


@injector.inject_to(DegreeTracker, 'process_acceptance')
def process_acceptance(original, self, send_telemetry=True):

    if send_telemetry:
        UniversityTelemetry.send_acceptance_telemetry(self._sim_info.age)

    if use_magic_tracker(self._sim_info):

        university = services.get_instance_manager(Types.UNIVERSITY)\
                     .get(MagicUniversity.tuning_id)

        for degree in university.all_degrees:
            if self.is_accepted_degree(university, degree):
                pass
            elif degree in university.prestige_degrees:
                if degree.can_sim_be_accepted(self._sim_info, degree.acceptance_score):
                    self.set_accepted_degree(university, degree)
            else:
                if degree.can_sim_be_accepted(self._sim_info, degree.acceptance_score):
                    self.set_accepted_degree(university, degree)
    else:
        original(self, send_telemetry)



@injector.inject_to(DegreeTracker, 'dropout')
def set_sim_enrolled(original, self):
    trait_manager = services.get_instance_manager(sims4.resources.Types.TRAIT)
    self._sim_info.remove_trait(trait_manager.get(MagicUniversityTraits.CURRENT))
    original(self)


@injector.inject_to(DegreeTracker, 'get_elective_course_ids')
def get_elective_course_ids(original, self, university_id):
    current_day = math.floor(services.time_service().sim_now.absolute_days())
    change_frequency = University.COURSE_ELECTIVES.elective_change_frequency
    if self._elective_timestamp is None or current_day - self._elective_timestamp >= change_frequency:
        self._elective_timestamp = current_day
        if self._elective_courses_map is None:
            self._elective_courses_map = defaultdict(list)
        resolver = SingleSimResolver(self._sim_info)
        for university in University.ALL_UNIVERSITIES:
            if university.guid64 == 7138212260552408781:
                self._elective_courses_map[university.guid64] = random.sample(MagicUniversity.electives,
                                                                              random.randint(8, 16))
            else:
                self._elective_courses_map[university.guid64] = [e.guid64 for e in
                                                                 University.generate_elective_courses(resolver)]
    return self._elective_courses_map[university_id]


@injector.inject_to(DegreeTracker, 'generate_enrollment_information')
def generate_enrollment_information(original, self, is_reenrollment=False):
    msg = UniversityEnrollmentData()
    msg.household_id = self._sim_info.household.id
    msg.is_pregnant = self._sim_info.is_pregnant

    if use_magic_tracker(self._sim_info):
        university = get_tuning(MagicUniversity.tuning_id)
        with ProtocolBufferRollback(msg.universities) as university_message:
            university_id = university.guid64
            university_message.university_id = university_id
            university_message.elective_class_ids.extend(self.get_elective_course_ids(university_id))
            for degree in university.all_degrees:
                with ProtocolBufferRollback(university_message.degrees) as degree_message:
                    degree_id = degree.guid64
                    credits_remaining = self.get_credits_remaining(university_id, degree_id)
                    major_status = self.get_major_status(university_id, degree_id)
                    degree_message.major_id = degree_id
                    degree_message.class_remaining = credits_remaining
                    degree_message.status = major_status

                    if major_status == UniversityMajorStatus.ACCEPTED:
                        core_class_ids = self.get_core_course_ids_for_enrollment(degree, university,
                                                                                 self.calculate_credits(
                                                                                     university_id,
                                                                                     degree_id),
                                                                                 credits_remaining)
                        degree_message.core_class_ids.extend(core_class_ids)

            msg.housing_zone_ids.extend(self.get_housing_zone_ids_for_enrollment())

        if is_reenrollment:
            if self._current_university is not None and self._current_major is not None:
                msg.current_enrollment = self._build_reenrollment_message()
            else:
                logger.debug(
                    'Trying to re-enroll sim {} but the current university or major is None'.format(self._sim_info))
        scholarship_manager = services.get_instance_manager(sims4.resources.Types.SNIPPET)
        merit_scholarship_info = ()
        merit_scholarship = ScholarshipTuning.MERIT_SCHOLARSHIP
        if merit_scholarship.guid64 not in self._active_scholarships:
            resolver = SingleSimResolver(self._sim_info)
            if merit_scholarship.evaluation_type.evaluation_type.get_score(self._sim_info, resolver):
                merit_scholarship_info = (merit_scholarship.guid64,)
        self._active_scholarships = list(set(self._active_scholarships))
        for scholarship_id in itertools.chain(self._active_scholarships, self._accepted_scholarships,
                                              merit_scholarship_info):
            value = scholarship_manager.get(scholarship_id).get_value(self._sim_info)
            if value is not None and value > 0:
                with ProtocolBufferRollback(msg.scholarships) as scholarship_message:
                    scholarship_message.scholarship_id = scholarship_id
                    scholarship_message.value = value

        op = GenericProtocolBufferOp(Operation.UNIVERSITY_ENROLLMENT_WIZARD, msg)
        Distributor.instance().add_op(self._sim_info, op)
    else:
        original(self, is_reenrollment)


@injector.inject_to(DegreeTracker, 'get_accepted_prestige_degrees')
def get_accepted_prestige_degrees(original, self):
    if self._accepted_degrees is None:
        return {}
    university_manager = services.get_instance_manager(sims4.resources.Types.UNIVERSITY)
    accepted_prestige_degrees = {}
    for (university_id, accepted_degree_ids) in self._accepted_degrees.items():
        university = university_manager.get(university_id)
        prestige_degree_ids = {d.guid64 for d in university.prestige_degrees}
        accepted_prestige_degrees[university_id] = set(accepted_degree_ids) & prestige_degree_ids
    return accepted_prestige_degrees