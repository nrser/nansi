from __future__ import annotations
from collections.abc import Mapping

from nansi.plugins.compose_action import ComposeAction

DEFAULTS = dict(
    name        = 'nginx',
    enabled     = True,
    state       = 'started',
)

class ActionModule(ComposeAction):
    def compose(self):
        self.run_task( 'service', **self.compose_args(defaults=DEFAULTS) )
