# Ceci est une implémentation de création d'un singleton pour L1TestRunner
from enum import Enum
from thonnycontrib.frontend.gui.l1test_gui_runner import ThonnyGuiRunner
from thonnycontrib.frontend.cli.l1test_cli_runner import L1TestCliRunner

_l1test_runner = None


class L1TestRunnerMode(Enum):

    THONNY_GUI = ThonnyGuiRunner
    L1TEST_CLI = L1TestCliRunner
    
    def get_instance(self):
        return self.value()
    
def get_l1test_runner(mode:L1TestRunnerMode):
    """
    If there's no `L1TestRunner` instance creates one and returns it, 
    otherwise returns the current `L1TestRunner` instance.
    """
    assert isinstance(mode, L1TestRunnerMode)
    return mode.get_instance() if not _l1test_runner else _l1test_runner

def get_l1test_gui_runner():
    return get_l1test_runner(L1TestRunnerMode.THONNY_GUI)

def get_l1test_cli_runner():
    return get_l1test_runner(L1TestRunnerMode.L1TEST_CLI)