import argparse

from ocdata.structure_sampler import StructureSampler


def parse_args():
    parser = argparse.ArgumentParser(description='Sample adsorbate and bulk surface(s)')

    parser.add_argument('--seed', type=int, default=None, help='Random seed for sampling')

    # input and output
    parser.add_argument('--bulk_db', type=str, required=True, help='Underlying db for bulks')
    parser.add_argument('--adsorbate_db', type=str, required=True, help='Underlying db for adsorbates')
    parser.add_argument('--output_dir', type=str, required=True, help='Root directory for outputs')

    # for optimized (automatically try to use optimized if this is provided)
    parser.add_argument('--precomputed_structures', type=str, default=None, help='Root directory of precomputed structures')

    # args for enumerating all combinations:
    parser.add_argument('--enumerate_all_structures', action='store_true', default=False,
        help='Find all possible structures given a specific adsorbate and a list of bulks')
    parser.add_argument('--adsorbate_index', type=int, default=None, help='Adsorbate index (int)')
    parser.add_argument('--bulk_indices', type=str, default=None, help='Comma separated list of bulk indices')
    parser.add_argument('--surface_index', type=int, default=None, help='Optional surface index (int)')

    parser.add_argument('--verbose', action='store_true', default=False, help='Log detailed info')

    # write adslabs to .pkl instead of vasp input files
    parser.add_argument('--write_pickle', action='store_true', default=False, help='Used to save the ase.Atoms systems as .pkl files for ML-based relaxations instead of vasp-based relaxations.')
    
    # sample structures from a specific split
    parser.add_argument('--split', type=str, default='all', choices=['all', 'id', 'val_ood', 'test_ood'], 
        help='specify a subset of ads/cat or use all by default.')
    parser.add_argument('--splits_db', type=str, required=False, 
        help='File containing a dict with keys [id_ads, id_cat, val_ood_ads, val_ood_cat, test_ood_ads, test_ood_cat], and values being sets')

    # check that all needed args are supplied
    args = parser.parse_args()
    if args.enumerate_all_structures:
        if args.adsorbate_index is None or args.bulk_indices is None:
            parser.error('Enumerating all structures requires specified adsorbate and bulks')

    elif args.seed is None:
            parser.error('Seed is required when sampling one random structure')
    return args

if __name__ == '__main__':
    args = parse_args()
    job = StructureSampler(args)
    job.run()
