
import sys
mypath = "C:\EC-Lab Development Package\Examples\Python"
sys.path.insert(0, mypath)

from kbio.utils import exception_brief

#==============================================================================#
# Helper functions
#==============================================================================#
class Helpers:
    def __init__(self):
        pass
    @staticmethod
    def _newline():
        print()

    def _print_exception(self, e):
        print(f"{exception_brief(e, self.verbosity)}")
