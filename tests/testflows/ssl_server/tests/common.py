import uuid

from testflows.core import *
from testflows.core.name import basename, parentname
from testflows._core.testtype import TestSubType

def getuid():
    if current().subtype == TestSubType.Example:
        testname = f"{basename(parentname(current().name)).replace(' ', '_').replace(',','')}"
    else:
        testname = f"{basename(current().name).replace(' ', '_').replace(',','')}"
    return testname + "_" + str(uuid.uuid1()).replace('-', '_')
