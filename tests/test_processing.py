# -*- coding: utf-8 -*-
#
# test_processing.py
#
# purpose:  Test processing step from ctd.py
# author:   Filipe P. A. Fernandes
# e-mail:   ocefpaf@gmail
# web:      http://ocefpaf.tiddlyspot.com/
# created:  01-Mar-2013
# modified: Wed 24 Jul 2013 08:17:36 PM BRT
#
# obs:
#


import unittest
import numpy as np
from ctd import DataFrame, lp_filter, derive_cnv


class BasicProcessingTests(unittest.TestCase):
    def setUp(self):
        self.raw = DataFrame.from_cnv('data/CTD-spiked-unfiltered.cnv.bz2',
                                      compression='bz2')
        self.prc = DataFrame.from_cnv(fname='data/CTD-spiked-filtered.cnv.bz2',
                                      compression='bz2')

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    # Split.
    def test_split_return_tuple(self):
        self.assertIsInstance(self.raw.split(), tuple)

    def test_split_cnv(self):
        downcast, upcast = self.raw.split()
        self.assertTrue(downcast.index.size + upcast.index.size ==
                        self.raw.index.size)

    # Despike.
    def test_despike(self):
        dirty = self.prc['c0S/m'].split()[0]  # Looking at downcast only.
        clean = dirty.despike(n1=2, n2=20, block=500)
        spikes = clean.isnull()
        equal = (dirty[~spikes] == clean[~spikes]).all()
        self.assertTrue(spikes.any() and equal)

    # Filter.
    def test_lp_filter_2(self):
        kw = dict(sample_rate=24.0, time_constant=0.15)
        unfiltered = self.raw.index.values
        filtered = lp_filter(unfiltered, **kw)
        # FIXME: Not a good test...
        np.testing.assert_almost_equal(filtered, self.prc.index.values,
                                       decimal=1)

    # Pressure check.
    def test_press_check(self):
        unchecked = self.raw['t090C']
        press_checked = unchecked.press_check()
        reversals = press_checked.isnull()
        equal = (unchecked[~reversals] == press_checked[~reversals]).all()
        self.assertTrue(reversals.any() and equal)

    def test_bindata(self):
        delta = 1.
        down = self.prc['t090C'].split()[0]
        down = down.bindata(delta=delta)
        self.assertTrue(np.unique(np.diff(down.index.values)) == delta)

    # PostProcessingTests.
    def test_smooth(self):
        pass  # TODO

    def test_mixed_layer_depth(self):
        pass  # TODO

    def test_barrier_layer_thickness(self):
        pass  # TODO

    def derive_cnv(self):
        derived = derive_cnv(self.raw)
        new_cols = set(derived).symmetric_difference(self.raw.columns)
        self.assertTrue(['CT', 'SA', 'SP', 'SR', 'sigma0_CT', 'z'] ==
                        sorted(new_cols))


def main():
    unittest.main()


if __name__ == '__main__':
    main()