##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.20                                                            #
# Generated on 2024-09-16T18:11:29.553157                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.metaflow_current
    import metaflow.decorators

current: metaflow.metaflow_current.Current

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

class TriggerDecorator(metaflow.decorators.FlowDecorator, metaclass=type):
    def flow_init(self, flow_name, graph, environment, flow_datastore, metadata, logger, echo, options):
        ...
    ...

class TriggerOnFinishDecorator(metaflow.decorators.FlowDecorator, metaclass=type):
    def flow_init(self, flow_name, graph, environment, flow_datastore, metadata, logger, echo, options):
        ...
    def get_top_level_options(self):
        ...
    ...

