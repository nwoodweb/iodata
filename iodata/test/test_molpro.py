# -*- coding: utf-8 -*-
# IODATA is an input and output module for quantum chemistry.
#
# Copyright (C) 2011-2019 The IODATA Development Team
#
# This file is part of IODATA.
#
# IODATA is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# IODATA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --
# pragma pylint: disable=invalid-name, no-member
"""Test iodata.molpro module."""

import os

import numpy as np
from numpy.testing import assert_equal, assert_allclose

from ..iodata import IOData

try:
    from importlib_resources import path
except ImportError:
    from importlib.resources import path


def test_load_fcidump_psi4_h2():
    with path('iodata.test.data', 'FCIDUMP.psi4.h2') as fn:
        mol = IOData.from_file(str(fn))
    assert_allclose(mol.core_energy, 0.7151043364864863E+00)
    assert_equal(mol.nelec, 2)
    assert_equal(mol.ms2, 0)
    assert_equal(mol.one_mo.shape, (10, 10))
    assert_allclose(mol.one_mo[0, 0], -0.1251399119550580E+01)
    assert_allclose(mol.one_mo[2, 1], 0.9292454365115077E-01)
    assert_allclose(mol.one_mo[1, 2], 0.9292454365115077E-01)
    assert_allclose(mol.one_mo[9, 9], 0.9035054979531029E+00)
    assert_allclose(mol.two_mo.shape, (10, 10, 10, 10))
    assert_allclose(mol.two_mo[0, 0, 0, 0], 0.6589928924251115E+00)
    # Check physicist's notation and symmetry
    assert_allclose(mol.two_mo[6, 1, 5, 0], 0.5335846565304321E-01)
    assert_allclose(mol.two_mo[5, 1, 6, 0], 0.5335846565304321E-01)
    assert_allclose(mol.two_mo[6, 0, 5, 1], 0.5335846565304321E-01)
    assert_allclose(mol.two_mo[5, 0, 6, 1], 0.5335846565304321E-01)
    assert_allclose(mol.two_mo[1, 6, 0, 5], 0.5335846565304321E-01)
    assert_allclose(mol.two_mo[1, 5, 0, 6], 0.5335846565304321E-01)
    assert_allclose(mol.two_mo[0, 6, 1, 5], 0.5335846565304321E-01)
    assert_allclose(mol.two_mo[0, 5, 1, 6], 0.5335846565304321E-01)
    assert_allclose(mol.two_mo[9, 9, 9, 9], 0.6273759381091796E+00)


def test_load_fcidump_molpro_h2():
    with path('iodata.test.data', 'FCIDUMP.molpro.h2') as fn:
        mol = IOData.from_file(str(fn))
    assert_allclose(mol.core_energy, 0.7151043364864863E+00)
    assert_equal(mol.nelec, 2)
    assert_equal(mol.ms2, 0)
    assert_equal(mol.one_mo.shape, (4, 4))
    assert_allclose(mol.one_mo[0, 0], -0.1245406261597530E+01)
    assert_allclose(mol.one_mo[0, 1], -0.1666402467335385E+00)
    assert_allclose(mol.one_mo[1, 0], -0.1666402467335385E+00)
    assert_allclose(mol.one_mo[3, 3], 0.3216193420753873E+00)
    assert_allclose(mol.two_mo.shape, (4, 4, 4, 4))
    assert_allclose(mol.two_mo[0, 0, 0, 0], 0.6527679278914691E+00)
    # Check physicist's notation and symmetry
    assert_allclose(mol.two_mo[3, 0, 2, 1], 0.7756042287284058E-01)
    assert_allclose(mol.two_mo[2, 0, 3, 1], 0.7756042287284058E-01)
    assert_allclose(mol.two_mo[3, 1, 2, 0], 0.7756042287284058E-01)
    assert_allclose(mol.two_mo[2, 1, 3, 0], 0.7756042287284058E-01)
    assert_allclose(mol.two_mo[0, 3, 1, 2], 0.7756042287284058E-01)
    assert_allclose(mol.two_mo[0, 2, 1, 3], 0.7756042287284058E-01)
    assert_allclose(mol.two_mo[1, 3, 0, 2], 0.7756042287284058E-01)
    assert_allclose(mol.two_mo[1, 2, 0, 3], 0.7756042287284058E-01)
    assert_allclose(mol.two_mo[3, 3, 3, 3], 0.7484308847738417E+00)


def test_dump_load_fcidimp_consistency_ao(tmpdir):
    # Setup IOData
    with path('iodata.test.data', 'water.xyz') as fn:
        mol0 = IOData.from_file(str(fn))
    mol0.nelec = 10
    mol0.ms2 = 1
    with path('iodata.test.data', 'psi4_h2_one.npy') as fn:
        mol0.one_mo = np.load(str(fn))
    with path('iodata.test.data', 'psi4_h2_two.npy') as fn:
        mol0.two_mo = np.load(str(fn))

    # Dump to a file and load it again
    fn_tmp = os.path.join(tmpdir, 'FCIDUMP')
    mol0.to_file(fn_tmp)
    mol1 = IOData.from_file(fn_tmp)

    # Compare results
    assert_equal(mol0.nelec, mol1.nelec)
    assert_equal(mol0.ms2, mol1.ms2)
    assert_allclose(mol0.one_mo, mol1.one_mo)
    assert_allclose(mol0.two_mo, mol1.two_mo)
