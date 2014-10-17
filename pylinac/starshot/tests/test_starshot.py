from __future__ import division, absolute_import, print_function

import unittest

import numpy as np

from pylinac.starshot.starshot import Starshot


class Star_general_tests(unittest.TestCase):
    """Performs general tests (not demo specific)."""
    def setUp(self):
        self.star = Starshot()
        self.star.load_demo_image()

    def test_mechpoint_is_none_on_load(self):
        """The mechanical isocenter should not have been set upon loading an image."""
        self.assertIsNone(self.star._mechpoint, msg="The mechanical iso did not default to None")

    def test_mechpoint_autosets_if_unset(self):
        """Test that the mechanical isocenter will automatically set if not yet set."""
        # analyze image; mech point is not yet set
        self.star.analyze()
        # the mech point should now have been set
        self.assertIsNotNone(self.star._mechpoint, msg="The mechanical iso did not set automatically when analyzing")


class Star_test_demo1(unittest.TestCase):
    """Specific tests for the first demo image"""
    def setUp(self):
        self.star = Starshot()
        self.star.load_demo_image(number=1)

    def test_image_is_numpy(self):
        """The demo image should be numpy array when loaded."""
        self.assertIsInstance(self.star.image, np.ndarray)

    def test_passed(self):
        """Test that the demo image passed"""
        self.star.analyze()
        self.assertTrue(self.star.wobble_passed, msg="Wobble was not within tolerance")

    def test_wobble_radius(self):
        """Test than the wobble radius is similar to what it has been shown to be (0.495)."""
        self.star.analyze()
        self.assertAlmostEqual(self.star._wobble_radius, 0.49, delta=0.1)

    def test_wobble_center(self):
        """Test that the center of the wobble circle is close to what it's shown to be (1511.5, 1302.2)."""
        self.star.analyze()
        # test y-coordinate
        y_coord = self.star._wobble_center[0]
        self.assertAlmostEqual(y_coord, 1510, delta=10)
        # test x-coordinate
        x_coord = self.star._wobble_center[1]
        self.assertAlmostEqual(x_coord, 1300, delta=10)

    def test_num_peaks(self):
        """Test than the number of peaks (strips) found is what is expected."""
        expected_peaks = 18
        self.star.analyze()
        self.assertEqual(len(self.star._peak_locs), expected_peaks,
                         msg="The number of peaks found was not the number expected")


class Star_test_demo2(unittest.TestCase):
    """Tests specifically for demo image #2."""
    def setUp(self):
        self.star = Starshot()
        self.star.load_demo_image(number=2)

    def test_image_is_numpy(self):
        """The demo image should be numpy array when loaded."""
        self.assertIsInstance(self.star.image, type(np.array([])))

    def test_passed(self):
        """Test that the demo image passed"""
        self.star.analyze()
        self.assertTrue(self.star.wobble_passed, msg="Wobble was not within tolerance")

    def test_wobble_radius(self):
        """Test than the wobble radius is similar to what it has been shown to be (0.495)."""
        self.star.analyze()
        self.assertAlmostEqual(self.star._wobble_radius, 0.17, delta=0.1)

    def test_wobble_center(self):
        """Test that the center of the wobble circle is close to what it's shown to be (1511.5, 1302.2)."""
        self.star.analyze()
        # test y-coordinate
        y_coord = self.star._wobble_center[0]
        self.assertAlmostEqual(y_coord, 1698, delta=10)
        # test x-coordinate
        x_coord = self.star._wobble_center[1]
        self.assertAlmostEqual(x_coord, 1296, delta=10)

    def test_num_peaks(self):
        """Test than the number of peaks (strips) found is what is expected."""
        expected_peaks = 18
        self.star.analyze()
        self.assertEqual(len(self.star._peak_locs), expected_peaks,
                         msg="The number of peaks found was not the number expected")

    def test_still_pass_with_mech_point_off(self):
        """Test that the algo will still pass if the mech point is set
            to a point somewhat different than actual center.
            """
        self.star.set_mech_point([1600, 1200], warn_if_far_away=False)
        self.star.analyze()

        self.assertTrue(self.star.wobble_passed)

        y_coord = self.star._wobble_center[0]
        x_coord = self.star._wobble_center[1]
        self.assertAlmostEqual(y_coord, 1698, delta=10)
        self.assertAlmostEqual(x_coord, 1296, delta=10)
