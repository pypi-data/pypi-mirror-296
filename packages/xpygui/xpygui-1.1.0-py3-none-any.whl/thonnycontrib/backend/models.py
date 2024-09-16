from collections import namedtuple
from enum import Enum

from thonnycontrib.environement_vars import IS_GUI_MODE_VAR
from thonnycontrib.i18n.languages import tr
from .verdicts.ExceptionVerdict import ExceptionVerdict
from .verdicts.FailedVerdict import FailedVerdict
from .verdicts.ExampleVerdict import ExampleVerdict
from ..utils import build_event_msg, get_env_var, tostring
from typing import Callable, List, Tuple
from .doctest_parser import Example
import time
from thonny.common import BackendEvent
from thonnycontrib import backend
from thonnycontrib.backend import get_event_manager

r"""
Ce module contient les modèles d'objets créé pendant la phase du parsing du code source.
- Un `L1Doctest` représente une docstring d'un noeud ast et possède un ensemble d'exemples 
(ie. les tests) déclarés dans la docstring. les exemples sont représentés par la classe 
abstraite `Example` créé par le parser Doctest sous-jacent (le modèle Example n'est pas 
déclaré dans ce module. Voir le module doctests.py.). 
- Le L1DoctestFlag est une énumération qui représente le verdict global d'un L1Doctest. 
Un verdict gloabl est calculé après l'évaluation de tous les exemples du L1Doctest.
- Un `L1ModuleTest`est un ensemble de `L1Doctest` contenus dans un module.

Ces objets sont créés par le `L1DocTestParser` qui est responsable du parsing des méthodes 
et des classes d'un module. Les classes Examples sont créés via le parser Doctest sous-jacent
responsable du parsing des docstrings des méthodes et des classes.
"""

# Un objet qui représente le résumé des résultats de l'exécution des tests.
Summarize = namedtuple('Summarize', ["total", "success", "failures", "errors", "empty"])

class EventManager():
    """
    Class that allows to manage the events that are sent by the backend.
    Used to send the state of the execution of the tests.
    """
    def __init__(self):
        backend._event_manager = self
        self._is_gui_mode = get_env_var(IS_GUI_MODE_VAR)

        from thonnycontrib.frontend.l1test_runner import AbstractL1TestRunner
        self._listeners: List[AbstractL1TestRunner] = []

    def send_message(self, message: BackendEvent):
        """
        Send a message to all the listeners.
        """
        if self._is_gui_mode:
            from thonnycontrib.backend.l1test_backend import BACKEND 
            BACKEND.send_message(message)
        else:
            for listener in self._listeners:
                listener.handle_execution_state(message)

    def add_listener(self, listener):
        """
        Add a listener that will receive the messages.

        Args:
            listener (AbstractL1TestRunner): The listener to add.
        """
        self._listeners.append(listener)

    def remove_listener(self, listener):
        """
        Remove a listener.

        Args:
            listener (AbstractL1TestRunner): The listener to remove.
        """
        self._listeners.remove(listener)

    def clear_listeners(self):
        """
        Remove all the listeners.
        """
        self._listeners.clear()


class ExecutionStateEnum(Enum):
    """
    This enum represents the execution state of the tests:
    - `PENDING`: this state indicates that an Example (a test) is still evaluating. This state is sent for each Example (as test).
    - `FINISHED_TEST`: this state indicates that the Evaluator has finished evaluating the current Example (test). This state is sent after each Example (test).
    - `FINISHED_ALL`: this state indicates that the Evaluator has finished it's job and all the evalutions are done. This state is sent after all the evaluation.
    """
    PENDING = 0 
    FINISHED_TEST = 1 
    FINISHED_ALL = 2 

class L1DocTestFlag(Enum):
    """
    This enum represents the flag of a L1DocTest. The flag is the global 
    verdict of the L1DocTest.
    
    The flag can be one of the following: 
    - `FAILED`: The L1DocTest contains at least one failed/error test.
    - `EMPTY`: The L1DocTest is empty. It contains only setups or has no tests. 
    - `PASSED`: The L1DocTest contains only passed tests.
    """
    FAILED = -1
    EMPTY = 0
    PASSED = 1
    
    def from_value(value: int):
        """
        This method returns the flag corresponding to the given value. 
        The value must be one of the following: [-1, 0, 1]. Otherwise, a ValueError is raised.
        """  
        enum_types = [e for e in L1DocTestFlag]
        find = [e for e in enum_types if value == e.value]
        if not find:
            raise ValueError(f"The value must be one of the following: {[t.value for t in enum_types]}")

        return find[0]    
               
    def get_gui_format(self):
        """This method returns the icon corresponding to the flag."""
        if self.value == -1:
            return "verdict_failed.png"
        elif self.value == 0:
            return "verdict_warning.png"
        else:
            return "verdict_passed.png"
    
    def get_cli_format(self):
        """This method returns the icon corresponding to the flag."""
        if self.value == -1:
            return "❌ " # "☒ "
        elif self.value == 0:
            return "⚠️  " # "☐ "
        else:
            return "✅ " # "☑ "
    
    def get_color(self, cli_mode=False):
        """This method returns the color corresponding to the flag."""
        if self.value == -1:
            return "red"
        elif self.value == 0:
            return "orange" if not cli_mode else "orange3"
        else:
            return "green"
        
    def short_name(self):
        """This method returns the text corresponding to the flag."""
        if self.value == -1:
            return "Failed"
        elif self.value == 0:
            return "Empty"
        else:
            return "Passed"
    
    def is_failing(self):
        """
        Return True if the flag is `FAILED`. Otherwise, returns False.
        """
        return self.value == -1 
    
    def __eq__(self, o: object) -> bool:
        if not isinstance(o, L1DocTestFlag):
            return False
        return self.value == o.value

@tostring
class L1DocTest():
    """
    An `L1DocTest` corresponds to an ast node and that groups its tests 
    containing in the docstring of that node. A `L1DocTest` contains a list of 
    the examples of type `Example`. 
    
    Each L1DocTest is defined by the following attributes:
    - `l1ModuleTest`: The L1ModuleTest that contains the L1Doctest.
    - `name`: The name of the ast node which is represented by the L1Doctest.
            The name is the signature of the function or the class.
    - `type`: The type of the ast node which is represented by the L1Doctest.
    - `node_lineno`: The line number of the associated ast node.
    - `start_lineno`: The start line number of the docstring of the function/class.
    - `end_lineno`: The end line number of the docstring of the function/class.
    - `examples`: The list of the examples of the L1Doctest.
    - `flag`: The global verdict of the L1Doctest. Set as None while the 
              l1doctest is not evaluated.
    
    When a `L1DocTest` is created by the `L1TestAstParser` it is not evaluated. 
    Its global verdict (see `get_flag()`) will be `None` until it's evaluated. 
    Its `Example` are not evaluated too and thier verdicts are setted as `None`. 
    To evaluate a `L1DocTest` you should call the `evaluate()` method. Then all 
    the examples will be evaluated and the global verdict of the l1doctest will 
    be setted.
    
    Args:
        l1ModuleTest (L1ModuleTest): The L1ModuleTest that contains the L1Doctest.
        This is useful to know the context of the L1Doctest.
        name (str):  The name of the ast node which is associated to the L1Doctest.
        type (str): The type of the ast node which is associated to the L1Doctest. 
        related to one value reported in `SUPPORTED_TYPES` constant.
        node_lineno (int): The line of the associated ast node.
    """
    def __init__(self, l1ModuleTest, name:str, type:str, node_lineno:int) -> None:
        self.__l1ModuleTest = l1ModuleTest
        self.__name = name
        self.__type = type
        self.__node_lineno = node_lineno
        self.__start_lineno = -1
        self.__end_lineno = -1
        self.__examples:List[Example] = []
        self.__flag: L1DocTestFlag = None  # The global verdict of the l1doctest. 
                                           # Set as None while the l1doctest is not evaluated.
                                           
    
    def evaluate(self, globs:dict):
        """
        Evaluate the examples of this L1Doctest. Each example is evaluated and its 
        verdict is setted. The global verdict of the L1Doctest is also setted and you
        could access it by calling the method L1Doctest.get_flag().
        
        Args:
            globs (dict): The globals of the module in wich the L1Doctest is defined.
        Returns:
            L1DocTestFlag: The global verdict of the L1Doctest.
        """
        for example in self.get_examples(): 
            get_event_manager().send_message(build_event_msg(state=ExecutionStateEnum.PENDING, lineno=example.lineno))
            
            start = time.perf_counter()
            example.compute_and_set_verdict(globs) 
            end = time.perf_counter() - start

            duration = round(end, 4)
            get_event_manager().send_message(build_event_msg(state=ExecutionStateEnum.FINISHED_TEST, lineno=example.lineno, duration=duration))
        self.__flag = self._compute_global_flag() # set the global verdict of the l1doctest 
        return self.__flag
        
    def _compute_global_flag(self) -> L1DocTestFlag:
        """
        This method should be invoked after the evaluation (evaluate_examples() method) 
        of the l1doctest. It returns a flag that represents the global verdict of the L1Doctest.
        
        Returns:
            L1DocTestFlag: returns a flag that represents the global 
            verdict of the l1doctest. 
        """
        assert all(ex.is_evaluated() for ex in self.__examples) # assure that all the examples are evaluated
        if not self.has_examples():
            return L1DocTestFlag.EMPTY
        elif self.has_only_setUps() and all([ex.get_verdict().isSuccess() for ex in self.__examples]):
            return L1DocTestFlag.EMPTY
        elif all([ex.get_verdict().isSuccess() for ex in self.__examples]):
            return L1DocTestFlag.PASSED
        else:
            return L1DocTestFlag.FAILED
    
    ## Stats methods ##
    def count_tests(self):
        """
        Count the number of the tests containing in this L1doctest. The setups
        are not considered in the counting.
        
        Returns:
            int: the number of the tests containing in the l1doctest.
        """ 
        return len(self.get_test_examples()) 
    
    def count_setups(self):
        """
        Count the number of the setups containing in this L1doctest. The tests
        are not considered in the counting.
        
        Returns:
            int: the number of the setups containing in the l1doctest.
        """ 
        return len(self.get_setup_examples())
    
    def count_passed_tests(self):
        """Count the number of passed tests. Return `None` if the L1Doctest is not evaluated."""
        if not self.is_evaluated():
            return None
        return sum([1 for ex in self.__examples if ex.is_a_test() and ex.get_verdict().isSuccess()])
    
    def count_failed_tests(self):
        """Count the number of failed tests. Return `None` if the L1Doctest is not evaluated."""
        if not self.is_evaluated():
            return None
        return sum([1 for ex in self.__examples if not ex.get_verdict().isSuccess() and isinstance(ex.get_verdict(), FailedVerdict)])
    
    def count_error_tests(self):
        """
        Count the number of tests that raised an exception.
        Return `None` if the L1Doctest is not evaluated
        """
        if not self.is_evaluated():
            return None
        return sum([1 for ex in self.__examples if not ex.get_verdict().isSuccess() and isinstance(ex.get_verdict(), ExceptionVerdict)])
    
    ## Sorting/filtering methods ##
    def sort_examples_by_verdicts(self, key: Tuple[ExampleVerdict, ...], reverse=True):
        """
        Sort the examples of this L1Doctest by the given key. The key is a tuple of `ExampleVerdict`.
        This method set the examples of this L1Doctest as the sorted examples.
        """
        sorted_example = sorted(self.get_examples(), key=lambda x: isinstance(x.get_verdict(), key), reverse=reverse)
        self.set_examples(sorted_example)
    
    def filter_examples_by_verdicts(self, key: Tuple[ExampleVerdict, ...]):
        """
        Filter the examples of this L1Doctest by the given key. The key is a tuple of `ExampleVerdict`.
        
        Return self if the L1Doctest has no examples. Otherwise, return a new L1Doctest that contains
        only the examples that match the given key.
        """
        filtered_examples = [ex for ex in self.get_examples() if isinstance(ex.get_verdict(), key)]
        l1doctest = L1DocTest(self.get_l1ModuleTest(), self.get_name(), self.get_type(), self.get_node_lineno(), self.get_start_lineno(), self.get_end_lineno())
        l1doctest.set_examples(filtered_examples)
        return l1doctest
    
    ## Check methods ##
    def is_evaluated(self):
        """Returns True if the L1Doctest is evaluated. Otherwise, returns False."""
        return bool(self.__flag)
    
    def has_examples(self):
        """
        Returns:
            bool: Returns True if this `L1Doctest` contains at least one `Example`. 
            Otherwise, returns False.
        """
        return len(self.__examples) > 0
    
    def has_only_tests(self):
        """ 
        Return True if this L1Doctest contains only tests. Otherwise, returns False.
        """
        return self.count_tests() > 0 and self.count_tests() == len(self.__examples)
    
    def has_only_setUps(self):
        """
        Return True if this L1Doctest contains only setups. Otherwise, returns False.
        """
        return self.count_setups() > 0 and self.count_setups() == len(self.__examples)
    
    def has_flag(self, flag: L1DocTestFlag):
        """
        Return True if the l1doctest has the given flag.
        
        Args: 
            - flag (L1DocTestFlag): the flag
        """
        assert isinstance(flag, L1DocTestFlag)
        return self.__flag == flag
    
    def is_passing(self):
        """
        Return True if the l1doctest is passing. Otherwise, returns False.
        """
        return self.has_flag(L1DocTestFlag.PASSED)
    
    def is_failing(self):
        """
        Return True if the l1doctest is failing. Otherwise, returns False.
        """
        return self.has_flag(L1DocTestFlag.FAILED)
    
    def is_empty(self):
        """
        Return True if the l1doctest is empty. Otherwise, returns False.
        """
        return self.has_flag(L1DocTestFlag.EMPTY)
    
    ## Add and remove methods ##
    def add_example(self, example:Example):
        """
        Add an example to the L1Doctest.

        Args:
            example (Example): The example to add.
        """
        self.__examples.append(example)
        
    def remove_example(self, example:Example):
        """
        Remove an example from the L1Doctest.

        Args:
            example (Example): The example to remove.
        """
        self.__examples.remove(example)
    
    ## Utils methods ##
    def get_test_examples(self):
        """
        Return a list of the tests of this L1Doctest.
        """
        return [ex for ex in self.__examples if ex.is_a_test()]
    
    def get_setup_examples(self):
        """
        Return a list of the setups of this L1Doctest.
        """
        return [ex for ex in self.__examples if not ex.is_a_test()]
    
    def get_verdict_from_example(self, example:Example) -> ExampleVerdict:
        """
        Return the verdict of the given example. Return None if the example is not found.
        """
        found_example = self.__get_example(example.lineno)
        return found_example.get_verdict() if found_example else None
    
    def __get_example(self, lineno:int) -> Example:
        """
        Return the example that has the given lineno. 
        Return None if the example is not found.
        """
        found = [ex for ex in self.__examples if ex.lineno == lineno]
        return found[0] if found else None
    
    def get_ui_name(self, inline:bool=True):
        """
        Get a string that contains the name of that l1doctest and how many tests are passed. 
        If the l1docstest is empty, returns only the name of the l1doctest.
        
        Note : is that l1doctest is not evaluated yet returns only its name.
        """
        if self.is_evaluated():
            space = " " if inline else ""
            # The first space is necessary so that all text will be aligned
            if self.is_empty():
                return "%s%s" % (space, self.get_name())
            return "%s%s ~ %s/%s %s" % (space, 
                                        self.get_name(), 
                                        self.count_passed_tests(), 
                                        self.count_tests(),
                                        tr("passed"))
        return self.get_name()
    
    def __eq__(self, o: object) -> bool:
        if not isinstance(o, L1DocTest):
            return False
        return (self.get_node_lineno() == o.get_node_lineno() and 
                self.get_type() == o.get_type() and 
                self.get_name() == o.get_name() and 
                self.get_start_end_lineno() == o.get_start_end_lineno() and 
                self.get_examples() == o.get_examples())

    ## Getters and Setters ##
    def get_node_lineno(self):
        """Return the line number of the node of the L1Doctest. 
        The node is the function or the class associated to the L1Doctest. """
        return self.__node_lineno
    
    def get_examples(self):
        return self.__examples
    
    def set_examples(self, examples:List[Example]):
        self.__examples = examples
    
    def get_name(self):
        """Return the name of the L1Doctest. The name is the name of the function or the class."""
        return self.__name
    
    def get_start_end_lineno(self) -> Tuple[int, int]:
        """Return the start and the end line number of the docstring of the L1Doctest."""
        return (self.__start_lineno, self.__end_lineno)

    def get_start_lineno(self):
        """Return the start line number of the docstring of the L1Doctest.""" 
        return self.__start_lineno
    
    def set_start_lineno(self, start_lineno):
        self.__start_lineno = start_lineno
    
    def get_end_lineno(self):
        """Return the end line number of the docstring of the L1Doctest."""
        return self.__end_lineno
    
    def set_end_lineno(self, end_lineno):
        self.__end_lineno = end_lineno
        
    def get_flag(self):
        """Return the flag of the L1Doctest. The flag is the global verdict of the L1Doctest."""
        return self.__flag
    
    def get_type(self):
        """Return the type of the L1Doctest. The type is the type of the node of the L1Doctest."""
        return self.__type
    
    def set_type(self, type):
        self.__type = type   
   
    def get_filename(self):
        return self.__l1ModuleTest.get_filename() 

    def get_source(self):
        return self.__l1ModuleTest.get_source()     

@tostring
class L1TestModule():
    """
    An `L1ModuleTest` is a set of `L1Doctest` that are contained in the same module.
    
    The `L1ModuleTest` is defined by the following attributes:
    - `filename`: The name of the file in which the tests are extracted.
    - `l1doctests`: The list of the L1Doctest that are contained in the module.
    - `representer`: The representer that will be used to represent the L1ModuleTest in the UI.
    """
    
    def __init__(self, filename:str="", source="", l1doctests:List[L1DocTest]=[]) -> None:
        self.__filename = filename
        self.__source = source
        self.__l1doctests = l1doctests
    
    def evaluate(self, globs:dict):
        """
        Evaluate all the L1Doctests that are contained in this L1ModuleTest.
        
        Args:
            globs (dict): The globals of the module in wich the L1ModuleTest is defined.

        Returns:
            List[L1Doctest]: The list of the evaluated L1Doctests that are contained in this L1ModuleTest.
        """
        for l1doctest in self.get_l1doctests():
            globs = globs.copy() # copy the globals to avoid side effects. Each l1doctest has its own globals.
            l1doctest.evaluate(globs)
                
        get_event_manager().send_message(build_event_msg(state=ExecutionStateEnum.FINISHED_ALL))
        return self.get_l1doctests()       

    def add_l1doctest(self, l1doctest: L1DocTest):
        self.__l1doctests.append(l1doctest)
        
    def remove_l1doctest(self, l1doctest: L1DocTest):
        self.__l1doctests.remove(l1doctest)
        
    def count(self):
        """ Count the number of L1Doctests that are contained in this L1ModuleTest."""
        return len(self.__l1doctests)
    
    def has_l1doctests(self):
        """
        Return True if this L1ModuleTest contains at least one L1Doctest. Otherwise, returns False.
        """
        return self.count() > 0
    
    def filter_by_predicate(self, predicate:Callable[[L1DocTest], bool]):
        """
        Filter the L1Doctests that are contained in this L1ModuleTest by the given predicate.
        
        Args:
            predicate (Callable[[L1DocTest], bool]): the predicate to be used to filter the L1Doctests.
        """
        return [l1doctest for l1doctest in self.__l1doctests if predicate(l1doctest)]

    def filter_by_linenos(self, linenos:int|List[int]):
        """
        Filter the L1Doctests that are contained in this L1ModuleTest by the given line numbers.
        
        Args:
            linenos (int|List[int]): the line numbers to be used to filter the L1Doctests.
        """
        if isinstance(linenos, int):
            linenos = [linenos]
        return self.filter_by_predicate(lambda l1doctest: l1doctest.get_node_lineno() in linenos)

    def get_l1doctests_by_flag(self, flag:L1DocTestFlag) -> List['L1DocTest']:
        """
        Return a list of L1Doctests that have the given flag.
        """
        return self.filter_by_predicate(lambda l1doctest: l1doctest.has_flag(flag))
    
    def does_flag_exist(self, flag:L1DocTestFlag) -> bool:
        """
        Return True if at least one L1Doctest has the given flag. Otherwise, return False.
        """
        return any(l1doctest.has_flag(flag) for l1doctest in self.__l1doctests)
       
    def get_summarize(self) -> Summarize:
        """
        Builds the summarize informations. 
        The summarize contains :
            - Total number of executed tests.
            - How many succeed tests, failed tests, error tests and empty tests.

        Returns:
            Summarize: a namedtuple that represents the summarize object.
        """       
        success = self.count_success()
        failures = self.count_failures()
        errors = self.count_errors()
        empty = self.count_empty()
        total = success + failures + errors
        return Summarize(total, success, failures, errors, empty)
    
    def count_success(self):
        """ Count the number of success l1doctests."""
        return sum([l1doctest.count_passed_tests() for l1doctest in self.__l1doctests])
    
    def count_failures(self):
        """ Count the number of failed l1doctests."""
        return sum([l1doctest.count_failed_tests() for l1doctest in self.__l1doctests])
    
    def count_errors(self):
        """ Count the number of error l1doctests."""
        return sum([l1doctest.count_error_tests() for l1doctest in self.__l1doctests])
    
    def count_empty(self):
        """ Count the number of empty l1doctests."""
        return sum([1 for l1doctest in self.__l1doctests if l1doctest.is_empty()])
    
    def is_failing(self):
        """
        Return True if the module has at least one failing l1doctest. Otherwise, returns False.
        """
        return self.does_flag_exist(L1DocTestFlag.FAILED)
    
    def is_passing(self):
        """
        Return True if the module has only passing l1doctests. Otherwise, returns False.
        """
        return self.count_failures() == 0 and self.count_errors() == 0 and not self.is_empty()
    
    def has_only_failures(self):
        """
        Return True if the module has only failing l1doctests. Otherwise, returns False.
        """
        return self.count_success() == 0 and not self.is_empty()
    
    def is_empty(self):
        """
        Return True if the module has only empty l1doctests. Otherwise, returns False.
        """
        return self.count_empty() == self.count()
    
    def get_summarize_as_string(self):
        """
        Returns a string that contains the summarize informations.
        
        Args:
            summarize (Summarize): a named tuple that contains the summarize infos.
        """
        summarize = self.get_summarize()
        output = "%s: %s\n" % (tr("Tests run"), summarize.total)
        
        for field in summarize._fields[1:]:
            output += tr(field.capitalize()) + ": "
            value = getattr(summarize, field) # returns the value of the field
            output += f"{value}, " if summarize._fields[-1] != field else f"{value}"
        
        return output
    
    def clear(self):
        self.__l1doctests.clear()
    
    def get_l1doctests(self):
        return self.__l1doctests

    def set_l1doctests(self, l1doctests):
        self.__l1doctests = l1doctests
        
    def get_filename(self):
        return self.__filename
    
    def set_filename(self, filename):
        self.__filename = filename
    
    def get_source(self):
        return self.__source
    
    def set_source(self, source):
        self.__source = source
