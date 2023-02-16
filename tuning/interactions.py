from collections import namedtuple

import enum


class SuperAffordances(enum.Int):
    SA_COMPUTER = 34920
    SA_PHONE = 13784


class MagicInteractions(enum.Int):
    PHONE_CHECK_APPLICATION = 13318276395294084126
    PHONE_DROPOUT = 9616059797818760139
    PHONE_FAMILY_CONNECTIONS = 16722490066038021261
    PHONE_CONNECTIONS_PICKER = 14632248192095777115
    COMPUTER_CANCEL_APPLICATION = 18291786069509399759
    COMPUTER_RESEARCH_UNIVERSITY = 18446236764143561031
    COMPUTER_ENROLL = 10947676970594927781
    COMPUTER_APPLY = 16998830252239547023
    COMPUTER_CHECK_APPLICATION = 3723140962179548895
    COMPUTER_CHECK_SCHOLARSHIPS = 16077879225055892942
    COMPUTER_SCHOLARSHIP_APPLY_INIT = 16166786891703093796
    COMPUTER_SCHOLARSHIP_APPLY = 17817274618964446495
    DEBUG_GET_ACCEPTANCE = 12861997377200702238


Interactions = namedtuple('Interaction', 'super_affordance_id interaction_ids')

computer_interactions = Interactions(SuperAffordances.SA_COMPUTER,
                                     (MagicInteractions.COMPUTER_CHECK_APPLICATION,
                                      MagicInteractions.COMPUTER_RESEARCH_UNIVERSITY,
                                      MagicInteractions.COMPUTER_APPLY,
                                      MagicInteractions.COMPUTER_ENROLL,
                                      MagicInteractions.COMPUTER_CANCEL_APPLICATION,
                                      MagicInteractions.COMPUTER_CHECK_SCHOLARSHIPS,
                                      MagicInteractions.DEBUG_GET_ACCEPTANCE,
                                      MagicInteractions.COMPUTER_SCHOLARSHIP_APPLY_INIT,
                                      MagicInteractions.COMPUTER_SCHOLARSHIP_APPLY,
                                      10393526785282682089))

phone_interactions = Interactions(SuperAffordances.SA_PHONE,
                                  (MagicInteractions.PHONE_DROPOUT,
                                   MagicInteractions.PHONE_CHECK_APPLICATION,
                                   MagicInteractions.PHONE_CONNECTIONS_PICKER,
                                   MagicInteractions.PHONE_FAMILY_CONNECTIONS))

