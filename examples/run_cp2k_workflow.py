from aiida import load_dbenv
load_dbenv()

from aiida.common.example_helpers import test_and_get_code  # noqa
from aiida.orm.data.structure import StructureData  # noqa
from aiida.orm.data.parameter import ParameterData  # noqa
from aiida.orm.data.base import Str
from aiida.work.run import submit

from ase.io import read
from aiida_ddec.workflows import DdecCp2kChargesWorkChain

atoms = read('Cu-MOF-74.cif')

structure = StructureData(ase=atoms)
structure.store()

cp2k_options = {
    "resources": {
        "num_machines": 1,
    },
    "max_wallclock_seconds": 1 * 60 * 60,
    }

ddec_options = {
    "resources": {
        "num_machines": 1,
    },
    "max_wallclock_seconds": 1 * 60 * 60,
    "withmpi": False,
    }

cp2k_code = test_and_get_code('cp2k_6.1_18464@daint-s746', expected_code_type='cp2k')
ddec_code = test_and_get_code('chargemol_09_26_2017@daint-s746', expected_code_type='ddec')

ddec_params = ParameterData(dict={
    "net charge"                               : 0.0,
    "charge type"                              : "DDEC6",
    "periodicity along A, B, and C vectors"    : [True, True, True,],
    "compute BOs"                              : False,
    "atomic densities directory complete path" : ddec_code.get_extra("atomic_dens_dir"),
    "input filename"                           : "valence_density",
})

submit(DdecCp2kChargesWorkChain,
        structure=structure,
        cp2k_code=cp2k_code,
        _cp2k_options=cp2k_options,
#        cp2k_parent_folder=load_node(5337),
        ddec_code=ddec_code,
        _ddec_options=ddec_options,
        ddec_params=ddec_params,
        )
