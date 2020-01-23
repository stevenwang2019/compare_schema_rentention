import unittest
from process_yaml import *

class TestConversion(unittest.TestCase):
    def test_convert_retention_to_int(self):
        self.assertEqual(convert_retention_to_int('9'), 9)
        self.assertEqual(convert_retention_to_int('0s'), 0)
        self.assertEqual(convert_retention_to_int('2s'), 2)
        self.assertEqual(convert_retention_to_int('3m'), 180)
        self.assertEqual(convert_retention_to_int('4h'), 14400)
        self.assertEqual(convert_retention_to_int('5d'), 432000)
        self.assertEqual(convert_retention_to_int('2y'), 63072000)
        self.assertRaises(Exception, convert_retention_to_int, '')
        self.assertRaises(Exception, convert_retention_to_int, 'randoms string')
        self.assertRaises(Exception, convert_retention_to_int, '000badformat')
        self.assertRaises(Exception, convert_retention_to_int, '12x')

    def test_build_subdir_from_pattern(self):
        self.assertEqual(build_subdir_from_pattern('^data\.collectd\.'),'^'+wsp_root+'/data/collectd/')
        self.assertEqual(build_subdir_from_pattern('^stats_counts\.hawking_core\..*'),'^'+wsp_root+'/stats_counts/hawking_core/.*')
        self.assertEqual(build_subdir_from_pattern('^totango_cron\..*'),'^'+wsp_root+'/totango_cron/.*')
        self.assertEqual(build_subdir_from_pattern('^(stats|stats_counts)\..*'),'^'+wsp_root+'/(stats|stats_counts)/.*')
        self.assertEqual(build_subdir_from_pattern('.*'), wsp_root+'/.*')

    def test_compare_whisper_info(self):
        #self.assertEqual(compare_whisper_info('data_team_collectd','^data\.collectd\.',['259200 10','2592000 60']), 'data')
        #compare_whisper_info('data_team_collectd','^data\.collectd\.',['259200 10','2592000 60'])
        return

if __name__ == '__main__':
    unittest.main()