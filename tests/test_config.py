# Unit testing template for Blender add-ons
# Copyright (C) 2025 Spencer Magnusson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import logging
import os
import sys
from pathlib import Path
import unittest
import tomllib


# Add addon root to sys.path so relative imports inside __init__.py work
addon_root = Path(
    __file__
).parent.parent.resolve()  # points to blender_extension_template or addon_testing
sys.path.insert(0, str(addon_root))

from __init__ import bl_info  # relative imports inside __init__.py are now valid


class TestConfig(unittest.TestCase):
    def bl_info_dict(self):
        """Return bl_info dictionary from __init__.py"""
        logging.debug(bl_info)
        return bl_info

    def get_manifest_info(self):
        """Load blender_manifest.toml"""
        toml_file = addon_root / "blender_manifest.toml"
        with open(toml_file, "rb") as f:
            config = tomllib.load(f)

        logging.debug(config)
        return config

    def test_assert_version(self):
        """bl_info and blender_manifest versions match"""
        bl = self.bl_info_dict()
        manifest = self.get_manifest_info()

        bl_version_str = f"{bl['version'][0]}.{bl['version'][1]}.{bl['version'][2]}"
        self.assertEqual(bl_version_str, manifest["version"])

    def test_assert_name(self):
        """bl_info and blender_manifest names match"""
        bl = self.bl_info_dict()
        manifest = self.get_manifest_info()
        self.assertEqual(bl["name"], manifest["name"])

    def test_assert_description(self):
        """bl_info and blender_manifest descriptions match"""
        bl = self.bl_info_dict()
        manifest = self.get_manifest_info()
        self.assertEqual(bl["description"], manifest["tagline"])

    def test_assert_author(self):
        """bl_info and blender_manifest authors match"""
        bl = self.bl_info_dict()
        manifest = self.get_manifest_info()
        self.assertEqual(bl["author"], manifest["maintainer"])


if __name__ == "__main__":
    # discover and run tests in this folder
    loader = unittest.TestLoader()
    suite = loader.discover(str(Path(__file__).parent))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
