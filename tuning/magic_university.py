import random
import sims4

from sims.university.university_tuning import University
from sims4.utils import classproperty

from university_of_magic.utils.logging.logger import log
from university_of_magic.resources.enums import MagicDegrees
from university_of_magic.utils.tuning import get_tuning, get_tuning_from_ids
from university_of_magic.resources.enums import MagicHouses, MagicEvents

logger = sims4.log.Logger('_MagicUniversityTuning', default_owner='lala')


class MagicUniversity():

    tuning_id = 7138212260552408781

    _all_degrees = None
    _prestige_degrees = None
    _non_prestige_degrees = None
    _organizations = None
    _preferred_region = None

    @classproperty
    def preferred_region(self):
        if self._preferred_region is None:
            log('setting _preferred_region')
            self._preferred_region = 8086
        return self._preferred_region

    @classproperty
    def all_degrees(self):
        if self._all_degrees is None:
            self._all_degrees = self.prestige_degrees + self.non_prestige_degrees
        return self._all_degrees

    @classproperty
    def prestige_degrees(self):
        if self._prestige_degrees is None:
            self._prestige_degrees = get_tuning_from_ids(self.prestige_degree_ids)
        return self._prestige_degrees

    @classproperty
    def non_prestige_degrees(self):
        if self._non_prestige_degrees is None:
            self._non_prestige_degrees = get_tuning_from_ids(self.magic_non_prestige_degree_ids)
        return self._non_prestige_degrees

    @classproperty
    def organizations(self):
        if self._organizations is None:
            self._organizations = get_tuning_from_ids(self.organization_ids)
        return self._organizations

    @classproperty
    def events(self):
        return self.event_ids

    def get_electives(self):
        elective_map = []
        magic_electives = random.sample(self.electives, random.randint(8, 16))
        base_elective = University.COURSE_ELECTIVES.electives[0]

        for e in magic_electives:
            elective_map.append(base_elective.clone_with_overrides(elective=get_tuning(e)))

    electives = [
        12617456816470198050, 16305101354452387968, 15551234497199504996, 15838172403599200534,
        10408675437196365632, 18215348235782083255, 14205449886214830054, 11603772426135162762,
        12921895010483023036, 11270125608250660528, 9766034485691356760, 12093531425766082599,
        16802592135848751467, 10492050688426629392, 12554077857225050439, 18398711949616261269,
        17582165425512909174, 12767083510949868615, 16558489566651108811, 11945040599184184836,
        16347906117746966607, 12030379748053908378, 14884721275655197114, 15051656939573458070,
        16571916828216598167, 11874789369250908957, 9306343787008939789, 13144683931828910381,
        13223388206467935294, 10545235502318617508, 14787008436232667621, 13171246285854037214,
        12647506306469308712, 12712248648135887341, 14091767986226809867, 12620950391802479438]

    event_ids = [MagicEvents.HOGSNIFFLE_BARNIGHT, MagicEvents.GRIZZLEGAT_BARNIGHT,
                 MagicEvents.ROOKWING_BARNIGHT, MagicEvents.SNIVELEYE_BARNIGHT]

    scholarships = [16054557989361394956]

    mundane_universities = [219732, 219731]

    organization_ids = [MagicHouses.HOGSNIFFLE, MagicHouses.GRIZZLEGAT, MagicHouses.ROOKWING, MagicHouses.SNIVELEYE]

    magic_non_prestige_degree_ids = (
        MagicDegrees.ALCHEMY,
        MagicDegrees.CHARMS,
        MagicDegrees.DIVINATION,
        MagicDegrees.HISTORY_OF_MAGIC,
        MagicDegrees.MUGGLE_STUDIES)

    prestige_degree_ids = (
        MagicDegrees.DATDA,
        MagicDegrees.DARK_ARTS,
        MagicDegrees.MAGIBIOLOGY)
