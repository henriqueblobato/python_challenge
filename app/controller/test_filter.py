import mock
import unittest
import logit
from netaddr import IPNetwork
from .parser import Parser
from .filter import Filter

class TestFilter(unittest.TestCase):
    def setUp(self):
        pass

    def test_filter_translation(self):
        query = """
        city == "Redmond" || statecode == "WA"
        """

        f = Filter()


