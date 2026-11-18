"""Isolate the test suite from real autoshift state.

Import this module FIRST in every test module, before any application module.
Importing ``shift``, ``query`` or ``migrations`` opens and migrates ``keys.db``
under ``common.DATA_DIR``; without this, tests would touch the developer's
``data/`` directory. Every module resolves paths through ``common.data_path``
(or copies ``common.DATA_DIR`` at import), so redirecting it here is enough.
"""
import atexit
import shutil
import tempfile

import common

if not getattr(common, "TEST_DATA_DIR", None):
    common.TEST_DATA_DIR = tempfile.mkdtemp(prefix="autoshift-tests-")
    common.DATA_DIR = common.TEST_DATA_DIR
    atexit.register(shutil.rmtree, common.TEST_DATA_DIR, True)
