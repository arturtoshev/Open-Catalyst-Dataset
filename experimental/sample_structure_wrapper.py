""" 
Example of how to generate adslabs from a given split and save them as pickle 
files for later ML relaxation.
"""

from types import SimpleNamespace
from ocdata.structure_sampler import StructureSampler
from pebble import ProcessPool
import os
import shutil


def my_func(args):
    job = StructureSampler(args)
    job.run()


if __name__ == "__main__":

    output_dir = "outputs_id"  # store full information
    # we would later take only adslabs_dir to run ML-based relaxations
    adslabs_dir = "outputs_id_adslabs"  # store only adslabs
    seed_range = range(5000000, 5100000)
    timeout = 600  # skip systems whose generation takes > 10 min

    inputs = []
    for i in seed_range:
        inputs.append(SimpleNamespace(
            seed=i,
            bulk_db='data/bulk_db_nelems_2021sep20.pkl',
            adsorbate_db='data/adsorbate_db_2021apr28.pkl',
            output_dir=output_dir,
            precomputed_structures='data/precomputed_surfaces_2021Sep20',
            enumerate_all_structures=False,
            adsorbate_index=None,
            bulk_indices=None,
            surface_index=None,
            verbose=True,
            write_pickle=True,
            split='id',
            splits_db='data/oc20_distribution_splits.pkl'
        )
        )

    # core part
    with ProcessPool() as pool:
        pool.map(my_func, inputs, timeout=timeout)
        pool.close()

    # generate a second output dir only containing adslab data; 
    # ~3x less data than the full output_dir. 
    os.makedirs(adslabs_dir, exist_ok=True)
    items = os.listdir(output_dir)
    items = sorted(items)
    for i in items:
        try:
            os.makedirs(os.path.join(adslabs_dir, i), exist_ok=True)
            shutil.copy2(os.path.join(output_dir, i, 'adslabatoms.pkl'),
                         os.path.join(adslabs_dir, i, 'adslabatoms.pkl'))
        except:
            print(f"Seed {i} did not lead to successfull sample.")
