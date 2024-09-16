from abc import *
from logging import Logger, getLogger
import time
from typing import Dict, List
import ast, json, configparser
from thonnycontrib.exception_response import ExceptionResponse
from thonnycontrib.frontend import get_l1test_gui_runner
from thonnycontrib.l1test_options.l1test_options import TEMPLATE_DOCSTRING, set_option

from thonnycontrib.utils import add_newline, get_template_path, get_ini_config_path

SUMMARY_KEY = "summary"
PARAM_KEY = "parameters"
CU_KEY = "usage_constraints"
DOCTEST_KEY = "test_examples"
RETURN_KEY = "return_description" 
RETURN_TYPE_KEY = "return_type" 
TODO_KEY = "todo_label" 

DEFAULT_TEMPLATE_VOCABULARY = {
    "function": {
      SUMMARY_KEY: "à_remplacer_par_ce_que_fait_la_fonction\n\n",
      PARAM_KEY: "Paramètres :\n",
      CU_KEY: "Précondition : \n\n",
      DOCTEST_KEY: "Exemple(s) :\n$$$ \n\n",
      RETURN_KEY: "Valeur de retour ",
      RETURN_TYPE_KEY: "(%s) :\n",
      TODO_KEY: ""
    },
    "class": {
      SUMMARY_KEY: "This is a summary for class",
      PARAM_KEY: "",
      CU_KEY: "Class usage constraints: ",
      DOCTEST_KEY: "Example: ",
      TODO_KEY: ""
    }
}

def get_external_doc_config(field:str, convert_to=None):
    config = configparser.ConfigParser()
    config.read(get_ini_config_path())
    if convert_to == bool:
        return config['external-doc'].getboolean(field)
    elif convert_to == int:
        return config['external-doc'].getint(field)
    elif convert_to == float:
        return config['external-doc'].getfloat(field)
    else:
        return config['external-doc'][field]

ENABLE_EXTERNAL_DOC = get_external_doc_config('enable', bool)
set_option(TEMPLATE_DOCSTRING, not ENABLE_EXTERNAL_DOC)

CUSTOM_TEMPLATE_PATH = get_template_path(get_external_doc_config('basename'))

def display_error(error_msg:str, title:str, force:bool=True):
    exception_response = ExceptionResponse(Exception(error_msg))
    exception_response.set_title(title)
    get_l1test_gui_runner().display_error_on_view(exception_response, force)

def _build_vocabulary(enable_external_doc:bool=ENABLE_EXTERNAL_DOC, custom_template_path:str=CUSTOM_TEMPLATE_PATH):
    if not enable_external_doc:
        return DEFAULT_TEMPLATE_VOCABULARY
    
    external_doc, data = {}, {}
    try:
        with open(custom_template_path, 'r') as file:
            data:Dict[str, dict] = json.load(file)
    except FileNotFoundError:
        set_option(TEMPLATE_DOCSTRING, True) # set the default docstring
        getLogger(__name__).error("File not found: %s" % custom_template_path, exc_info=True)
        getLogger(__name__).warning("The given external template file (%s) not found. The default vocabulary will be used." % custom_template_path)
        display_error("The given external template file (%s) not found. The default vocabulary will be used." % custom_template_path,
                      title="Cannot read the custom docstring template:")
    
    for type, vocab in DEFAULT_TEMPLATE_VOCABULARY.items():
        external_doc[type] = {}
        if type in data.keys():
            for section, description in vocab.items():
                if section in data[type].keys(): 
                    external_doc[type][section] = data[type][section]
                else: 
                    external_doc[type][section] = ""
        else:
            external_doc[type] = vocab
                        
    return DEFAULT_TEMPLATE_VOCABULARY if not external_doc else external_doc

class DocTemplate(ABC):
    # Ces constantes peuvent être utilisées dans les classes d'implémention
    NEW_LINE = "\n"
    DOCSTRING_SYMBOL = '"""'
    LOGGER = getLogger(__name__)
    
    def __init__(self) -> None:
        self.__enable_external_doc = ENABLE_EXTERNAL_DOC
        self.__external_template_path = CUSTOM_TEMPLATE_PATH
        self.__vocabulary = _build_vocabulary()
    
    def _format_params(self, params) -> str:
        """
        Args:
            params (List): It's a list of the arguments.

        Returns:
            str: Returns the parameter representation section of a node in a docstring. 
        """
        if params is None:
            return ""
        args_to_exclude = ["self", "cls"]
        label = add_newline(self.vocabulary_field(PARAM_KEY))
        format_params = ""
        for p in params:
            arg_type = ast.unparse(p.annotation) if p.annotation else ""     
            arg_name = p.arg 
            if arg_name not in args_to_exclude: 
                format_params += "- %s (%s) : %s" %(arg_name, arg_type, add_newline(self.vocabulary_field(TODO_KEY)))
        return label + format_params
    
    @abstractmethod
    def get_parameters(self, node:ast.AST) -> List:
        """
        Get the paramters of a given node.
        
        Args:
            node (ast.AST): An AST node. 

        Returns:
            List: Returns a List of arguments of the given node.
        """
        pass
    
    @abstractmethod
    def _format_general_summary(self) -> str:
        """
        Returns:
            str: Returns a label which will indicate to write a summary of the function.
        """
        pass
    
    @abstractmethod
    def _format_usage_constraints(self) -> str:
        """
        Returns:
            str: Returns the usage constraints representation section in a docstring.
        """
        pass
    
    @abstractmethod
    def _format_return_value(self) -> str:
        """
        Returns:
            str: Returns the return value representation section in a docstring.
        """
        pass
    
    @abstractmethod
    def _format_test_examples(self) -> str:
        """
        Returns:
            str: Returns the test examples representation section in a docstring.
        """
        pass
    
    @abstractmethod
    def get_template(self, node:ast.AST=None) -> str:
        """Build the complete docstring template. 
        This method must invoke the above abstract methods.
        
        Args:
            node (ast.AST): The AST node in which the dosctring will be generated.

        Returns:
            str: Returns the template representation. 
        """
        pass  
    
    @abstractmethod
    def get_template_id(self) -> str: 
        pass      
    
    def vocabulary_field(self, name:str):
        """Get the value of a field from the vocabulary dict"""
        return self.get_vocabulary()[name]
    
    def get_enable_external_doc(self):
        return self.__enable_external_doc

    def get_basename(self):
        return self.__external_template_path

    def get_vocabulary(self):
        return self.__vocabulary

class DocFunctionTemplate(DocTemplate):
    '''
    Modifié pour coller au cours de PROG, portail MI, avec volonté
    d'alléger les docstring au max : uniquement la première phrase, la
    precond et les tests (les étudiant·es étant obligés d'indiquer des
    annotations de type).
    '''
    def __init__(self) -> None:
        super().__init__()
    
    def get_parameters(self, node:ast.AST):
        """
        Get the paramters of a given node.
        
        Args:
            node (ast.AST): An AST node. Must be an ast.FunctionDef or ast.AsyncFunctionDef

        Returns:
            List: Returns a List of arguments of the given node.
        """
        if isinstance(node, ast.FunctionDef):
            return node.args.args
        return []

    def _format_general_summary(self):
        return add_newline(self.vocabulary_field(SUMMARY_KEY))
    
    def _format_usage_constraints(self):
        return self.vocabulary_field(CU_KEY) + add_newline(self.vocabulary_field(TODO_KEY))

    def _format_return_value(self, node: ast):
        return_type = ast.unparse(node.returns) if node.returns else ""
        return_type_value:str = self.vocabulary_field(RETURN_TYPE_KEY)
        # check if the return type contains '%s' to replace it with the return type
        if return_type_value.find('%s') == -1:
            return_descr = return_type_value
        else:
            return_descr = return_type_value % return_type
        return self.vocabulary_field(RETURN_KEY) + add_newline(return_descr)
    
    def _format_test_examples(self):
        label = add_newline(self.vocabulary_field(DOCTEST_KEY))
        todo = add_newline(self.vocabulary_field(TODO_KEY))
        return label + todo
        
    def get_template(self, node: ast.AST):
        '''Les commentaires indiquent les allègements pour le passage SESI -> MI.'''
        return (
            self.DOCSTRING_SYMBOL + 
            self._format_general_summary() + 
            self._format_params(self.get_parameters(node))  + 
            self._format_usage_constraints() +
            self._format_test_examples() + 
            self._format_return_value(node) + 
            self.DOCSTRING_SYMBOL + self.NEW_LINE
        )
    
    def get_template_id(self): 
        return "def" 
    
    def get_vocabulary(self):
        return super().get_vocabulary()["function"]

class DocClassTemplate(DocTemplate): 
    def __init__(self) -> None:
        super().__init__()
        
    def _format_general_summary(self):
        return add_newline(self.vocabulary_field(SUMMARY_KEY))
    
    def get_parameters(self, node):
        # Parcourir les définitions de méthodes dans la classe
        for sub_node in node.body:
            if isinstance(sub_node, ast.FunctionDef) and sub_node.name == "__init__":
                # Trouver les paramètres de la méthode __init__
                return sub_node.args.args
        return []
     
    def _format_usage_constraints(self):
        return (self.vocabulary_field(CU_KEY) +
                add_newline(self.vocabulary_field(TODO_KEY))
            )  

    def _format_return_value(self):
        return ""
    
    def _format_test_examples(self):
        label = add_newline(self.vocabulary_field(DOCTEST_KEY))
        todo = add_newline(self.vocabulary_field(TODO_KEY))
        return label + todo
            
    def get_template(self, node):
        return self.DOCSTRING_SYMBOL + \
               self._format_general_summary() + \
               self._format_usage_constraints() + \
               self._format_test_examples() + \
               self.DOCSTRING_SYMBOL + self.NEW_LINE

    def get_template_id(self): 
        return "class" 
    
    def get_vocabulary(self):
        return super().get_vocabulary()["class"]

class DocTemplateFactory:            
    @staticmethod
    def create_template(type:str):
        return DocTemplateFactory.__search_type(type)
    
    @staticmethod
    def __docTemplate_subclasses(cls=DocTemplate):
        return set(cls.__subclasses__()) \
               .union([s for c in cls.__subclasses__() \
                            for s in DocTemplateFactory.__docTemplate_subclasses(c)])
    
    @staticmethod
    def __search_type(type:str) -> DocTemplate|None:
        template_types = DocTemplateFactory.__docTemplate_subclasses()
        
        find_type = [t() for t in template_types if type==t().get_template_id()]
        return find_type[0] if find_type else None   
