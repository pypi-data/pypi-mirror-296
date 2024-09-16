from thonnycontrib.i18n.languages import tr
from thonny import get_workbench
import thonnycontrib.i18n.languages as languages

if get_workbench(): # si l'éditeur est prêt alors on change la langue du translateur.
    languages.set_language(get_workbench().get_option("general.language"))

PLUGIN_NAME = "L1Test"
ERROR_VIEW_LABEL = '%s errors' % PLUGIN_NAME

# ici vous pouvez changer la syntaxe du doctest. 
# version 2022 PJI : Actuellement on garde la syntaxe `$py`.
L1TEST_SYMBOL = "[$]py"
# version 2022 avant la rentrée
L1TEST_SYMBOL1 = "[$][$][$]"
L1TEST_SYMBOL2 = "[$]PY"
L1TEST_SYMBOL3 = "[$]py"
# L'invite des tests qui vérifient la levée d'exception
L1TEST_EXCEPTION_SYMBOL = "[$][$]e"
L1TEST_PROCEDURE_SYMBOL = "[$][$]p"

# ############################################################################################### #
#                       LES NOUVELLES VARIABLES VERSION 2023 PFE                                  #
# ############################################################################################### #

# Le nom de la commande magique pour l1test(doit toujours commencer par une majuscule)
BACKEND_COMMAND = "L1test"

# Le nom de l'event qui lance le redémarrage du backend thonny
BACKEND_RESTART_EVENT = "BackendRestart"
EXECUTION_STATE_EVENT = "ExecutionStateResponse"

# ############ Les noms des clés du dictionnaire renvoyé par le l1test_backend ############
# Le nom de l'attribut contenant les résulats des tests renvoyés par l1test_backend
VERDICTS = "verdicts"
# Le nom de l'attribut contenant une exception levée et renvoyée par l1test_backend
L1TEST_EXCEPTION = "l1test_exception"
# Le nom de l'attribut contenant le numéro de la ligne sélectionnée
SELECTED_LINENO = "selected_lineno"

# ############ Les labels des buttons du menu l1test treeview ############
PLACE_RED_TEST_ON_TOP_LABEL = tr("Place the red tests on the top")
SHOW_ONLY_RED_TESTS = tr("Show only red tests")
RESTORE_ORIGINAL_ORDER = tr("Restore original order")
EXPAND_ALL = tr("Expand all functions")
FOLD_ALL = tr("Fold all functions")
UPDATE_FONT_LABEL = tr("Update the font")
INCREASE_SPACE_BETWEEN_ROWS = tr("Inrease row height")
DECREASE_SPACE_BETWEEN_ROWS = tr("Decrease row height")
WORD_WRAP = tr("Word wrap")
CLEAR = tr("Clear")

# Le message affiché sur la treeview quand `l1test` est en cours d'execution
START_EXECUTION_STATE_MSG = tr("Start evaluating test at line %s")
FINISHED_EXECUTION_STATE_MSG = tr("Finished evaluating test at line %s (executed in %s s)")

# Le message affiché sur la treeview quand il n'existe aucun test
NO_TEST_FOUND_MSG = tr("No test found !")

# The title of the error view when the docstring genertor shows the raised error
CANNOT_GENERATE_THE_DOCSTRING = tr("Cannot generate the docstring :")
# The title of the error view when the l1test shows the raised error
CANNOT_RUN_TESTS_MSG = tr("Cannot run %s :")%(PLUGIN_NAME)

# -------------------------------------- Les images utilisées par le plugin ------------------------------------------------------
BTN_L1TEST = "btn_l1test.png" # image du boutton l1test
BTN_RERUN_FAILURES = "btn_rerun_failures.png"
BTN_MENU_TREEVIEW = "btn_menu_treeview.png"

STATE_PENDING_ICON = "state_pending.png" # icone qui indique que les tests sont en cours d'évaluation
STATE_ERROR_ICON = "state_error.png"  # icone qui indique qu'une erreur est survenue lors de l'évaluation des tests
STATE_RESTART_ICON = "state_restart.png"  # icone qui indique que le backend est en cours de redémarrage

CHIP_RED = "chip_red.png" # le petit cercle rouge qui précède un test qui a échoué
CHIP_EXCEPTION = "chip_exception.png" # le petit cercle rouge (avec un poitn d'exclamation) qui précède un test qui a échoué
CHIP_GREEN = "chip_green.png" # le petit cercle vert qui précède un test qui a réussi

MENU_FILTER_TESTS = "menu_filter_red_tests.png"
MENU_SORT_RED_TESTS = "menu_sort_by_red_tests.png"
MENU_RESTORE_ORIGINAL_ORDER = "menu_restore_original_order.png"
MENU_FOLD_ROWS = "menu_fold_rows.png"
MENU_EXPAND_ROWS = "menu_expand_rows.png"
MENU_POLICE = "menu_police.png"
MENU_CLEAR = "menu_clear.png"
MENU_INCREASE_ROW_HEIGHT = "menu_increase.png"
MENU_DECREASE_ROW_HEIGHT = "menu_decrease.png"

BOX_CHECKED = "box_checked.png"
BOX_UNCHECKED = "box_unchecked.png"
