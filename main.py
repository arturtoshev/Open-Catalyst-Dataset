""" 
Example of how to generate adslabs from a given split and save them for later 
ML relaxation as pickle files
"""

import time
import multiprocessing as mp
from types import SimpleNamespace
from ocdata.structure_sampler import StructureSampler


def my_func(seed):
    args = SimpleNamespace(
        seed=seed,
        bulk_db='data/bulk_db_nelems_2021sep20.pkl',
        adsorbate_db='data/adsorbate_db_2021apr28.pkl',
        output_dir='outputs_id/',
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
    job = StructureSampler(args)
    job.run()


if __name__ == "__main__":

    start = time.time()

    with mp.Pool(processes=mp.cpu_count()) as pool:
        pool.map(my_func, range(5000000,5001000))
        pool.close()
    
    print(time.time() - start)
