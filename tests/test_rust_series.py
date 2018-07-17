# -*- coding: utf-8 -*-

import unittest
import logging
import timeit
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class RustSeriesTestCase(unittest.TestCase):

    def test_cumsum(self):
        """
        Test cumulative sum of series
        """
        from lumberjack.cython.series import LumberJackSeries

        series = LumberJackSeries.arange(0, 4)
        _pd_series = pd.Series(np.arange(0, 4))
        cumsum = series.cumsum()
        logger.debug('Got cumsum of {}'.format(cumsum))

        # Ensure they sum to the same
        lj_cumsum_sum = series.cumsum().sum()
        pd_cumsum_sum = _pd_series.cumsum().sum()
        logger.debug(
            'Cumulative sum over arange(0, 4) -> LumberJack: {} -- Pandas: {}'.format(lj_cumsum_sum, pd_cumsum_sum)
        )
        self.assertEqual(lj_cumsum_sum, pd_cumsum_sum,
                         msg='LumberJack and Pandas .cumsum().sum() does not match! -- LumberJack: {}, Pandas: {}'
                             .format(lj_cumsum_sum, pd_cumsum_sum)
                         )

        # Speed test
        lj_time = timeit.timeit(
            stmt='series.cumsum()',
            number=10000,
            setup='from lumberjack.cython.series import LumberJackSeries; series = LumberJackSeries.arange(0, 10000)'
        )
        pd_time = timeit.timeit(
            stmt='series.cumsum()',
            number=10000,
            setup='import numpy as np; import pandas as pd; series = pd.Series(np.arange(0, 10000))'
        )
        logger.debug(
            '.cumsum() speed: Avg LumberJack: {:.4f}s -- Pandas: {:.4f}'.format(lj_time, pd_time))
        self.assertLessEqual(lj_time, pd_time)


    def test_sum(self):
        """
        Test the ability to sum a series
        """
        from lumberjack.cython.series import LumberJackSeries
        series = LumberJackSeries.arange(0, 4)
        total = series.sum()
        logger.debug('Sum of arange(0, 4) is: {}'.format(total))
        self.assertEqual(total, 6)

        # Test speed
        lj_time = timeit.timeit(
            stmt='series.sum()',
            number=10000,
            setup='from lumberjack.cython.series import LumberJackSeries; series = LumberJackSeries.arange(0, 10000)'
        )
        np_time = timeit.timeit(
            stmt='array.sum()',
            number=10000,
            setup='import numpy as np; array = np.arange(0, 10000)'
        )
        pd_time = timeit.timeit(
            stmt='series.sum()',
            number=10000,
            setup='import numpy as np; import pandas as pd; series = pd.Series(np.arange(0, 10000))'
        )
        logger.debug('.sum() speed: Avg LumberJack: {:.4f}s -- Numpy: {:.4f}s -- Pandas: {:.4f}'.format(lj_time, np_time, pd_time))
        self.assertLessEqual(lj_time, np_time, msg='Expected LumberJack .sum() to be faster but it was not!')

    def test_arange(self):
        """
        Check creating an array from inside Rust and passing it to Python
        """
        from lumberjack.cython.series import LumberJackSeries
        series = LumberJackSeries.arange(0, 4)
        vec = series.to_numpy()
        logger.debug('Vector type: {}, and it looks like: {}, sum is: {}'.format(type(vec), vec, vec.sum()))
        self.assertEqual(vec.sum(), 6)

        # If we re-implement numpy function, they should be faster
        lj_time = timeit.timeit('LumberJackSeries.arange(0, 10000)',
                                number=10000,
                                setup='from lumberjack.cython.series import LumberJackSeries')
        np_time = timeit.timeit('np.arange(0, 10000)',
                                number=10000,
                                setup='import numpy as np')
        logger.debug('.arange(0, 10000) speed: Avg LumberJack: {:4f}s -- Avg numpy: {:.4f}s'.format(lj_time, np_time))
        self.assertLess(lj_time, np_time,
                        'Expected LumberJack ({:.4f}) to be faster than numpy ({:.4f}), but it was not!'
                        .format(lj_time, np_time))
    '''
    def test_from_numpy(self):
        """
        Test creating a series from numpy array
        """
        from lumberjack.cython.series import LumberJackSeries

        array = np.ones(shape=(10,), dtype=float)
        series = LumberJackSeries.from_numpy(array)
        logger.debug('Made series from numpy: {}'.format(series))
    '''


