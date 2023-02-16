import services
import sims4
from sims.sim import Sim
from sims4.resources import Types
from sims4.tuning.instance_manager import InstanceManager
from university_of_magic.utils import injector
from university_of_magic.tuning.interactions import computer_interactions, phone_interactions

logger = sims4.log.Logger('_UniversityOfMagicInteractions', default_owner='lala')


def add_interactions_by_sa(self, super_affordance_id, interaction_ids):
    try:
        affordance_manager = services.get_instance_manager(Types.INTERACTION)
        super_affordance = affordance_manager.get(super_affordance_id)
        if super_affordance is None or interaction_ids is None:
            return
        for (key, cls) in self._tuned_classes.items():
            if hasattr(cls, 'guid64') and hasattr(cls,
                                                  '_super_affordances') and super_affordance in cls._super_affordances:
                interactions = map(lambda interaction_id: affordance_manager.get(interaction_id), interaction_ids)
                to_add = filter(lambda interaction: interaction is not None, interactions)
                cls._super_affordances = cls._super_affordances + tuple(to_add)
    except Exception as e:
        raise Exception(f'Error injecting by affordance in University of Magic: {str(e)}')


@injector.inject_to(InstanceManager, 'load_data_into_class_instances')
def add_interactions(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    if self.TYPE == Types.OBJECT:
        add_interactions_by_sa(self, computer_interactions.super_affordance_id,
                               computer_interactions.interaction_ids)
    return result


@injector.inject_to(Sim, 'on_add')
def add_phone_interactions(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    interactions = phone_interactions.interaction_ids
    if interactions is None:
        return result
    new_interactions = []
    affordance_manager = services.get_instance_manager(Types.INTERACTION)
    for new_id in interactions:
        interaction = affordance_manager.get(new_id)
        if interaction is not None:
            new_interactions.append(interaction)
    self._phone_affordances += tuple(new_interactions)
    return result
