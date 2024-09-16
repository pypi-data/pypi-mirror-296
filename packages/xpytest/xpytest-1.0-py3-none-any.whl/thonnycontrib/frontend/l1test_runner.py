from abc import ABC, abstractmethod
from logging import getLogger
import traceback
from typing import List
from thonnycontrib.backend import get_event_manager
from thonnycontrib.environement_vars import FILTER_PREDICATE_VAR, IS_GUI_MODE_VAR, LINENO
from thonnycontrib.backend.l1test_backend import ExceptionResponse
from thonnycontrib.properties import BACKEND_COMMAND
from thonnycontrib.utils import tostring
from thonnycontrib import frontend 
from thonny.common import ToplevelResponse, BackendEvent
from thonnycontrib.exceptions import *

@tostring
class AbstractL1TestRunner(ABC):
    """The `L1TestRunner` is responsible for starting the execution of the plugin. It's like 
    a controller that handles sending requests and receiving responses.
    
    The `L1TestRunner` handles also the state of the current execution of the plugin. It has 
    three states : 
    - _is_l1test_running : set to true when the  l1test is just invoked.
    - _is_pending : set to true when the plugin is still runinng but not yet finished. 
                    This state is sent from the backend to tell the `L1TestRunner` that the `Evaluator`
                    didn't finished the evaluations yet. This is useful when the Evaluator encouter
                    an infinite loop, in this case the L1TestRunner knows that the Evaluator is still 
                    working (or blocked). 
    - _has_exception: when the backend sends an exception instead of the verdicts.

    You should implement the _handle_execution_state() method to make your logic when receiving an exécution state from the backend. For example, you can just show the current exécuted test.
    """
    def __init__(self):
        frontend._l1test_runner = self
        self._has_exception = False
        self._is_l1test_running = False
        self._is_pending = False
        get_event_manager().add_listener(self)
               
    def run(self, **kw):
        """
        Run the L1Test. Each implementation should specify how the L1test
        should be executed.
        """
        from thonnycontrib.frontend import L1TestRunnerMode
        try:
            if not self.is_running(): # si l1test n'est est pas déjà en cours d'execution
                self.set_is_running()
                kw[IS_GUI_MODE_VAR] = self.is_gui_mode()
                print
                self._run(**kw)
        except BaseException as e:
            getLogger(__name__).error("%s", traceback.format_exc(), exc_info=True)
            self.terminate_running()
            self.set_has_exception(True)
            if not isinstance(e, FrontendException):
                # on veut pas afficher une erreur quelconque sur la errorview car on aura moins 
                # de contexte. Si cette ligne s'exécute c'est probablement dû à un bug dans le code.
                raise e 
            self.show_error(e)  

    def run_test_at(self, linenos:int|List[int]):
        """
        Run the test at the given lineno.
        
        Args:
            lineno (int): the lineno of the test to run.
        """
        if isinstance(linenos, int):
            linenos = [linenos]
        predicate = lambda l1doctest: l1doctest.get_node_lineno() in linenos
        self.run(**{FILTER_PREDICATE_VAR: predicate, LINENO: linenos})

    def run_failed_tests(self):
        """
        Run the failed tests. 
        This method based on the predicate that filters the failed tests.
        """
        predicate = lambda l1doctest: l1doctest.is_failing()
        self.run(**{FILTER_PREDICATE_VAR: predicate})
    
    @abstractmethod
    def _run(self, **kw):
        pass
    
    @abstractmethod
    def handle_execution_state(self, event: BackendEvent):
        """
        This Method is invoked by the backend when the tests are evaluated. It is invoked for each Example and when the Evaluator finishes the evaluation. 

        - When Examples are evaluated the state sent by the backend is PENDING_STATE. 
        - When the Evaluator finishes it's job the state is FINISHED_STATE. 

        The event contains other useful informations like the lineno of the current executed Example.
        """
        pass
    
    def show_error(self, exception_response: ExceptionResponse|BaseException, error_title:str=None):
        """
        Clears the error view and reports the error message on it. Hides the treeview.
        
        Note: use this method instead of _show_error().
        
        Args:
            exception_response (ExceptionResponse|Exception): The exception to display.
            It can be either a ExceptionResponse or an Exception. If it is an Exception
            so it will be converted to a ExceptionResponse.
        """
        assert isinstance(exception_response, (ExceptionResponse, BaseException)), "exception_response must be an ExceptionResponse or an Exception but was %s" % type(exception_response)
        if not isinstance(exception_response, ExceptionResponse):
            exception_response = ExceptionResponse(exception_response)
        exception_response.set_title(error_title)
             
        self._show_error(exception_response)
    
    @abstractmethod
    def _show_error(self, exception_response: ExceptionResponse|BaseException) -> None:
        """
        Shows the error message in the frontend. You should not use this method directly, 
        
        Note: use the show_error() instead.
        """
        pass
    
    def _is_relevant_response(self, msg: ToplevelResponse, cmd_name:str=BACKEND_COMMAND):
       """Returns True if the TopLevelResponse is relevant to the l1test plugin."""         
       return msg.get("command_name") == cmd_name
    
    def set_is_running(self, value=True):
        self._is_l1test_running = value
        if not self.is_running():
            self.set_is_pending(False)

    def is_gui_mode(self):
        """
        Returns True if the current mode is GUI mode, otherwise False.
        """
        return frontend.L1TestRunnerMode.THONNY_GUI.value == self.__class__
        
    def is_running(self):
        return self._is_l1test_running
    
    def is_pending(self):
        return self._is_pending
    
    def set_is_pending(self, is_pending:bool):
        self._is_pending = is_pending
    
    def set_has_exception(self, has_exception:bool):
        self._has_exception = has_exception
    
    def has_exception(self):
        return self._has_exception
    
    def terminate_running(self):
        """
        Set the state of `L1TestRunner` as terminated.
        This function sets the `_is_l1test_running` attribute to False
        """
        self.set_is_pending(False)
        self.set_is_running(False)