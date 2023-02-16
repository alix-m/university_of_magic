from university_of_magic.utils.logging.logger import log

import services
from sims import sim_info
from sims4.localization import _create_localized_string, LocalizationHelperTuning
from ui.ui_dialog import UiDialog, UiDialogResponse, ButtonType


def show_menu():
    client = services.client_manager().get_first_client()

    def get_inputs_callback(dialog):
        if not dialog.accepted:
            log("Dialog was closed/cancelled")
            return
        log("Dialog was accepted")

    btn_title = lambda **_: _create_localized_string(2910527622)
    btn_desc = lambda **_: _create_localized_string(2910527622)
    localized_text = lambda **_: LocalizationHelperTuning.get_raw_text(
        "Organization Tiers")
    localized_exit = lambda **_: _create_localized_string(2910527622)

    dialog = UiDialog.TunableFactory().default(client.active_sim, text=localized_text, title=btn_title)

    responses = list()
    responses.append(UiDialogResponse(dialog_response_id=ButtonType.DIALOG_RESPONSE_CANCEL, text=localized_exit,
                                      ui_request=UiDialogResponse.UiDialogUiRequest.NO_REQUEST))

    dialog.add_listener(get_inputs_callback)
    dialog.set_responses(responses)
    dialog.show_dialog()

