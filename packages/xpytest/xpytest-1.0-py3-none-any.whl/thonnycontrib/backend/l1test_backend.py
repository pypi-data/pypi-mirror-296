from types import ModuleType
from thonnycontrib.exception_response import ExceptionResponse
from thonnycontrib.utils import tostring, get_env_var, serialize
from thonnycontrib.exceptions import BackendException
from thonnycontrib.environement_vars import *
from thonnycontrib.backend.evaluator import Evaluator 
from thonny.common import ToplevelCommand, ToplevelResponse
from thonnycontrib.properties import BACKEND_COMMAND, SELECTED_LINENO, L1TEST_EXCEPTION, VERDICTS
from thonny.plugins.cpython_backend.cp_back import Executor, MainCPythonBackend
import thonny.plugins.cpython_backend.cp_back

BACKEND: MainCPythonBackend = thonny.plugins.cpython_backend.cp_back.get_backend()

@tostring
class L1TestExecutor(Executor):
    def execute_source(self, source:str, filename:str, mode:str, ast_postprocessors):  
        """Cette fonction est invoquée par la méthode `BACKEND._execute_file(cmd, L1TestExecutor)`
        située en haut de ce fichier.

        Returns:
            dict: doit retourner, obligatoirement, un dictionnaire dont les données sont séralisées.
        """
        assert mode == "exec"
        try:
            evaluator = Evaluator(filename)
            l1ModuleTest = evaluator.evaluate(source)
            
            # Importation du module dans le shell.
            # on récupère la valeur de l'option qui indique si on doit importer le module dans le shell
            if get_env_var(IMPORT_MODULE_VAR): # si la valeur est True alors on importe
                self._import_module_in_shell(evaluator.get_module())                                                

            # The data should be serialized and the returned statement must be a dictionary
            return { VERDICTS: serialize(l1ModuleTest) }
        except BackendException as e:
            return { L1TEST_EXCEPTION: serialize(ExceptionResponse(e)) }     

    def _import_module_in_shell(self, module:ModuleType):
        """
        Imports the given `module` into Thonny's shell.
        
        Args:
            module (ModuleType): the module to be imported into the shell.
        """
        import __main__ 
        __main__.__dict__.update(module.__dict__) 
        
def _cmd_l1test(cmd: ToplevelCommand) -> ToplevelResponse:   
    """
    Cette fonction est invoquée lorsque un événement de type `ToplevelCommand` (associé 
    à la commande L1test) est récupéré.
    
    Args: 
        cmd(ToplevelCommand): L'événement `ToplevelCommand` associé à la commande L1test.
        
    Returns:
        ToplevelResponse: un événement de type ToplveleResponse qui contiendra la réponse
        renvoyé par `L1TestExecutor.execute_source()`.
    """ 
    return BACKEND._execute_file(cmd, L1TestExecutor)
   
def load_plugin(): 
    """
        Cette fonction est importante car il est appelée par Thonny à son intialisation.
        
        Cette fonction doit déclarer les commandes magiques et leurs handlers.
    """
    BACKEND.add_command(BACKEND_COMMAND, _cmd_l1test)
