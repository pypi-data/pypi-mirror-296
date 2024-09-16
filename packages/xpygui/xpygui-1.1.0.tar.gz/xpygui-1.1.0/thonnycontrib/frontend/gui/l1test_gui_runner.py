from abc import *
from thonnycontrib.backend.l1test_backend import ExceptionResponse
from thonnycontrib.frontend.l1test_runner import AbstractL1TestRunner
from thonnycontrib.utils import *
from thonnycontrib.backend.models import *
from thonnycontrib.exceptions import *
from thonnycontrib.environement_vars import *
from .views.l1test_reporter import *
from thonnycontrib.properties import *
from thonny.common import ToplevelResponse
from thonny.workbench import WorkbenchEvent
from thonny import editors
from thonnycontrib.frontend.gui.ThonnyLogsGenerator import log_in_thonny
from thonnycontrib.l1test_options import l1test_options 
from thonnycontrib.i18n.languages import tr
import thonny

@tostring
class ThonnyGuiRunner(AbstractL1TestRunner):
    """
    THis runner is responsible for handling the execution of the L1Test on the Thonny's GUI.
    `ThonnyGuiRunner` decides and invokes the `L1TestReporter` to show either the verdicts 
    or the error message.
    
    Firstly, it sends a request to the backend to evaluate the current source code. Then,
    it handles the response received from the backend and parses it. The backend
    send a response of type `TopLevelResponse` that contains results computed by the `Evaluator`.
    The results can be the verdicts if it succeed or an exception if failed. 
    
    Note: `ThonnyGuiRunner` does not deal with the construction of the views but 
    it allows to invoke the correct one.
    
    `@See the super class for more details.`
    """
    def __init__(self, reporter=None):
        super().__init__()
        self._reporter = L1TestReporter() if not reporter else reporter
        self._kw = {} # les données qui seront partagées avec le backend
        
        # Quand le backend envoie une réponse de type `ToplevelResponse``,
        # alors le TestRunner va invoquer la fonction `show_verdicts`
        thonny.get_workbench().bind("ToplevelResponse", self.handle_backend_response, True)
                
        # Quand le backend est redémarré en thonny nous invoquons la méthode 
        # `self._on_restart_backend()`
        thonny.get_workbench().bind(BACKEND_RESTART_EVENT, self._on_restart_backend, True)
        
        thonny.get_workbench().bind(EXECUTION_STATE_EVENT, self.handle_execution_state, True)
    
    def _run(self, **kw):
        """
        Run the L1Test plugin by sending a command to the l1test_backend. This method checks
        if the file is saved and if the editor is empty. If the file is not saved or the editor is empty
        then it will display an error message on the ErrorView. Otherwise, it will send a command 
        to the backend to run the tests. 
        
        The `kw` (key words arguments) is a dictionary containing
        the data to send to the backend. Each data will be serialized in bytes format.
        
        Args:
            **kw (dict): The key arguments to send to the backend. Each key/value will be 
            stored in the environnement variable (after serialization of its value).        
        """
        editor_content = self.ask_to_save_file()
        
        if not editor_content.strip():  # L'éditeur est vide. 
            # on a pas envie d'envoyer une commande au backend si le fichier est vide.
            # Dans tous les cas y a rien à tester.
            raise EmptyEditorException(tr("The editor is empty!\n"))
        
        clear_env_vars(list(self._kw.keys())) # on efface les variables d'environnement
        self.clear_kw()

        # on ajoute l'option d'importation du module dans les données à envoyer au backend
        if self._kw.get(IMPORT_MODULE_VAR) is None:
            self.add_kw(IMPORT_MODULE_VAR, l1test_options.get_option(l1test_options.IMPORT_MODULE))
        
        # si on est là alors le fichier est bien sauvegardé et contient quelque chose.
        self._request_backend(**kw)         
    
    def ask_to_save_file(self):
        """
        This function checks if the file is saved and if the editor is empty. If the file is not saved
        or the editor is empty then it will display an error message on the ErrorView.

        Args:
            editor (EditorNotebook): The editor notebook of Thonny.
        
        Raises:
            NoEditorFoundException: When no editor is opened on the workbench.
            NotSavedFileException: When the file is not saved.
        """
        editor = thonny.get_workbench().get_editor_notebook()
        # si aucun editeur n'est ouvert sur le workbench
        if not editor.get_current_editor():
            raise NoEditorFoundException(tr("No editor found !\n\nPlease open an editor before running the tests."))
        
        # cette ligne demande de sauver le fichier s'il n'a pas encore été sauvé sur
        # la machine. Si le fichier est déjà sauvé, il va permettre d'enregistrer la nouvelle
        # version du fichier.
        filename = editors.get_saved_current_script_filename(force=True)          

        # si le filename est null alors le fichier n'a  pas été sauvé sur machine.  
        # Ce cas survient quand l'utilisatur quitte la fenetre de sauvegarde sans sauver le fichier.
        if not filename: 
            msg = tr("The file is not saved.\n\nConsider to save the file before running the tests.")
            raise NotSavedFileException(msg)
        
        return editor.get_current_editor_content()
    
    def _request_backend(self, count=0, **kw):
        """Allows to execute the `L1test` magic command. 
        
        There's two cases : 
        1. if the `L1test` is invoked only one time so the command is sent to 
        backend to be executed by the thonny's runner. 
        2. if the `L1test` is invoked a lot of times (lot of clicks), then we only
        consider the first invocation (first click) of the `L1test` command. While 
        the l1test still running, the other clicks are ignored.

        Args:
            count (int, optional): The number of times this function is invoked to retry
            to send the command to the backend. Always set to 0.
            kw (dict): The key arguments to send to the backend. Each key/value will be 
            stored in the environnement variable (after serialization of its value).
        """
        treeview = self._reporter.get_treeview()
        try:
            # si le backend n'est pas en cours prêt à recevoir une commande.
            # cette vérification est nécessaire pour éviter le problème décrit 
            # dans l'issue #17 (https://gitlab.univ-lille.fr/reda.idtaleb.etu/thonny_test_framework/-/issues/17)
            if not thonny.get_runner().is_waiting_toplevel_command(): 
                raise BackendNotReadyYetException(tr("The backend is not ready yet !"))
            
            self._kw.update(kw)
            #self._kw = self._kw | kw
            getLogger(__name__).info("Data to share with backend (**kw): %s", self._kw)
            self.__send_command_to_backend()
        except BackendNotReadyYetException as e:
            # si le backend n'est pas prêt à recevoir une commande alors on
            # attend 1 seconde avant de réessayer. 
            treeview.insert_in_header(tr("Waiting for the backend to restart completely ..."), 
                                        clear=True, tags=("red"), image=STATE_RESTART_ICON)
            if count > 0: # si on a déjà essayé une fois alors on arrête
                self.terminate_running() # l'état de l'execution est terminée
                treeview.insert_in_header(str(BackendCoudntBeRestartedException()), clear=True, tags=("red"), image=STATE_ERROR_ICON)
                return 
            thonny.get_workbench().after(1000, self._request_backend, count+1, **kw) # on réessaye après 1 seconde
       
    def __send_command_to_backend(self, command_name=BACKEND_COMMAND):
        """
        Sends a command to the Thonny's backend to execute the current script.
        The name of the command must starts with a uppercase.    
        
        Any data would be shared with the backend should be stored stored in an 
        environnement variable. The handler of the command(l1test_backend) can access 
        this environnement variables.

        Note: it is recommanded to serialize the value of the environnement variable. You 
        can use the `utils.add_env_var()` function to do this.
        
        For example : 
        ```py
        utils.add_env_var("selected_line", 14) # 14 is the number of the selected line
        ```

        In the handler of the command use the `utils.get_env_var()` function to get the
        value of the environnement variable. 
        
        For example :
        ```py
        def _cmd_l1test(cmd: ToplevelCommand):         
            selected_line: int = utils.get_env_var("selected_line") # prints 14
        ```
                    
        Note : when a new command is called in Thonny it triggers a partial 
        "restart" of the backend before processing the new command. Thonny does 
        this to force stop the current process and start a new process for the 
        new command.
            
        Args:
            command_name (str): A command name , should starts with a upper case. 
            Defaults to BACKEND_COMMAND.
        """ 
        # On ajoute les données du dictionnaire kw dans les variables d'environnement
        add_env_vars(**self.get_kw()) 
        
        # Une fois que execute_current() est executée un restart backend partiel est invoqué
        # pour un nouveau processus pour la commande passé en paramètre.
        thonny.get_runner().execute_current(command_name)        
    
    def handle_backend_response(self, msg: ToplevelResponse):     
        """
        This method is binded to the `TopLevelResponse` event sent by the backend.
        
        If this method is triggered so the `msg` parameter will contain the response received 
        from the backend. Please note that the `TopLevelResponse` event is not necessary sent 
        by the l1test_backend, but it can be also sent by the Shell. The shell contains an 
        internal infinite loop that waits for commands and sends the responses periodically.
        
        This method verify the source of the `TopLevelResponse` event. If the source is 
        l1test_backend so it checks the recieved response if it contains exception or not. 
        If the response contains an exception so the according error will be displayed in 
        error view. Otherwise the response contains the verdicts of the tests and will be shown 
        on the treeview.
        
        Note: The data is deserialized before displaying it on the view.
        """   
        # On vérifie si le TopLevelRespone reçu est envoyé par le l1test_backend 
        if self._is_relevant_response(msg):
            verdicts, exception_response = self.__get_verdicts_or_error(msg)
            if not self.has_exception(): 
                self.display_verdicts_on_treeview(verdicts) 
            else: 
                self.clean_treeview()
                self.display_error_on_view(exception_response)
                self._reporter.get_treeview().insert_in_header("An error was raised please see the error view.", image=STATE_ERROR_ICON, clear=True, tags=("red"))
            self.terminate_running() # On indique l'état de l'execution du la commande comme terminée
        else:
            return # Le TopLevelReponse reçu ne nous intéresse pas.
        
    def __get_verdicts_or_error(self, msg:ToplevelResponse) -> tuple[L1TestModule, ExceptionResponse]:
        """
        Returns the l1TestModule containing the l1doctests or the error message from the received response. 
        If the response contains an exception so the error message will be returned. In this
        case the l1TestModule will be None. Reverse is true, if the response does not contain the
        error message so the l1TestModule will be returned and the error message will be None.
        
        Args:
            msg (ToplevelResponse): The received response from the backend.

        Returns:
            a tuple of (L1TestModule, error_msg)
        """
        l1TestModule: L1TestModule = None
        exception_response: ExceptionResponse = None
        self.clean_error_view()
        received_verdicts, received_exception = msg.get(VERDICTS), msg.get(L1TEST_EXCEPTION)
        if self.is_running() or received_verdicts or received_exception: # si le plugin est en cours d'execution et n'est pas en attente (càd pas de tests en cours d'execution)
            self.clean_treeview()
            if received_verdicts: # si les verdicts sont présents on les désérialize en liste de L1DocTest
                self.set_has_exception(False)
                # deserialize the verdicts
                l1TestModule = deserialize(received_verdicts)
                # log in thonny
                filter_predicate = self.get_key(FILTER_PREDICATE_VAR)                    
                self.__filter_selected_l1doctests(l1TestModule, filter_predicate)
                log_in_thonny(l1TestModule.get_l1doctests(), l1TestModule.get_filename(), self.get_key(LINENO))
            elif received_exception: # si les verdicts sont None alors c'est une exception qui a été levée par le backend
                exception_response = deserialize(received_exception)
                exception_response = self.__handle_raised_exception(exception_response)
            else:
                error = msg.get("error")
                thonny_error = "Thonny indicates `%s`. See the console." % error if error else ""
                exception_response = self.__handle_raised_exception(ExceptionResponse(Exception("Unknown error is occured. %s" % thonny_error)) )
        else:
            # si on reçoit une réponse du l1test_backend et que le plugin n'est pas en cours d'execution. Problème !
            # cela ne doit pas arriver. 
            self.set_has_exception(True)
            exception_response = ExceptionResponse(BackendCoudntBeRestartedException())
        return l1TestModule, exception_response
    
    def __filter_selected_l1doctests(self, l1TestModule:L1TestModule, filter_predicate: Callable[[L1DocTest], bool] | None):
        """
        Filters the l1doctests of the given l1TestModule by the selected line number.
        """
        if filter_predicate:
            filtered_l1doctests = l1TestModule.filter_by_predicate(filter_predicate)
            l1TestModule.set_l1doctests(filtered_l1doctests)

    def __handle_raised_exception(self, exception_info: ExceptionResponse) -> ExceptionResponse|None:
        """
        Returns the same exception response or `None` if the exception is an `InterruptedError`.
        
        Note: this function also sets the state of the execution. It set the `_has_exception`
        attribute to True if the exception is not an `InterruptedError`. Otherwise, it
        sets the `_has_exception` attribute to False.
        
        Args:
            exception_info (BackendExceptionResponse): The exception to handle.

        Returns:
            BackendExceptionResponse|None: The same exception response or None if 
            the exception is an `InterruptedError`.
        """
        if exception_info.get_type_name() == InterruptedError.__name__:
            self.set_has_exception(False)  # ce n'est pas une erreur
            self.clean_treeview()
            return None   # On fait rien.
        
        self.set_has_exception(True)   # on indique l'état de l'execution
        return exception_info
    
    def _on_restart_backend(self, event: WorkbenchEvent):
        """
        This function is called when the backend of thonny is restared. The restarting
        of the backend generates a `BackendRestart` event and this event can 
        be generated either by  the red `Stop/Restart backend` button in Thonny's 
        toolbar or by invoking a new command. 
        
        When a new command is called in Thonny it triggers a partial restart
        of the backend before processing the command. Thonny does this to stop
        the current process and start a new process for the new command.

        This function tries to verify if the backend is restarted by clicking the red button
        or by invoking the `l1test_command`. 
            - if the backend is restarted by clicking the red button, so the treeview is cleaned.
            - if the backend is restarted by invoking the `l1test_command`, so we show in the
            treeview that the l1test is being executed.
            - if the backend is restarted by invoking an other command, so nothing is done.
        
        The problem is that we cannot know who generates the `BackendRestart` event. So to know 
        if the `BackendRestart` event is generated by the `l1test_command` we use the attribute 
        `self._is_l1test_running`. This attribute was setted to True before sending the 
        `l1test_command` to the backend.
        
        Args:
            event (WorkbenchEvent): The event generated from backend restart.
        """
        if (event.get("sequence") == BACKEND_RESTART_EVENT):   
            # Quand le backend est redémarré on efface les exceptions récemment affichée par l1test 
            self.set_has_exception(False)
            self.clean_error_view() 
                        
            treeview:L1TestTreeView = self._reporter.get_treeview()
            
            # L'attribut "full" est un boolean, si c'est "True" alors le backend procède a un
            # redémarrage complet (c'est le cas quand on appuit sur le bouton rouge Stop/Restart).
            # Si c'est False alors c'est un redémarrage partiel du backend (c'est le cas d'un appel 
            # d'une nouvelle commande).
            if event.get("full"):
                self.terminate_running()
                self.clean_treeview(clear_all=True, clear_verdicts_data=True) 
            elif self.is_running(): # si le plugin a été lancé par l'utilisateur
                self.clean_treeview(clear_all=True, clear_verdicts_data=True) 
                treeview.insert_in_header(tr("Starting executing tests ..."), clear=True, tags="gray", 
                                            image=STATE_PENDING_ICON)
            else: # probablement une autre commande a déclenché le Restart du backend -> on fait rien
                pass
            self.hide_errorview_and_show_treeview()
    
    def handle_execution_state(self, msg: BackendEvent):
        """
        This function is called when an event of type InlineResponse is received. 
        This function verifies the source of the event. If the source is L1Test so it will access to the 
        received response and then it will handle the state of the execution.
        """
        def __report_execution_state_on_treeview(message: str):
            """
            Reports the execution state of the tests in the treeview. 
            
            Args:
                message (str): The message to show in the treeview.
            """
            if get_option(EXECUTION_STATE):
                self._reporter.get_treeview().insert_in_header(message, clear=True, tags="gray", image=STATE_PENDING_ICON)

        is_relevant_event = msg.get("event_type") == EXECUTION_STATE_EVENT
        if is_relevant_event:
            state:ExecutionStateEnum = ExecutionStateEnum(msg.get("state"))
            lineno = msg.get("lineno")
            match state:
                case ExecutionStateEnum.PENDING:
                    self.set_is_pending(True)
                    getLogger(__name__).info("Start evaluating test at line %s (state = %s)", lineno, state.name)
                    __report_execution_state_on_treeview(START_EXECUTION_STATE_MSG % lineno)
                case ExecutionStateEnum.FINISHED_TEST:
                    duration = msg.get("duration")
                    getLogger(__name__).info("Finished evaluating test at line %s [%s s] (state = %s)", lineno, duration, state.name)
                    __report_execution_state_on_treeview(FINISHED_EXECUTION_STATE_MSG % (lineno, duration))
                case ExecutionStateEnum.FINISHED_ALL: 
                    self.set_is_pending(False) 
                    getLogger(__name__).info("The evaluation of the tests is finished (state = %s)", state.name)
                case _:
                    getLogger(__name__).info("Unknown state : %s", state)

    def _show_error(self, exception_response: ExceptionResponse):
        self.display_error_on_view(exception_response)  
    
    def display_error_on_view(self, exception_response: ExceptionResponse, force=False, show_treeview=False):
        if self._has_exception or force:
            self._reporter.display_error_msg(str(exception_response), title=exception_response.get_title())
            self._reporter.get_error_view().show_view()   
            if show_treeview:
                self._reporter.get_treeview().show_view()
            else: 
                self._reporter.get_treeview().hide_view()
    
    def display_verdicts_on_treeview(self, l1TestModule:L1TestModule):
        if not self._has_exception:
            self._reporter.display_verdicts(l1TestModule)  
            self.hide_errorview_and_show_treeview()
    
    def hide_errorview_and_show_treeview(self):
        self._reporter.get_treeview().show_view()
        self.clean_error_view()
        self._reporter.get_error_view().hide_view()
        
    def clean_error_view(self):
        self._reporter.get_error_view().clear()
               
    def clean_treeview(self, clear_verdicts_data=False, clear_all=True, clear_errorview=False): 
        self._reporter.get_treeview().clear_tree(clear_verdicts_data=clear_verdicts_data, 
                                                 clear_all=clear_all, 
                                                 clear_errorview=clear_errorview)
        
    def get_reporter(self) -> L1TestReporter:
        return self._reporter
    
    def set_reporter(self, reporter):
        self._reporter = reporter
    
    def get_kw(self):
        return self._kw
    
    def add_kw(self, key, value):
        self._kw[key] = value

    def get_key(self, key):
        return self._kw.get(key, None)
        
    def remove_kw(self, key):
        return self._kw.pop(key, None)
    
    def clear_kw(self):
        self._kw.clear()