import unittest

from clientwrapper import ResultMapping


class MappingTestCase(unittest.TestCase):
    def test_filtering(self):
        apples_data = [
            {
                'color': 'red',
                'taste': 'sweet'
            },
            {
                'color': 'green',
                'taste': 'sour'
            },
            {
                'color': 'purple',
                'taste': 'rotten'
            }
        ]
        colorless_apples = [ResultMapping(apple, filter_keys=["taste"]) for apple in apples_data]
        self.assertTrue(all(apple.data.get('taste', '') != '' for apple in colorless_apples))
        self.assertTrue(all(apple.data.get('color', '') == '' for apple in colorless_apples))
        tasteless_apples = [ResultMapping(apple, filter_keys=["color"]) for apple in apples_data]
        self.assertTrue(all(apple.data.get('color', '') != '' for apple in tasteless_apples))
        self.assertTrue(all(apple.data.get('taste', '') == '' for apple in tasteless_apples))
