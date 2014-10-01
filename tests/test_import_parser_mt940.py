import datetime
import os
import tempfile
from decimal import Decimal

from nose.tools import eq_, ok_

from bdgt.importer.parsers.mt940 import Mt940Parser
