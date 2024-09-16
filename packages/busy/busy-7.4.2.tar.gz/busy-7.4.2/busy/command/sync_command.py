from importlib import import_module
from busy.command import BusyCommand

from wizlib.parser import WizParser

from busy.error import BusyError


class SyncCommand(BusyCommand):
    """Takes the name of an integration"""

    name = 'sync'

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument('integration')

    @BusyCommand.wrap
    def execute(self):
        module = import_module('busy_' + self.integration)
        func = getattr(module, 'sync')
        result = func(self.app)
        self.status = 'Synced'
        return result
