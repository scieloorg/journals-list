# coding: utf-8

import unittest
from articlemeta.client import ThriftClient

client = ThriftClient()

class ClientTest(unittest.TestCase):

    def test_journal_collection_acronym(self):

        result = [journal.collection_acronym  for journal in client.journals('spa')][0]

        expected = 'spa'
        
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()