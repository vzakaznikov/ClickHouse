import time

from testflows.core import *
from testflows.asserts import error
from ssl_server.requirements import *
from ssl_server.tests.common import *


@TestFeature
@Name("dynamic ssl context")
@Requirements(
)
def feature(self, node="clickhouse1"):
    self.context.node = self.context.cluster.node(node)

    for scenario in loads(current_module(), Scenario):
        scenario()
