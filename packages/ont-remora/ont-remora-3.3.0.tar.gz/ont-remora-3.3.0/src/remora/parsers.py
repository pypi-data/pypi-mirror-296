"""Parsers module provides all implementations of command line interfaces.

Each command should implment a `register_` function and `run_` function. The
register function should take a parser and add the appropriate entries for the
command. The run function should accept the parser.parse_args() object and
execute the command.  run commands should contain minimal logic. If run
functions become too complex consider moving logic into an appropriate betta
module. Imports required for a particular command should be made inside of the
run commands to avoid loading all modules when a user simply wants the help
string.
"""

import os
import sys
import atexit
import argparse
from pathlib import Path

from remora import constants
from remora import log, RemoraError

LOGGER = log.get_logger()


class SubcommandHelpFormatter(
    argparse.RawDescriptionHelpFormatter,
    argparse.ArgumentDefaultsHelpFormatter,
):
    """Helper function to prettier print subcommand help. This removes some
    extra lines of output when a final command parser is not selected.
    """

    def _format_action(self, action):
        parts = super(SubcommandHelpFormatter, self)._format_action(action)
        if action.nargs == argparse.PARSER:
            parts = "\n".join(parts.split("\n")[1:])
        return parts


##################
# remora dataset #
##################


def register_dataset(parser):
    subparser = parser.add_parser(
        "dataset",
        description="Remora dataset operations",
        help="Create or perform operations on a Remora dataset",
        formatter_class=SubcommandHelpFormatter,
    )
    ssubparser = subparser.add_subparsers(title="dataset commands")
    #  Since `dataset` has several sub-commands, print help as default
    subparser.set_defaults(func=lambda x: subparser.print_help())
    #  Register dataset sub commands
    register_dataset_prepare(ssubparser)
    register_dataset_prepare_basecall(ssubparser)
    register_dataset_inspect(ssubparser)
    register_dataset_make_config(ssubparser)
    register_dataset_merge(ssubparser)
    register_dataset_head(ssubparser)
    register_dataset_copy(ssubparser)
    register_dataset_make_filter(ssubparser)


def register_dataset_prepare(parser):
    subparser = parser.add_parser(
        "prepare",
        description="Prepare a core Remora dataset",
        help="Prepare a core Remora dataset",
        formatter_class=SubcommandHelpFormatter,
    )
    subparser.add_argument(
        "pod5",
        help="POD5 (file or directory) matched to bam file.",
    )
    subparser.add_argument(
        "bam",
        help="BAM file containing mv tags.",
    )

    out_grp = subparser.add_argument_group("Output Arguments")
    out_grp.add_argument(
        "--output-path",
        default="remora_training_dataset",
        help="Output Remora training dataset directory. Cannot exist unless "
        "--overwrite is specified in which case the directory will be removed.",
    )
    out_grp.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output directory if existing.",
    )

    data_grp = subparser.add_argument_group("Data Arguments")
    data_grp.add_argument(
        "--motif",
        nargs=2,
        action="append",
        metavar=("MOTIF", "FOCUS_POSITION"),
        required=True,
        help="""Motif at which the produced model is applicable. If
        --focus-reference-positions is not provided chunks will be extracted
        from motif positions as well. Argument takes 2 values representing
        1) sequence motif and 2) focus position within the motif. For example
        to restrict to CpG sites use --motif CG 0".""",
    )
    data_grp.add_argument(
        "--focus-reference-positions",
        help="""BED file containing reference positions around which to extract
        training chunks.""",
    )
    data_grp.add_argument(
        "--chunk-context",
        default=constants.DEFAULT_CHUNK_CONTEXT,
        type=int,
        nargs=2,
        metavar=("NUM_BEFORE", "NUM_AFTER"),
        help="""Number of context signal points to select around the central
        position.""",
    )
    data_grp.add_argument(
        "--min-samples-per-base",
        type=int,
        default=constants.DEFAULT_MIN_SAMPLES_PER_BASE,
        help="""Minimum number of samples per base. This sets the size of the
        ragged arrays of chunk sequences.""",
    )
    data_grp.add_argument(
        "--kmer-context-bases",
        nargs=2,
        default=constants.DEFAULT_KMER_CONTEXT_BASES,
        type=int,
        metavar=("BASES_BEFORE", "BASES_AFTER"),
        help="""Definition of k-mer (derived from the reference) passed into
        the model along with each signal position.""",
    )
    data_grp.add_argument(
        "--max-chunks-per-read",
        type=int,
        default=15,
        help="Maxiumum number of chunks to extract from a single read.",
    )
    data_grp.add_argument(
        "--base-start-justify",
        action="store_true",
        help="""Justify extracted chunk against the start of the base of
        interest. Default justifies chunk to middle of signal of the base
        of interest.""",
    )
    data_grp.add_argument(
        "--offset",
        default=0,
        type=int,
        help="Offset selected chunk position by a number of bases.",
    )
    data_grp.add_argument(
        "--num-reads",
        type=int,
        help="Number of reads.",
    )
    data_grp.add_argument(
        "--basecall-anchor",
        action="store_true",
        help="""Make dataset from basecall sequence instead of aligned
        reference sequence""",
    )
    data_grp.add_argument(
        "--reverse-signal",
        action="store_true",
        help="""Is nanopore signal 3' to 5' orientation? Primarily for direct
        RNA""",
    )
    data_grp.add_argument(
        "--picoamp-scaling-basecall-model",
        help="""Provide the path to the Dorado basecalling model directory
        which will be linke with this modified base model. Produce dataset wtih
        picoampere scaled signal. Note that this is incompatible with any
        signal mapping refine arguments""",
    )
    data_grp.add_argument(
        "--save-every",
        default=100_000,
        type=int,
        help="""Flush dataset data and update dataset size at this interval.
        Larger values will increase RAM usage, but could increase speed.""",
    )
    data_grp.add_argument(
        "--skip-shuffle",
        action="store_true",
        help="""Skip shuffle of completed dataset. Note that shuffling requires
        loading the entire signal array into memory. If dataset is very large
        and shuffling is not required specify this flag.""",
    )

    refine_grp = subparser.add_argument_group("Signal Mapping Refine Arguments")
    refine_grp.add_argument(
        "--refine-kmer-level-table",
        help="""Tab-delimited file containing no header and two fields:
        1. string k-mer sequence and 2. float expected normalized level.
        All k-mers must be the same length and all combinations of the bases
        'ACGT' must be present in the file.""",
    )
    refine_grp.add_argument(
        "--refine-rough-rescale",
        action="store_true",
        help="""Apply a rough rescaling using quantiles of signal+move table
        and levels.""",
    )
    refine_grp.add_argument(
        "--refine-scale-iters",
        default=-1,
        type=int,
        help="""Number of iterations of signal mapping refinement and signal
        re-scaling to perform. Set to 0 in order to perform signal mapping
        refinement, but skip re-scaling. Set to -1 (default) to skip signal
        mapping (potentially using levels for rough rescaling).""",
    )
    refine_grp.add_argument(
        "--refine-half-bandwidth",
        default=constants.DEFAULT_REFINE_HBW,
        type=int,
        help="""Half bandwidth around signal mapping over which to search for
        "new path.""",
    )
    refine_grp.add_argument(
        "--refine-algo",
        default=constants.DEFAULT_REFINE_ALGO,
        choices=constants.REFINE_ALGOS,
        help="Refinement algorithm to apply (if kmer level table is provided).",
    )
    refine_grp.add_argument(
        "--refine-short-dwell-parameters",
        default=constants.DEFAULT_REFINE_SHORT_DWELL_PARAMS,
        type=float,
        nargs=3,
        metavar=("TARGET", "LIMIT", "WEIGHT"),
        help="""Short dwell penalty refiner parameters. Dwells shorter than
        LIMIT will be penalized a value of `WEIGHT * (dwell - TARGET)^2`.""",
    )
    refine_grp.add_argument(
        "--rough-rescale-method",
        default=constants.DEFAULT_ROUGH_RESCALE_METHOD,
        choices=constants.ROUGH_RESCALE_METHODS,
        help="""Use either least squares or Theil-Sen estimator for rough
        rescaling.""",
    )

    label_grp = subparser.add_argument_group("Label Arguments")
    label_grp.add_argument(
        "--mod-base",
        nargs=2,
        metavar=("SHORT_NAME", "LONG_NAME"),
        help="""Modified base information. The short name should be a single
        letter modified base code or ChEBI identifier as defined in the SAM
        tags specificaions. The long name may be any longer identifier.
        Example: `--mod-base m 5mC`""",
    )
    label_grp.add_argument(
        "--mod-base-control",
        action="store_true",
        help="Is this a modified bases control sample?",
    )

    comp_grp = subparser.add_argument_group("Compute Arguments")
    comp_grp.add_argument(
        "--num-extract-alignment-workers",
        type=int,
        default=1,
        help="Number of signal extraction workers.",
    )
    comp_grp.add_argument(
        "--num-extract-chunks-workers",
        type=int,
        default=1,
        help="""Number of chunk extraction workers. If performing signal
        refinement this should be increased.""",
    )

    subparser.set_defaults(func=run_dataset_prepare)


def run_dataset_prepare(args):
    from remora.io import parse_bed
    from remora.refine_signal_map import SigMapRefiner
    from remora.prepare_train_data import extract_chunk_dataset
    from remora.util import Motif, prepare_out_dir, parse_picoamps

    prepare_out_dir(args.output_path, args.overwrite)
    if args.mod_base is None and not args.mod_base_control:
        LOGGER.error("Must specify either --mod-base or --mod-base-control")
        sys.exit(1)

    motifs = [Motif(*mo) for mo in args.motif]
    focus_ref_pos = (
        None
        if args.focus_reference_positions is None
        else parse_bed(args.focus_reference_positions)
    )
    sig_map_refiner = SigMapRefiner(
        kmer_model_filename=args.refine_kmer_level_table,
        do_rough_rescale=args.refine_rough_rescale,
        scale_iters=args.refine_scale_iters,
        algo=args.refine_algo,
        half_bandwidth=args.refine_half_bandwidth,
        sd_params=args.refine_short_dwell_parameters,
        do_fix_guage=True,
        rough_rescale_method=args.rough_rescale_method,
    )
    if not sig_map_refiner.is_valid:
        raise RemoraError("Invalid signal mapping refiner settings.")
    pa_scaling = parse_picoamps(
        args.picoamp_scaling_basecall_model, sig_map_refiner
    )
    extract_chunk_dataset(
        bam_path=args.bam,
        pod5_path=args.pod5,
        out_path=args.output_path,
        mod_base=args.mod_base,
        mod_base_control=args.mod_base_control,
        motifs=motifs,
        focus_ref_pos=focus_ref_pos,
        chunk_context=args.chunk_context,
        min_samps_per_base=args.min_samples_per_base,
        max_chunks_per_read=args.max_chunks_per_read,
        pa_scaling=pa_scaling,
        sig_map_refiner=sig_map_refiner,
        kmer_context_bases=args.kmer_context_bases,
        base_start_justify=args.base_start_justify,
        offset=args.offset,
        num_reads=args.num_reads,
        num_extract_alignment_threads=args.num_extract_alignment_workers,
        num_extract_chunks_threads=args.num_extract_chunks_workers,
        basecall_anchor=args.basecall_anchor,
        rev_sig=args.reverse_signal,
        save_every=args.save_every,
        skip_shuffle=args.skip_shuffle,
    )
    LOGGER.info("Done")


def register_dataset_prepare_basecall(parser):
    subparser = parser.add_parser(
        "prepare_basecall",
        description="Prepare a core Remora dataset for basecaller training",
        help="Prepare a core Remora dataset for basecaller training",
        formatter_class=SubcommandHelpFormatter,
    )
    subparser.add_argument(
        "pod5",
        help="POD5 (file or directory) matched to bam file.",
    )
    subparser.add_argument(
        "bam",
        help="BAM file containing mv tags.",
    )

    out_grp = subparser.add_argument_group("Output Arguments")
    out_grp.add_argument(
        "--output-path",
        default="remora_basecaller_training_dataset",
        help="Output Remora training dataset directory. Cannot exist unless "
        "--overwrite is specified in which case the directory will be removed.",
    )
    out_grp.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output directory if existing.",
    )

    data_grp = subparser.add_argument_group("Data Arguments")
    data_grp.add_argument(
        "--chunk-length",
        default=constants.DEFAULT_BASECALL_CHUNK_LEN,
        type=int,
        help="""Number of signal points to include in a chunk. Smaller chunks
        can be extracted at data reading time.""",
    )
    data_grp.add_argument(
        "--min-samples-per-base",
        type=int,
        default=constants.DEFAULT_MIN_SAMPLES_PER_BASE,
        help="""Minimum number of samples per base. This sets the size of the
        ragged arrays of chunk sequences.""",
    )
    data_grp.add_argument(
        "--kmer-context-bases",
        nargs=2,
        default=constants.DEFAULT_KMER_CONTEXT_BASES,
        type=int,
        metavar=("BASES_BEFORE", "BASES_AFTER"),
        help="""Definition of k-mer (derived from the reference) passed into
        the model along with each signal position.""",
    )
    data_grp.add_argument(
        "--max-chunks-per-read",
        type=int,
        default=15,
        help="Maxiumum number of chunks to extract from a single read.",
    )
    data_grp.add_argument(
        "--num-reads",
        type=int,
        help="Number of reads.",
    )
    data_grp.add_argument(
        "--basecall-anchor",
        action="store_true",
        help="""Make dataset from basecall sequence instead of aligned
        reference sequence""",
    )
    data_grp.add_argument(
        "--reverse-signal",
        action="store_true",
        help="""Is nanopore signal 3' to 5' orientation? Primarily for direct
        RNA""",
    )
    data_grp.add_argument(
        "--picoamp-scaling-basecall-model",
        help="""Provide the path to the Dorado basecalling model directory
        which will be linke with this modified base model. Produce dataset wtih
        picoampere scaled signal. Note that this is incompatible with any
        signal mapping refine arguments""",
    )
    data_grp.add_argument(
        "--save-every",
        default=100_000,
        type=int,
        help="""Flush dataset data and update dataset size at this interval.
        Larger values will increase RAM usage, but could increase speed.""",
    )
    data_grp.add_argument(
        "--skip-shuffle",
        action="store_true",
        help="""Skip shuffle of completed dataset. Note that shuffling requires
        loading the entire signal array into memory. If dataset is very large
        and shuffling is not required specify this flag.""",
    )
    data_grp.add_argument(
        "--shuffle-batch-size",
        type=int,
        default=200_000,
        help="""Number of training chunks to include in each shuffle. Smaller
        values will be faster, but chunks from the same read will be supplied
        together more often during training.""",
    )

    refine_grp = subparser.add_argument_group("Signal Mapping Refine Arguments")
    refine_grp.add_argument(
        "--refine-kmer-level-table",
        help="""Tab-delimited file containing no header and two fields:
        1. string k-mer sequence and 2. float expected normalized level.
        All k-mers must be the same length and all combinations of the bases
        'ACGT' must be present in the file.""",
    )
    refine_grp.add_argument(
        "--refine-rough-rescale",
        action="store_true",
        help="""Apply a rough rescaling using quantiles of signal+move table
        and levels.""",
    )
    refine_grp.add_argument(
        "--refine-scale-iters",
        default=-1,
        type=int,
        help="""Number of iterations of signal mapping refinement and signal
        re-scaling to perform. Set to 0 in order to perform signal mapping
        refinement, but skip re-scaling. Set to -1 (default) to skip signal
        mapping (potentially using levels for rough rescaling).""",
    )
    refine_grp.add_argument(
        "--refine-half-bandwidth",
        default=constants.DEFAULT_REFINE_HBW,
        type=int,
        help="""Half bandwidth around signal mapping over which to search for
        "new path.""",
    )
    refine_grp.add_argument(
        "--refine-algo",
        default=constants.DEFAULT_REFINE_ALGO,
        choices=constants.REFINE_ALGOS,
        help="Refinement algorithm to apply (if kmer level table is provided).",
    )
    refine_grp.add_argument(
        "--refine-short-dwell-parameters",
        default=constants.DEFAULT_REFINE_SHORT_DWELL_PARAMS,
        type=float,
        nargs=3,
        metavar=("TARGET", "LIMIT", "WEIGHT"),
        help="""Short dwell penalty refiner parameters. Dwells shorter than
        LIMIT will be penalized a value of `WEIGHT * (dwell - TARGET)^2`.""",
    )
    refine_grp.add_argument(
        "--rough-rescale-method",
        default=constants.DEFAULT_ROUGH_RESCALE_METHOD,
        choices=constants.ROUGH_RESCALE_METHODS,
        help="""Use either least squares or Theil-Sen estimator for rough
        rescaling.""",
    )

    comp_grp = subparser.add_argument_group("Compute Arguments")
    comp_grp.add_argument(
        "--num-extract-alignment-workers",
        type=int,
        default=1,
        help="Number of signal extraction workers.",
    )
    comp_grp.add_argument(
        "--num-extract-chunks-workers",
        type=int,
        default=1,
        help="""Number of chunk extraction workers. If performing signal
        refinement this should be increased.""",
    )

    subparser.set_defaults(func=run_dataset_prepare_basecall)


def run_dataset_prepare_basecall(args):
    from remora.refine_signal_map import SigMapRefiner
    from remora.util import prepare_out_dir, parse_picoamps
    from remora.prepare_train_data import extract_basecall_chunk_dataset

    prepare_out_dir(args.output_path, args.overwrite)

    sig_map_refiner = SigMapRefiner(
        kmer_model_filename=args.refine_kmer_level_table,
        do_rough_rescale=args.refine_rough_rescale,
        scale_iters=args.refine_scale_iters,
        algo=args.refine_algo,
        half_bandwidth=args.refine_half_bandwidth,
        sd_params=args.refine_short_dwell_parameters,
        do_fix_guage=True,
        rough_rescale_method=args.rough_rescale_method,
    )
    if not sig_map_refiner.is_valid:
        raise RemoraError("Invalid signal mapping refiner settings.")
    pa_scaling = parse_picoamps(
        args.picoamp_scaling_basecall_model, sig_map_refiner
    )
    extract_basecall_chunk_dataset(
        bam_path=args.bam,
        pod5_path=args.pod5,
        out_path=args.output_path,
        chunk_context=(0, args.chunk_length),
        min_samps_per_base=args.min_samples_per_base,
        max_chunks_per_read=args.max_chunks_per_read,
        pa_scaling=pa_scaling,
        sig_map_refiner=sig_map_refiner,
        kmer_context_bases=args.kmer_context_bases,
        num_reads=args.num_reads,
        num_extract_alignment_threads=args.num_extract_alignment_workers,
        num_extract_chunks_threads=args.num_extract_chunks_workers,
        basecall_anchor=args.basecall_anchor,
        rev_sig=args.reverse_signal,
        save_every=args.save_every,
        skip_shuffle=args.skip_shuffle,
    )
    LOGGER.info("Done")


def register_dataset_inspect(parser):
    subparser = parser.add_parser(
        "inspect",
        description="Inspect Remora dataset",
        help="Inspect Remora dataset",
        formatter_class=SubcommandHelpFormatter,
    )
    subparser.add_argument(
        "remora_dataset_path",
        help="Remora training dataset",
    )
    subparser.add_argument(
        "--out-path",
        help="Path to save new config with hierarchical datasets expanded "
        "and dataset hash values included.",
    )
    subparser.set_defaults(func=run_dataset_inspect)


def run_dataset_inspect(args):
    import json

    from remora.data_chunks import load_dataset

    dataset = load_dataset(
        args.remora_dataset_path,
        core_ds_kwargs={"do_check_super_batches": True},
    )
    print(f"Dataset summary:\n{dataset.summary}")
    if args.out_path is not None:
        with open(args.out_path, "w") as fh:
            json.dump(dataset.get_config(), fh)


def register_dataset_make_config(parser):
    subparser = parser.add_parser(
        "make_config",
        description="""Create Remora dataset from core datasets. This will not
        copy data. The config file points to the core datasets and generates
        batches with specified proportions from each core dataset.""",
        help="Create Remora dataset from core datasets",
        formatter_class=SubcommandHelpFormatter,
    )
    subparser.add_argument(
        "out_path",
        help="Path to save new config.",
    )
    subparser.add_argument(
        "dataset_paths",
        nargs="+",
        help="""Remora training dataset. May be either a core Remora dataset or
        another config""",
    )
    subparser.add_argument(
        "--dataset-weights",
        type=float,
        nargs="+",
        help="""Specify weights to apply to each input dataset. Must be the
        same length as the input datasets if provided. Default will create
        config with weights equal to the size of each dataset (drawing chunks
        globally with equal probability)""",
    )
    subparser.add_argument(
        "--dataset-filters",
        nargs="+",
        help="""Specify filters file(s) to be applied to each dataset. Must be
        the same length as the input datasets if provided. See remora dataset
        make_filter for details.""",
    )
    subparser.add_argument(
        "--log-filename",
        help="Log filename. Default: Don't output log file.",
    )
    subparser.set_defaults(func=run_dataset_make_config)


def run_dataset_make_config(args):
    import json
    from itertools import repeat

    import numpy as np

    from remora.data_chunks import load_dataset, RemoraDataset

    if args.log_filename is not None:
        log.init_logger(args.log_filename)
    if args.dataset_weights is None:
        ds_weights = repeat(None)
    else:
        if len(args.dataset_weights) != len(args.dataset_paths):
            raise RemoraError("Weights must be same length as input datasets.")
        if any(w < 0 for w in args.dataset_weights):
            raise RemoraError("Weights must not be negative.")
        ds_weights = args.dataset_weights
    if args.dataset_filters is None:
        dss_filts = repeat(None)
    else:
        if len(args.dataset_filters) != len(args.dataset_paths):
            raise RemoraError("Filters must be same length as input datasets.")
        dss_filts = args.dataset_filters
    core_datasets, core_weights, core_hashes = [], [], []
    for ds_path, ds_weight, ds_filts in zip(
        args.dataset_paths, ds_weights, dss_filts
    ):
        if ds_filts == "None":
            ds_filts = None
        dataset = load_dataset(
            ds_path, core_ds_kwargs={"filters_path": ds_filts}
        )
        if any(dataset.props == 0):
            empty_datasets = ", ".join(
                [p for p, w in zip(dataset.paths, dataset.props) if w == 0]
            )
            raise RemoraError(f"Encountered empty dataset: {empty_datasets}")
        weights = dataset.props.copy()
        if ds_weight is None:
            weights *= sum([ds.size for ds in dataset.datasets])
        else:
            weights *= ds_weight
        for ds, ds_weight, ds_hash in zip(
            dataset.datasets, weights, dataset.hashes
        ):
            # skip zero weight datasets
            if ds_weight <= 0:
                continue
            core_datasets.append(ds)
            core_weights.append(ds_weight)
            core_hashes.append(ds_hash)
    core_weights = np.array(core_weights)
    dataset = RemoraDataset(
        core_datasets,
        core_weights / core_weights.sum(),
        core_hashes,
    )
    with open(args.out_path, "w") as fh:
        json.dump(dataset.get_config(), fh)
    LOGGER.info("\n" + dataset.summary)


def register_dataset_merge(parser):
    subparser = parser.add_parser(
        "merge",
        description="""Merge core Remora datasets. This will duplicate the data
        on disk, but allow more efficient data access. Also note that chunks
        are selected randomly from merged datasets.""",
        help="Merge core Remora datasets",
        formatter_class=SubcommandHelpFormatter,
    )
    subparser.add_argument(
        "out_path",
        help="Path to save new dataset.",
    )
    subparser.add_argument(
        "dataset_paths",
        nargs="+",
        help="""Remora training dataset. May be either a core Remora dataset or
        another config""",
    )
    subparser.add_argument(
        "--max-size",
        type=int,
        help="""Maximum size of output dataset""",
    )
    subparser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output directory if existing.",
    )
    subparser.set_defaults(func=run_dataset_merge)


def run_dataset_merge(args):
    import numpy as np
    from tqdm import tqdm

    from remora.data_chunks import (
        compute_best_split,
        extract_core_dataset_paths,
        CoreRemoraDataset,
        RemoraDataset,
        DATASET_VERSION,
    )
    from remora.util import prepare_out_dir

    prepare_out_dir(args.out_path, args.overwrite)
    all_paths = [
        sub_ds_path
        for ds_path in args.dataset_paths
        for sub_ds_path in extract_core_dataset_paths(ds_path)
    ]
    dataset = RemoraDataset(
        [
            CoreRemoraDataset(
                path, infinite_iter=False, do_check_super_batches=True
            )
            for path in all_paths
        ],
        np.ones(len(all_paths)),
    )
    common_extra_arrays = set.intersection(
        *[set(ds.metadata.extra_array_names) for ds in dataset.datasets]
    )

    LOGGER.info(f"Loaded dataset:\n{dataset.summary}")
    merged_metadata = dataset.metadata.copy()
    ds_out_sizes = np.array([ds.size for ds in dataset.datasets])
    if args.max_size is not None and ds_out_sizes.sum() > args.max_size:
        ds_out_sizes = compute_best_split(
            args.max_size, ds_out_sizes / ds_out_sizes.sum()
        )
    merged_metadata.allocate_size = ds_out_sizes.sum()
    merged_metadata.max_seq_len = max(
        ds.metadata.max_seq_len for ds in dataset.datasets
    )
    merged_metadata.dataset_start = 0
    merged_metadata.dataset_end = 0
    merged_metadata.version = DATASET_VERSION

    merged_dataset = CoreRemoraDataset(
        data_path=args.out_path,
        mode="w",
        metadata=merged_metadata,
    )
    merged_dataset.write_metadata()
    LOGGER.info("Copying datasets")
    for ds, ds_out_size in tqdm(
        zip(dataset.datasets, ds_out_sizes),
        smoothing=0,
        dynamic_ncols=True,
        desc="Datasets",
        total=ds_out_sizes.size,
    ):
        if ds.metadata.dataset_end != ds_out_size:
            LOGGER.debug(
                f"Reducing dataset size from {ds.metadata.dataset_end:,} to "
                f"{ds_out_size:,}"
            )
            ds.metadata.dataset_end = ds_out_size
        total_sbs = ds.size // ds.super_batch_size
        LOGGER.debug(f"Adding dataset from {ds.data_path}")
        ds.set_return_arrays(common_extra_arrays)
        for sb_idx, sb in tqdm(
            enumerate(ds.iter_super_batches()),
            smoothing=0,
            dynamic_ncols=True,
            total=total_sbs,
            leave=False,
            position=1,
            desc="Batches",
        ):
            merged_dataset.write_batch(sb)
            merged_dataset.flush()
            merged_dataset.write_metadata()
            if sb_idx % 10 == 9:
                # update every 10 batches
                LOGGER.debug(f"{sb_idx + 1}/{total_sbs} super batches complete")
    LOGGER.info("Shuffling dataset")
    merged_dataset.shuffle(show_prog=True)
    LOGGER.info(f"Saved core dataset:\n{merged_dataset.summary}")


def register_dataset_head(parser):
    subparser = parser.add_parser(
        "head",
        description="""Create new core dataset with a selection of the first
        reads from another core dataset.""",
        help="Create new core dataset from beginning of another",
        formatter_class=SubcommandHelpFormatter,
    )
    subparser.add_argument(
        "out_path",
        help="Path to save new dataset.",
    )
    subparser.add_argument(
        "in_path",
        help="""Input core Remora dataset (cannot be a config dataset).""",
    )
    subparser.add_argument(
        "num_chunks",
        type=int,
        help="""Number of chunks to select""",
    )
    subparser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output directory if existing.",
    )
    subparser.set_defaults(func=run_dataset_head)


def run_dataset_head(args):
    from tqdm import tqdm

    from remora.util import prepare_out_dir
    from remora.data_chunks import CoreRemoraDataset

    prepare_out_dir(args.out_path, args.overwrite)
    in_ds = CoreRemoraDataset(
        args.in_path, infinite_iter=False, do_check_super_batches=True
    )
    LOGGER.info(f"Loaded dataset:\n{in_ds.summary}")
    head_metadata = in_ds.metadata.copy()
    head_metadata.allocate_size = args.num_chunks
    head_metadata.dataset_start = 0
    head_metadata.dataset_end = 0

    head_dataset = CoreRemoraDataset(
        data_path=args.out_path,
        mode="w",
        metadata=head_metadata,
    )
    head_dataset.write_metadata()
    LOGGER.info("Extracting head data")
    for sb_idx, sb in tqdm(
        enumerate(in_ds.iter_super_batches()),
        smoothing=0,
        dynamic_ncols=True,
        leave=False,
        position=1,
        desc="Batches",
    ):
        if (
            head_dataset.metadata.dataset_end + sb["sequence_lengths"].size
            >= args.num_chunks
        ):
            num_chunks = args.num_chunks - head_dataset.metadata.dataset_end
            sb = dict(
                (arr_name, arr[:num_chunks]) for arr_name, arr in sb.items()
            )
            # add last batch and exit
            head_dataset.write_batch(sb)
            head_dataset.flush()
            head_dataset.write_metadata()
            LOGGER.debug(f"{sb_idx + 1} super batches complete (last batch)")
            break
        head_dataset.write_batch(sb)
        head_dataset.flush()
        head_dataset.write_metadata()
        LOGGER.debug(f"{sb_idx + 1} super batches complete")

    LOGGER.info("Shuffling dataset")
    head_dataset.shuffle(show_prog=True)
    LOGGER.info(f"Saved core dataset:\n{head_dataset.summary}")


def register_dataset_copy(parser):
    subparser = parser.add_parser(
        "copy",
        description="""Copy dataset to a new location. Useful for moving
        multi-part datasets to faster disk access locations. New config will be
        at [out_path]/dataset.cfg and core datasets will be sub-directories
        [out_path]/dataset_001, [out_path]/dataset_002, etc.""",
        help="Copy dataset to new location",
        formatter_class=SubcommandHelpFormatter,
    )
    subparser.add_argument(
        "in_path",
        help="""Input core Remora dataset (config or core dataset).""",
    )
    subparser.add_argument(
        "out_path",
        help="Path to save new datasets.",
    )
    subparser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output directory if existing.",
    )
    subparser.set_defaults(func=run_dataset_copy)


def run_dataset_copy(args):
    import json
    import shutil

    from remora.util import prepare_out_dir
    from remora.data_chunks import (
        load_dataset,
        CoreRemoraDataset,
        RemoraDataset,
    )

    out_dir = Path(args.out_path)
    prepare_out_dir(args.out_path, args.overwrite)
    in_dataset = load_dataset(args.in_path)
    src_fh = open(out_dir / "sources.txt", "w")
    ds_out_dirs = []
    if in_dataset.num_datasets > 10_000:
        raise RemoraError("Cannot copy more than 10,000 datasets")
    for ds_idx, src_path in enumerate(in_dataset.paths):
        for item in os.listdir(src_path):
            if os.path.isdir(os.path.join(src_path, item)):
                raise RemoraError(
                    f"Source dataset has nested directory: {item}"
                )
        ds_out_dir = out_dir / f"dataset_{ds_idx:05}"
        ds_out_dirs.append(ds_out_dir)
        src_fh.write(f"{src_path}\t{ds_out_dir}\n")
        try:
            shutil.copytree(src_path, ds_out_dir)
            LOGGER.info(f"'{src_path}' copied to '{ds_out_dir}' successfully.")
        except FileExistsError:
            raise RemoraError(f"Destination '{ds_out_dir}' already exists.")
        except FileNotFoundError:
            raise RemoraError(f"Source '{src_path}' does not exist.")
        except PermissionError:
            raise RemoraError("Permission denied.")
        except Exception as e:
            RemoraError(f"Error: {e}")
    src_fh.close()
    dataset = RemoraDataset(
        [
            CoreRemoraDataset(ds_out_dir, filters_path=ds_filts_path)
            for ds_out_dir, ds_filts_path in zip(
                ds_out_dirs, in_dataset.filter_paths
            )
        ],
        in_dataset.props,
        in_dataset._hashes,
    )
    with open(out_dir / "dataset.cfg", "w") as fh:
        json.dump(dataset.get_config(), fh)
    LOGGER.info(dataset.summary)


def register_dataset_make_filter(parser):
    subparser = parser.add_parser(
        "make_filter",
        description="""Make dataset filter. Filters will be applied at access
        time and will not effect the dataset contents.""",
        help="Create dataset filter",
        formatter_class=SubcommandHelpFormatter,
    )
    subparser.add_argument(
        "--dataset",
        help="""Dataset path. Filter will be saved in the default location and
        applied by default.""",
    )
    subparser.add_argument(
        "--output-filter-path",
        help="""Output path for filter file.""",
    )
    subparser.add_argument(
        "--filter",
        nargs=4,
        metavar=("COLUMN", "OPERATOR", "THRESHOLD", "IS_QUANTILE"),
        action="append",
        help="""Filter to be applied. Four values are required and represent
        the 1) column to be filtered (must be available in dataset or specified
        in remora.data_chunks.DatasetFilters.derived_cols), 2) operator to be
        applied (must be attribute of operator package) 3) threshold value,
        and 4) is the thershold value a quantile? (default is a raw threshold
        value)""",
    )
    subparser.add_argument(
        "--store-raw-thresholds",
        action="store_true",
        help="""Store raw threshold to avoid computing these at access time.
        Storing quantiles where specified will make a filter file which can be
        copied to new datasets retaining the quantile value.""",
    )
    subparser.add_argument(
        "--log-filename",
        help="Log filename. Default: Don't output log file.",
    )
    subparser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing filter file.",
    )
    subparser.set_defaults(func=run_dataset_make_filter)


def run_dataset_make_filter(args):
    import json

    from remora import log, util
    from remora.data_chunks import (
        load_dataset,
        CoreRemoraDataset,
        DatasetFilters,
    )

    def open_filter_file(path):
        if path.exists() and not args.overwrite:
            raise RemoraError(
                "Filter file already exists and --overwrite not specified"
            )
        return open(path, "w")

    if args.log_filename is not None:
        log.init_logger(args.log_filename)

    raw_filters = [
        (col, op_str, float(thresh), util.str_to_bool(is_quantile))
        for col, op_str, thresh, is_quantile in args.filter
    ]
    if args.dataset is not None:
        ds = load_dataset(args.dataset)
        if ds.num_datasets == 1:
            ds = ds.datasets[0]
        else:
            raise NotImplementedError("Cannot apply filter to config dataset")
        filt_path = (
            Path(ds.data_path) / CoreRemoraDataset._filters_path
            if args.output_filter_path is None
            else Path(args.output_filter_path)
        )
        filt_fh = open_filter_file(filt_path)
        # load filters to validate and compute quantiles
        filters = DatasetFilters.from_raw_filters(raw_filters, ds)
        if args.store_raw_thresholds:
            raw_filters = filters.storage_filters
    elif args.output_filter_path is not None:
        filt_fh = open_filter_file(Path(args.output_filter_path))
    else:
        if args.store_raw_thresholds and any(
            isq for _, _, _, isq in raw_filters
        ):
            raise RemoraError(
                """Cannot store computed quantile values without loading a
                dataset"""
            )
        filt_fh = sys.stdout
    json.dump(raw_filters, filt_fh)
    if filt_fh != sys.stdout:
        filt_fh.close()


################
# remora model #
################


def register_model(parser):
    subparser = parser.add_parser(
        "model",
        description="Remora model operations",
        help="Train or perform operations on Remora models",
        formatter_class=SubcommandHelpFormatter,
    )
    ssubparser = subparser.add_subparsers(title="model commands")
    #  Since `model` has several sub-commands, print help as default
    subparser.set_defaults(func=lambda x: subparser.print_help())
    #  Register model sub commands
    register_model_train(ssubparser)
    register_model_inspect(ssubparser)
    register_model_export(ssubparser)
    register_model_list_pretrained(ssubparser)
    register_model_download(ssubparser)


def register_model_train(parser):
    def none_or_float(x):
        if x == "None":
            return
        return float(x)

    subparser = parser.add_parser(
        "train",
        description="Train Remora model",
        help="Train Remora model",
        formatter_class=SubcommandHelpFormatter,
    )

    subparser.add_argument(
        "remora_dataset_path",
        help="Remora training dataset",
    )

    data_grp = subparser.add_argument_group("Data Arguments")
    data_grp.add_argument(
        "--batch-size",
        default=constants.DEFAULT_BATCH_SIZE,
        type=int,
        help="Number of samples per batch.",
    )
    data_grp.add_argument(
        "--chunk-context",
        type=int,
        nargs=2,
        metavar=("NUM_BEFORE", "NUM_AFTER"),
        help="""Override chunk context from data prep. Number of context signal
        points to select around the central position.""",
    )
    data_grp.add_argument(
        "--kmer-context-bases",
        nargs=2,
        type=int,
        metavar=("BASES_BEFORE", "BASES_AFTER"),
        help="""Override kmer context bases from data prep. Definition of
        k-mer passed into the model along with each signal position.""",
    )
    data_grp.add_argument(
        "--ext-val",
        nargs="+",
        help="Path(s) to the external validation Remora datasets.",
    )
    data_grp.add_argument(
        "--ext-val-names",
        nargs="+",
        help="""Names for external datasets. If provided must match length of
        [--ext-val] argument""",
    )
    data_grp.add_argument(
        "--chunks-per-epoch",
        default=constants.DEFAULT_CHUNKS_PER_EPOCH,
        type=int,
        help="Number of chunks per-epoch.",
    )
    data_grp.add_argument(
        "--num-test-chunks",
        default=constants.DEFAULT_NUM_TEST_CHUNKS,
        type=int,
        help="Number of chunks per-epoch.",
    )
    data_grp.add_argument(
        "--filter-fraction",
        default=constants.DEFAULT_FILT_FRAC,
        type=float,
        help="""Fraction of predictions to filter in validation reporting.
        Un-filtered validation metrics will always be reported as well.""",
    )

    out_grp = subparser.add_argument_group("Output Arguments")
    out_grp.add_argument(
        "--output-path",
        default="remora_train_results",
        help="Path to the output files.",
    )
    out_grp.add_argument(
        "--save-freq",
        default=10,
        type=int,
        help="After how many epochs to save the model.",
    )
    out_grp.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output directory if existing.",
    )

    mdl_grp = subparser.add_argument_group("Model Arguments")
    mdl_grp.add_argument(
        "--model", required=True, help="Model architecture file (required)"
    )
    mdl_grp.add_argument(
        "--finetune-path",
        help="Path to the torch checkpoint for the model to be fine tuned.",
    )
    mdl_grp.add_argument(
        "--freeze-num-layers",
        default=0,
        type=int,
        help="Number of layers to be frozen for finetuning.",
    )
    mdl_grp.add_argument(
        "--size",
        type=int,
        default=constants.DEFAULT_NN_SIZE,
        help="Model layer size.",
    )

    train_grp = subparser.add_argument_group("Training Arguments")
    train_grp.add_argument(
        "--epochs",
        default=constants.DEFAULT_EPOCHS,
        type=int,
        help="Number of training epochs.",
    )
    train_grp.add_argument(
        "--optimizer",
        default=constants.DEFAULT_OPTIMIZER,
        help="Optimizer. Select from torch.optim",
    )
    train_grp.add_argument(
        "--optimizer-kwargs",
        nargs=3,
        action="append",
        metavar=("NAME", "VALUE", "TYPE"),
        help="""Arguments to torch optimizer. TYPE should be str, int or float.
        Default: """
        + " ".join(
            f"--optimizer-kwargs {n} {v} {t}"
            for n, v, t in constants.DEFAULT_OPT_VALUES
        ),
    )
    train_grp.add_argument(
        "--lr",
        default=constants.DEFAULT_LR,
        type=float,
        help="Learning rate",
    )
    train_grp.add_argument(
        "--lr-scheduler",
        default=constants.DEFAULT_SCHEDULER,
        help="""Torch learning rate scheduler. Select from
        torch.optim.lr_scheduler""",
    )
    train_grp.add_argument(
        "--lr-scheduler-kwargs",
        nargs=3,
        action="append",
        metavar=("NAME", "VALUE", "TYPE"),
        help="""Arguments to torch scheduler. TYPE should be str, int or float,
        Default: """
        + " ".join(
            f"--lr-scheduler-kwargs {n} {v} {t}"
            for n, v, t in constants.DEFAULT_SCH_VALUES
        ),
    )
    train_grp.add_argument(
        "--lr-cool-down-epochs",
        type=int,
        default=constants.DEFAULT_SCH_COOL_DOWN_EPOCHS,
        help="Number of cool down epochs at the end of training",
    )
    train_grp.add_argument(
        "--lr-cool-down-learning-rate",
        type=int,
        default=constants.DEFAULT_SCH_COOL_DOWN_LR,
        help="Cool down learning rate at the end of training",
    )
    train_grp.add_argument(
        "--early-stopping",
        default=constants.DEFAULT_EARLY_STOPPING,
        type=int,
        help="""Stops training after a number of epochs without improvement.
        If set to 0 no stopping is done.""",
    )
    train_grp.add_argument(
        "--seed",
        type=int,
        help="Seed value.",
    )
    train_grp.add_argument(
        "--high-conf-incorrect-thr-frac",
        nargs=2,
        type=float,
        metavar=("THRESHOLD", "FRACTION"),
        help="""Filter highly confident but incorrect chunks from training each
        iteration. First value sets the threshold for high confidence
        predictions and second value sets the maximum fraction of chunks to
        filter per batch.""",
    )
    train_grp.add_argument(
        "--gradient-clip-num-mads",
        default=0,
        type=none_or_float,
        help="""Clip gradients (by value) at num_MADs above the median of
        the last 1000 parameter gradient maximums. Gradient threshold
        values are computed for each parameter group independently. Use
        "--gradient-clip-num-mads None" for no clipping.""",
    )

    comp_grp = subparser.add_argument_group("Compute Arguments")
    comp_grp.add_argument(
        "--device",
        help="Device for neural network processing. See torch.device.",
    )
    comp_grp.add_argument(
        "--super-batch-size",
        default=constants.DEFAULT_SUPER_BATCH_SIZE,
        type=int,
        help="""Number of chunks to load off disk at one time. Larger values
        may improve disk IO, but also increase RAM usage.""",
    )
    comp_grp.add_argument(
        "--super-batch-sample-fraction",
        default=constants.DEFAULT_SUPER_BATCH_SAMPLE_FRAC,
        type=float,
        help="""Fraction of loaded super batch to use. Smaller values will
        increase randomness, but also increase disk IO required.""",
    )
    data_grp.add_argument(
        "--read-batches-from-disk",
        action="store_true",
        help="""Read validation batches from disk each iteration. Default:
        loads all batches into memory once upfront. Setting this flag may
        reduce RAM usage.""",
    )

    subparser.set_defaults(func=run_model_train)


def run_model_train(args):
    from remora.model_util import TrainOpts
    from remora.train_model import train_model
    from remora.util import parse_device, prepare_out_dir

    prepare_out_dir(args.output_path, args.overwrite)
    PROF_TRAIN_FN = os.getenv("REMORA_TRAIN_PROFILE_FILE")
    if PROF_TRAIN_FN is not None:
        from torch.profiler import profile, ProfilerActivity

        train_model_wrapper = train_model

        def train_model(*args):
            with profile(
                activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]
            ) as prof:
                train_model_wrapper(*args)
            prof.export_chrome_trace(PROF_TRAIN_FN)

    train_opts = TrainOpts(
        epochs=args.epochs,
        early_stopping=args.early_stopping,
        optimizer_str=args.optimizer,
        opt_kwargs=args.optimizer_kwargs,
        learning_rate=args.lr,
        lr_scheduler_str=args.lr_scheduler,
        lr_scheduler_kwargs=args.lr_scheduler_kwargs,
        lr_cool_down_epochs=args.lr_cool_down_epochs,
        lr_cool_down_lr=args.lr_cool_down_learning_rate,
    )
    train_model(
        args.seed,
        parse_device(args.device),
        Path(args.output_path),
        args.remora_dataset_path,
        args.chunk_context,
        args.kmer_context_bases,
        args.batch_size,
        args.model,
        args.size,
        train_opts,
        args.chunks_per_epoch,
        args.num_test_chunks,
        args.save_freq,
        args.filter_fraction,
        args.ext_val,
        args.ext_val_names,
        args.high_conf_incorrect_thr_frac,
        args.finetune_path,
        args.freeze_num_layers,
        args.super_batch_size,
        args.super_batch_sample_fraction,
        args.read_batches_from_disk,
        args.gradient_clip_num_mads,
    )
    LOGGER.info("Done")


def register_model_inspect(parser):
    subparser = parser.add_parser(
        "inspect",
        description="Inspect a Remora model",
        help="Inspect a Remora model",
        formatter_class=SubcommandHelpFormatter,
    )
    subparser.add_argument(
        "checkpoint_path",
        help="Path to a pretrained model checkpoint.",
    )
    subparser.add_argument(
        "--model-path",
        help="Path to a model architecture. Default: Use path from checkpoint.",
    )

    subparser.set_defaults(func=run_model_inspect)


def run_model_inspect(args):
    from remora.model_util import (
        continue_from_checkpoint,
        load_torchscript_model,
        repr_model_metadata,
    )
    from remora.refine_signal_map import SigMapRefiner

    LOGGER.info("Loading model")
    try:
        model, model_metadata = load_torchscript_model(args.checkpoint_path)
        LOGGER.info("Loaded a torchscript model")
    except RuntimeError:
        model_metadata, model = continue_from_checkpoint(
            args.checkpoint_path, args.model_path
        )
        # TODO add function in model_util for this simmilar to
        # add_derived_metadata for .pt models
        if (
            "refine_kmer_levels" in model_metadata
            and model_metadata["refine_kmer_levels"] is not None
        ):
            # load sig_map_refiner
            model_metadata["sig_map_refiner"] = SigMapRefiner(
                _levels_array=model_metadata["refine_kmer_levels"],
                center_idx=int(model_metadata["refine_kmer_center_idx"]),
                do_rough_rescale=model_metadata["refine_do_rough_rescale"],
                scale_iters=int(model_metadata["refine_scale_iters"]),
                algo=model_metadata["refine_algo"],
                half_bandwidth=int(model_metadata["refine_half_bandwidth"]),
                sd_arr=model_metadata["refine_sd_arr"],
            )
        else:
            # handle original models without sig_map_refiner
            model_metadata["sig_map_refiner"] = SigMapRefiner()
            model_metadata["base_start_justify"] = False
            model_metadata["offset"] = 0
        for md_name in [
            md_name
            for md_name in model_metadata.keys()
            if md_name.startswith("refine_")
        ]:
            del model_metadata[md_name]
        for md_name in ["state_dict", "opt"]:
            del model_metadata[md_name]
        LOGGER.info("Loaded model from checkpoint")

    md_str = repr_model_metadata(model_metadata)
    LOGGER.info(f"Loaded Remora model attrs\n{md_str}\n")
    LOGGER.info("Done")


def register_model_export(parser):
    subparser = parser.add_parser(
        "export",
        description="Export a model to TorchScript format for inference",
        help="Export a model to TorchScript format for inference",
        formatter_class=SubcommandHelpFormatter,
    )
    subparser.add_argument(
        "checkpoint_path",
        help="Path to a pretrained model checkpoint.",
    )
    subparser.add_argument(
        "output_path",
        help="Path or directory to save the model.",
    )
    subparser.add_argument(
        "--model-path",
        help="Path to a model architecture. Default: Use path from checkpoint.",
    )
    subparser.add_argument(
        "--format",
        default="dorado",
        choices=["dorado", "torchscript"],
        help="Export format.",
    )

    subparser.set_defaults(func=run_model_export)


def run_model_export(args):
    from remora.model_util import (
        continue_from_checkpoint,
        load_torchscript_model,
        export_model_dorado,
        export_model_torchscript,
    )

    LOGGER.info("Loading model")
    try:
        model, ckpt = load_torchscript_model(args.checkpoint_path)
        LOGGER.info("Loaded a torchscript model")
    except RuntimeError:
        ckpt, model = continue_from_checkpoint(
            args.checkpoint_path, args.model_path
        )
        LOGGER.info("Loaded model from checkpoint")

    if args.format == "dorado":
        LOGGER.info("Exporting model to dorado format")
        export_model_dorado(ckpt, model, args.output_path)
    elif args.format == "torchscript":
        LOGGER.info("Exporting model to TorchScript format")
        export_model_torchscript(ckpt, model, args.output_path)
    else:
        raise RemoraError(f"Invalid export format: {args.format}")
    LOGGER.info("Done")


def register_model_list_pretrained(parser):
    subparser = parser.add_parser(
        "list_pretrained",
        description="List pre-trained modified base models",
        help="List pre-trained modified base models",
        formatter_class=SubcommandHelpFormatter,
    )
    subparser.add_argument("--pore", help="specify pore type")
    subparser.add_argument(
        "--basecall-model-type",
        help="Specify the basecaller model type (e.g., fast, hac or sup)",
    )
    subparser.add_argument(
        "--basecall-model-version", help="Specify basecaller model version"
    )
    subparser.add_argument(
        "--modified-bases",
        nargs="+",
        help="Specify the modified base(s)",
    )
    subparser.add_argument(
        "--remora-model-type",
        help="Specify model motif (sequence context)",
    )
    subparser.add_argument(
        "--remora-model-version", type=int, help="Specify Remora model version"
    )
    subparser.set_defaults(func=run_list_pretrained)


def run_list_pretrained(args):
    import polars as pl

    from remora.model_util import get_pretrained_models

    pl.Config.set_tbl_hide_column_data_types(True)
    pl.Config.set_tbl_hide_dataframe_shape(True)
    pl.Config.set_tbl_width_chars(200)
    pl.Config.set_fmt_str_lengths(250)
    pl.Config.set_tbl_rows(50)

    models = get_pretrained_models(
        args.pore,
        args.basecall_model_type,
        args.basecall_model_version,
        args.modified_bases,
        args.remora_model_type,
        args.remora_model_version,
    )
    LOGGER.info("Remora pretrained modified base models:\n" + str(models))


def register_model_download(parser):
    subparser = parser.add_parser(
        "download",
        description="Download pre-trained modified base models",
        help="Download pre-trained modified base models",
        formatter_class=SubcommandHelpFormatter,
    )
    subparser.add_argument("--pore", help="specify pore type")
    subparser.add_argument(
        "--basecall-model-type",
        help="Specify the basecaller model type (e.g., fast, hac or sup)",
    )
    subparser.add_argument(
        "--basecall-model-version", help="Specify basecaller model version"
    )
    subparser.add_argument(
        "--modified-bases",
        nargs="+",
        help="Specify the modified base(s)",
    )
    subparser.add_argument(
        "--remora-model-type",
        help="Specify model motif (sequence context)",
    )
    subparser.add_argument(
        "--remora-model-version", help="Specify Remora model version"
    )
    subparser.set_defaults(func=run_download)


def run_download(args):
    import pkg_resources

    from remora.download import ModelDownload
    from remora.model_util import get_pretrained_models

    models = get_pretrained_models(
        args.pore,
        args.basecall_model_type,
        args.basecall_model_version,
        args.modified_bases,
        args.remora_model_type,
        args.remora_model_version,
    )
    path = pkg_resources.resource_filename(
        "remora",
        constants.MODEL_DATA_DIR_NAME,
    )
    out_path = Path(path)
    out_path.mkdir(parents=True, exist_ok=True)
    model_dl = ModelDownload(out_path)
    for model_url in models["Remora\nModel\nURL"]:
        if model_url != "":
            model_dl.download(model_url)
    LOGGER.info("Done")


################
# remora infer #
################


def register_infer(parser):
    subparser = parser.add_parser(
        "infer",
        description="Perform Remora model inference",
        help="Perform Remora model inference",
        formatter_class=SubcommandHelpFormatter,
    )
    ssubparser = subparser.add_subparsers(title="infer commands")
    # Since `infer` has several sub-commands, print help as default
    subparser.set_defaults(func=lambda x: subparser.print_help())
    # Register infer sub commands
    register_infer_from_pod5_and_bam(ssubparser)
    register_infer_duplex_from_pod5_and_bam(ssubparser)


def register_infer_from_pod5_and_bam(parser):
    subparser = parser.add_parser(
        "from_pod5_and_bam",
        description="Infer modified bases from pod5 and bam inputs",
        help="Run inference on pod5s and alignments",
        formatter_class=SubcommandHelpFormatter,
    )
    subparser.add_argument(
        "pod5",
        help="POD5 (file or directory) matched to bam file.",
    )
    subparser.add_argument(
        "in_bam",
        help="BAM file containing mv tags.",
    )

    out_grp = subparser.add_argument_group("Output Arguments")
    out_grp.add_argument("--out-bam", help="Output BAM path.", required=True)
    out_grp.add_argument(
        "--log-filename",
        help="Log filename. Default: Don't output log file.",
    )
    out_grp.add_argument(
        "--preserve-move-tag",
        action="store_true",
        help="Preserve move tables in output BAM file.",
    )

    mdl_grp = subparser.add_argument_group(
        "Model Arguments",
        """Specify model. --model can be specified multiple times, but only
        one model can be specified per canonical base. Additional arguments
        will select a default model given sufficient specificty (pore and
        modified base).""",
    )
    mdl_grp.add_argument(
        "--model",
        action="append",
        help="Path(s) to a pretrained model in torchscript format.",
    )
    mdl_grp.add_argument(
        "--pore",
        help="Choose the type of pore the Remora model has been trained on "
        "(e.g. dna_r10.4_e8.1)",
    )
    mdl_grp.add_argument(
        "--basecall-model-type",
        help="Choose the basecaller model type (choose from fast, hac or sup)",
    )
    mdl_grp.add_argument(
        "--basecall-model-version",
        help="Choose a specific basecaller version",
    )
    mdl_grp.add_argument(
        "--modified-bases",
        nargs="+",
        help="Long name of the modified bases to call (e.g., 5mc, 5hmc).",
    )
    mdl_grp.add_argument(
        "--remora-model-type",
        help="""Choose the specific motif of the model you want to load.
        If None, load CG model.""",
    )
    mdl_grp.add_argument(
        "--remora-model-version",
        type=int,
        help="Choose the remora model version. If None, use latest.",
    )

    data_grp = subparser.add_argument_group("Data Arguments")
    data_grp.add_argument(
        "--num-reads",
        default=None,
        type=int,
        help="Number of reads.",
    )
    data_grp.add_argument(
        "--reference-anchored",
        action="store_true",
        help="""Infer per-read modified bases against reference bases instead
        of basecalls.""",
    )

    comp_grp = subparser.add_argument_group("Compute Arguments")
    comp_grp.add_argument(
        "--device",
        type=int,
        help="ID of GPU that is used for inference. Default: CPU only",
    )
    comp_grp.add_argument(
        "--queue-max",
        type=int,
        default=1_000,
        help="Maximum number of reads to store in each multiprocessing queue.",
    )
    comp_grp.add_argument(
        "--num-extract-alignment-workers",
        type=int,
        default=1,
        help="""Number of alignment extraction workers. See log for queue
        status and potentially increase num workers for process with inputs,
        but no outputs.""",
    )
    comp_grp.add_argument(
        "--num-prepare-read-workers",
        type=int,
        default=1,
        help="Number of read preparation workers.",
    )
    comp_grp.add_argument(
        "--num-prepare-nn-input-workers",
        type=int,
        default=1,
        help="Number of neural net input preparation workers.",
    )
    comp_grp.add_argument(
        "--num-post-process-workers",
        type=int,
        default=1,
        help="Number of post-processing workers.",
    )
    comp_grp.add_argument(
        "--batch-size",
        default=constants.DEFAULT_BATCH_SIZE,
        type=int,
        help="Number of input units per batch.",
    )

    subparser.set_defaults(func=run_infer_from_pod5_and_bam)


def register_infer_duplex_from_pod5_and_bam(parser):
    duplex_delim_flag = "--duplex-delim"
    subparser = parser.add_parser(
        "duplex_from_pod5_and_bam",
        description="Infer modified bases on duplex reads from pod5 and bam "
        "inputs",
        help="Run inference on pod5s simplex reads and duplex alignments with "
        "duplex pairs",
        formatter_class=SubcommandHelpFormatter,
    )
    subparser.add_argument(
        "pod5",
        help="POD5 (file or directory) matched to bam file.",
    )
    subparser.add_argument(
        "simplex_bam",
        help="Base called BAM file containing mv tags.",
    )
    subparser.add_argument(
        "duplex_bam",
        help=f"""BAM file containing duplex base called sequences (and optional
        reference mappings). Record names may either be the template read_id
        or template<delim>complement. The value of <delim> can be set with
        {duplex_delim_flag}.""",
    )
    subparser.add_argument(
        "duplex_read_pairs",
        help="""Whitespace separated plain text file containing read ID pairs,
        no header.""",
    )
    subparser.add_argument(
        duplex_delim_flag,
        default=";",
        help="""Deliminator string between template and complement read
        ids in the duplex BAM""",
    )

    out_grp = subparser.add_argument_group("Output Arguments")
    out_grp.add_argument(
        "--out-bam",
        help="Output BAM path.",
    )
    out_grp.add_argument(
        "--log-filename",
        help="Log filename. Default: Don't output log file.",
    )

    mdl_grp = subparser.add_argument_group("Model Arguments")
    mdl_grp.add_argument(
        "--model",
        action="append",
        help="Path(s) to a pretrained model in torchscript format.",
    )
    mdl_grp.add_argument(
        "--pore",
        help="""Choose the type of pore the Remora model has been trained on
        (e.g. dna_r10.4_e8.1)""",
    )
    mdl_grp.add_argument(
        "--basecall-model-type",
        help="Choose the basecaller model type (choose from fast, hac or sup)",
    )
    mdl_grp.add_argument(
        "--basecall-model-version",
        help="Choose a specific basecaller version",
    )
    mdl_grp.add_argument(
        "--modified-bases",
        nargs="+",
        help="Long name of the modified bases to call (e.g., 5mc, 5hmc).",
    )
    mdl_grp.add_argument(
        "--remora-model-type",
        help="Choose the specific motif of the model you want to load. "
        "If None, load CG model.",
    )
    mdl_grp.add_argument(
        "--remora-model-version",
        type=int,
        help="Choose the remora model version. If None, use latest.",
    )

    data_grp = subparser.add_argument_group("Data Arguments")
    data_grp.add_argument(
        "--num-reads",
        type=int,
        help="Number of reads.",
    )

    comp_grp = subparser.add_argument_group("Compute Arguments")
    comp_grp.add_argument(
        "--device",
        type=int,
        help="ID of GPU that is used for inference. Default: CPU only",
    )
    comp_grp.add_argument(
        "--num-extract-alignment-workers",
        type=int,
        default=1,
        help="Number of IO extraction workers.",
    )
    comp_grp.add_argument(
        "--num-duplex-prep-workers",
        type=int,
        default=1,
        help="Number of duplex prep workers (tends to bottleneck).",
    )
    comp_grp.add_argument(
        "--num-infer-workers",
        type=int,
        default=1,
        help="""Number of chunk extraction workers. If performing signal
        refinement this should be increased.""",
    )

    subparser.set_defaults(func=run_infer_from_pod5_and_bam_duplex)


def _unpack_models_kw_args(args) -> dict:
    from remora.util import parse_device

    device = parse_device(args.device)
    if args.model is None:
        return [
            {
                "pore": args.pore,
                "basecall_model_type": args.basecall_model_type,
                "basecall_model_version": args.basecall_model_version,
                "modified_bases": args.modified_bases,
                "remora_model_type": args.remora_model_type,
                "remora_model_version": args.remora_model_version,
                "device": device,
            },
        ]
    if any(not os.path.exists(mdl_path) for mdl_path in args.model):
        invalid_paths = [
            mdl_path for mdl_path in args.model if not os.path.exists(mdl_path)
        ]
        raise ValueError(f"Model path(s) do not exist {invalid_paths}")
    return [
        {
            "model_filename": mdl_path,
            "device": device,
        }
        for mdl_path in args.model
    ]


def check_models(models):
    if any(
        mdl[1]["reverse_signal"] != models[0][1]["reverse_signal"]
        for mdl in models[1:]
    ):
        raise RemoraError("All models must be the same signal direction")
    if any(
        mdl[1]["pa_scaling"] != models[0][1]["pa_scaling"] for mdl in models[1:]
    ):
        raise RemoraError("All models must use the same signal normalization")
    if len(models) != len(set(metadata["can_base"] for _, metadata in models)):
        raise RemoraError("Only one model per canonical base allowed.")


def run_infer_from_pod5_and_bam(args):
    import torch

    from remora.model_util import load_model
    from remora.inference import infer_from_pod5_and_bam

    if args.log_filename is not None:
        log.init_logger(args.log_filename)
    # test that model can be loaded in parent process
    models_kwargs = _unpack_models_kw_args(args)
    models = [
        load_model(**model_kwargs, quiet=False, eval_only=True)
        for model_kwargs in models_kwargs
    ]
    check_models(models)
    torch.set_grad_enabled(False)
    infer_from_pod5_and_bam(
        pod5_path=args.pod5,
        in_bam_path=args.in_bam,
        models=models,
        out_bam_path=args.out_bam,
        num_reads=args.num_reads,
        queue_max=args.queue_max,
        num_extract_alignment_workers=args.num_extract_alignment_workers,
        num_prep_read_workers=args.num_prepare_read_workers,
        num_prep_nn_input_workers=args.num_prepare_nn_input_workers,
        num_post_process_workers=args.num_post_process_workers,
        batch_size=args.batch_size,
        ref_anchored=args.reference_anchored,
        drop_move_tag=not args.preserve_move_tag,
    )
    LOGGER.info("Done")


def run_infer_from_pod5_and_bam_duplex(args):
    import torch

    from remora.model_util import load_model
    from remora.inference import infer_duplex

    if args.log_filename is not None:
        log.init_logger(args.log_filename)
    models_kwargs = _unpack_models_kw_args(args)
    models = [
        load_model(**model_kwargs, quiet=False, eval_only=True)
        for model_kwargs in models_kwargs
    ]
    if len(models) > 1:
        raise NotImplementedError(
            "Duplex infer does not currently implement running of "
            "multiple models"
        )
    # check_models(models)
    model, model_metadata = models[0]
    torch.set_grad_enabled(False)

    if not os.path.exists(args.pod5):
        raise ValueError(f"didn't find pod5 at {args.pod5}")
    if not os.path.exists(args.simplex_bam):
        raise ValueError(f"didn't find simplex bam at {args.simplex_bam}")
    if not os.path.exists(args.duplex_bam):
        raise ValueError(f"didn't find duplex bam at {args.duplex_bam}")
    if not os.path.exists(args.duplex_read_pairs):
        raise ValueError(
            f"didn't find duplex read pairs at {args.duplex_read_pairs}"
        )

    infer_duplex(
        simplex_pod5_path=args.pod5,
        simplex_bam_path=args.simplex_bam,
        duplex_bam_path=args.duplex_bam,
        pairs_path=args.duplex_read_pairs,
        model=model,
        model_metadata=model_metadata,
        out_bam=args.out_bam,
        num_extract_alignment_threads=args.num_extract_alignment_workers,
        num_duplex_prep_workers=args.num_duplex_prep_workers,
        num_infer_threads=args.num_infer_workers,
        num_reads=args.num_reads,
        duplex_deliminator=args.duplex_delim,
    )
    LOGGER.info("Done")


###################
# remora validate #
###################


def register_validate(parser):
    subparser = parser.add_parser(
        "validate",
        description="Validate modified base predictions",
        help="Validate modified base predictions",
        formatter_class=SubcommandHelpFormatter,
    )
    ssubparser = subparser.add_subparsers(title="validation commands")
    # Since `validate` has several sub-commands, print help as default
    subparser.set_defaults(func=lambda x: subparser.print_help())
    # Register validate sub commands
    register_validate_from_modbams(ssubparser)
    register_validate_from_remora_dataset(ssubparser)


def register_validate_from_modbams(parser):
    subparser = parser.add_parser(
        "from_modbams",
        description="Validation with ground truth samples",
        help="Validation with ground truth samples",
        formatter_class=SubcommandHelpFormatter,
    )
    subparser.add_argument(
        "--bam-and-bed",
        required=True,
        nargs=2,
        metavar=("BAM", "GROUND_TRUTH_BED"),
        action="append",
        help="""Argument accepts 2 values. The first value is the BAM file path
        with modified base tags. The second is a bed file with ground truth
        reference positions. The name field in the ground truth bed file should
        be the single letter code for a modified base or the corresponding
        canonical base. This argument can be provided more than once for
        multiple samples.""",
    )
    subparser.add_argument(
        "--full-results-filename", help="Output per-read calls to TSV file."
    )
    subparser.add_argument(
        "--name",
        default="sample",
        help="""Name of this sample/comparison. Useful when tabulating
        several runs.""",
    )
    subparser.add_argument(
        "--pct-filt",
        type=float,
        default=10.0,
        help="Filter a specified percentage (or less given ties) of calls.",
    )
    subparser.add_argument(
        "--allow-unbalanced",
        action="store_true",
        help="Allow classes to be unbalanced for metric computation.",
    )
    subparser.add_argument(
        "--max-sites-per-read",
        type=int,
        help="Maxiumum number of sites to extract from a single read.",
    )
    subparser.add_argument(
        "--seed",
        type=int,
        help="Seed value. Default: Random seed",
    )
    subparser.add_argument(
        "--extra-bases",
        help="""Extra canoncial or modified base single letter codes not in
        the ground truth bed files which should be added to the accepted
        alphabet. For example, consider a BED file with only canonical (C)
        sites. To extract 5mC (m) and 5hmC (h) calls from the modBAM the
        `--extra-bases mh` argument should be supplied""",
    )
    subparser.add_argument(
        "--log-filename",
        help="Log filename. (default: Don't output log file)",
    )
    subparser.add_argument(
        "--explicit-mod-tag-used",
        action="store_true",
        help="""Specify that the user has checked that the modified base tag
        (MM) uses the explicit (`?`) specifier. With the implicit (`.`) tag
        type  pysam will return invalid modified base probabilities and result
        may be invalid""",
    )

    subparser.set_defaults(func=run_validate_modbams)


def run_validate_modbams(args):
    from remora.validate import validate_modbams

    LOGGER.warning(
        """This command is deprecated and will be removed from a future version
        of Remora. Please use the `modkit validate` command."""
    )
    if args.explicit_mod_tag_used:
        LOGGER.warning(
            """
            If implict modified tag types are included (from all-context
            modified base models) results from this command will be invalid.
            Please see pysam issue here:
            https://github.com/pysam-developers/pysam/issues/1123"""
        )
    else:
        LOGGER.error(
            """
            If implict modified tag types are included (from all-context
            modified base models) results from this command will be inavlid.
            Please see pysam issue here:
            https://github.com/pysam-developers/pysam/issues/1123
            To force the usage of this command please specify the
            --explicit-mod-tag-used argument"""
        )
        sys.exit(1)

    if args.log_filename is not None:
        log.init_logger(args.log_filename)
    validate_modbams(
        bams_and_beds=args.bam_and_bed,
        full_results_path=args.full_results_filename,
        name=args.name,
        pct_filt=args.pct_filt,
        allow_unbalanced=args.allow_unbalanced,
        seed=args.seed,
        extra_bases=args.extra_bases,
        max_sites_per_read=args.max_sites_per_read,
    )
    LOGGER.info("Done")


def register_validate_from_remora_dataset(parser):
    subparser = parser.add_parser(
        "from_remora_dataset",
        description="Run validation on external Remora dataset",
        help="Validate on Remora dataset",
        formatter_class=SubcommandHelpFormatter,
    )
    subparser.add_argument(
        "remora_dataset_path",
        help="Remora training dataset",
    )

    mdl_grp = subparser.add_argument_group("Model Arguments")
    mdl_grp.add_argument(
        "--model",
        help="Path to a pretrained model.",
    )
    mdl_grp.add_argument(
        "--pore",
        help="Choose the type of pore the Remora model has been trained on "
        "(e.g. dna_r10.4_e8.1)",
    )
    mdl_grp.add_argument(
        "--basecall-model-type",
        help="Choose the basecaller model type (choose from fast, hac or sup)",
    )
    mdl_grp.add_argument(
        "--basecall-model-version",
        help="Choose a specific basecaller version",
    )
    mdl_grp.add_argument(
        "--modified-bases",
        nargs="+",
        help="Long name of the modified bases to call (e.g., 5mc, 5hmc).",
    )
    mdl_grp.add_argument(
        "--remora-model-type",
        help="Choose the specific motif of the model you want to load. "
        "If None, load CG model.",
    )
    mdl_grp.add_argument(
        "--remora-model-version",
        type=int,
        help="Choose the remora model version. If None, use latest.",
    )

    out_grp = subparser.add_argument_group("Output Arguments")
    out_grp.add_argument(
        "--out-file",
        help="Output path for the validation result file.",
    )
    out_grp.add_argument(
        "--full-results-filename", help="Output per-read calls to TSV file."
    )
    out_grp.add_argument(
        "--log-filename",
        help="Log filename. (default: Don't output log file)",
    )

    val_grp = subparser.add_argument_group("Validation Arguments")
    val_grp.add_argument(
        "--pct-filt",
        type=float,
        default=10.0,
        help="Filter a specified percentage (or less given ties) of calls.",
    )

    comp_grp = subparser.add_argument_group("Compute Arguments")
    comp_grp.add_argument(
        "--batch-size",
        default=constants.DEFAULT_BATCH_SIZE,
        type=int,
        help="Number of input units per batch.",
    )
    comp_grp.add_argument(
        "--device",
        type=int,
        help="ID of GPU that is used for inference. Default: CPU",
    )
    comp_grp.add_argument(
        "--read-batches-from-disk",
        action="store_true",
        help="""Read batches from disk during iteration. Default: loads batches
        before iteration""",
    )

    subparser.set_defaults(func=run_validate_from_remora_dataset)


def run_validate_from_remora_dataset(args):
    import torch

    from remora.util import parse_device
    from remora.model_util import load_model
    from remora.validate import ValidationLogger
    from remora.data_chunks import load_dataset

    if args.log_filename is not None:
        log.init_logger(args.log_filename)
    LOGGER.info("Loading model")
    model, model_metadata = load_model(
        args.model,
        pore=args.pore,
        basecall_model_type=args.basecall_model_type,
        basecall_model_version=args.basecall_model_version,
        modified_bases=args.modified_bases,
        remora_model_type=args.remora_model_type,
        remora_model_version=args.remora_model_version,
        device=parse_device(args.device),
        eval_only=True,
    )
    torch.set_grad_enabled(False)

    LOGGER.info("Loading Remora dataset")
    override_metadata = {}
    override_metadata["kmer_context_bases"] = model_metadata[
        "kmer_context_bases"
    ]
    override_metadata["chunk_context"] = model_metadata["chunk_context"]
    dataset = load_dataset(
        args.remora_dataset_path,
        core_ds_kwargs={
            "override_metadata": override_metadata,
            "infinite_iter": False,
            "do_check_super_batches": True,
        },
        ds_kwargs={
            "batch_size": args.batch_size,
            "return_arrays": ["signal", "modbase_label", "enc_kmer"],
        },
    )
    LOGGER.info(f"Loaded dataset summary:\n{dataset.summary}")
    if not args.read_batches_from_disk:
        dataset.load_all_batches()

    if args.out_file is None:
        out_fp = sys.stdout
    else:
        out_fp = open(args.out_file, "w", buffering=1)
        atexit.register(out_fp.close)
    if args.full_results_filename is None:
        full_results_fp = None
    else:
        full_results_fp = open(args.full_results_filename, "w", buffering=1)
        atexit.register(full_results_fp.close)

    LOGGER.info("Running validation")
    val_fp = ValidationLogger(out_fp, full_results_fp)
    val_fp.validate_model(
        model,
        model_metadata["mod_bases"],
        torch.nn.CrossEntropyLoss(),
        dataset,
        args.pct_filt / 100,
    )
    LOGGER.info("Done")


##################
# remora analyze #
##################


def register_analyze(parser):
    subparser = parser.add_parser(
        "analyze",
        description="Analyze nanopore data including raw signal",
        help="Analyze nanopore data including raw signal",
        formatter_class=SubcommandHelpFormatter,
    )
    ssubparser = subparser.add_subparsers(title="Analyze commands")
    # register_estimate_kmer_levels(ssubparser)
    # Since `plot` has several sub-commands, print help as default
    subparser.set_defaults(func=lambda x: subparser.print_help())
    # Register analyze sub commands
    register_analyze_plot(ssubparser)


def register_analyze_plot(parser):
    subparser = parser.add_parser(
        "plot",
        description="Plot nanopore data including raw signal",
        help="Plot nanopore data including raw signal",
        formatter_class=SubcommandHelpFormatter,
    )
    ssubparser = subparser.add_subparsers(title="Plot commands")
    # Since `plot` has several sub-commands, print help as default
    subparser.set_defaults(func=lambda x: subparser.print_help())
    # Register plot sub commands
    register_plot_ref_region(ssubparser)


def register_plot_ref_region(parser):
    subparser = parser.add_parser(
        "ref_region",
        description="Plot signal at reference region",
        help="Plot signal at reference region",
        formatter_class=SubcommandHelpFormatter,
    )

    in_grp = subparser.add_argument_group("Input Arguments")
    in_grp.add_argument(
        "--pod5-and-bam",
        required=True,
        nargs=2,
        metavar=("POD5", "BAM"),
        action="append",
        help="""POD5 and BAM paths. POD5 may be a file or directory. BAM file
        must be mapped, sorted and indexed and contain move table and MD tags.
        Multiple samples can be supplied and will be plotted in different
        colors""",
    )
    in_grp.add_argument(
        "--ref-regions",
        required=True,
        help="""Reference region(s) to plot specified in BED format. Each line
        in this input file will produce one page in the output PDF.""",
    )
    in_grp.add_argument(
        "--highlight-ranges",
        help="""BED file containing regions to highlight""",
    )
    in_grp.add_argument(
        "--highlight-color",
        default="orange",
        help="""Color or highlighted regions""",
    )

    refine_grp = subparser.add_argument_group("Signal Mapping Refine Arguments")
    refine_grp.add_argument(
        "--refine-kmer-level-table",
        help="""Tab-delimited file containing no header and two fields:
        1. string k-mer sequence and 2. float expected normalized level.
        All k-mers must be the same length and all combinations of the bases
        'ACGT' must be present in the file.""",
    )
    refine_grp.add_argument(
        "--refine-rough-rescale",
        action="store_true",
        help="""Apply a rough rescaling using quantiles of signal+move table
        and levels.""",
    )
    refine_grp.add_argument(
        "--refine-scale-iters",
        default=0,
        type=int,
        help="""Number of iterations of signal mapping refinement and signal
        re-scaling to perform. Set to 0 (default) in order to perform signal
        mapping refinement, but skip re-scaling. Set to -1 to skip signal
        mapping (potentially using levels for rough rescaling).""",
    )
    refine_grp.add_argument(
        "--refine-half-bandwidth",
        default=constants.DEFAULT_REFINE_HBW,
        type=int,
        help="""Half bandwidth around signal mapping over which to search for
        new path.""",
    )
    refine_grp.add_argument(
        "--refine-algo",
        default=constants.DEFAULT_REFINE_ALGO,
        choices=constants.REFINE_ALGOS,
        help="Refinement algorithm to apply (if kmer level table is provided).",
    )
    refine_grp.add_argument(
        "--refine-short-dwell-parameters",
        default=constants.DEFAULT_REFINE_SHORT_DWELL_PARAMS,
        type=float,
        nargs=3,
        metavar=("TARGET", "LIMIT", "WEIGHT"),
        help="""Short dwell penalty refiner parameters. Dwells shorter than
        LIMIT will be penalized a value of `WEIGHT * (dwell - TARGET)^2`.""",
    )

    out_grp = subparser.add_argument_group("Output Arguments")
    out_grp.add_argument(
        "--plots-filename",
        default="remora_raw_signal_plot.pdf",
        help="Output plots PDF file location.",
    )
    out_grp.add_argument(
        "--log-filename",
        help="Log filename. Default: Don't output log file.",
    )

    subparser.set_defaults(func=run_plot_ref_region)


def run_plot_ref_region(args):
    import pysam
    import plotnine as p9
    from pod5 import DatasetReader

    from remora import log, io, refine_signal_map

    p9.theme_set(p9.theme_minimal() + p9.theme(figure_size=(8, 3)))

    if args.log_filename is not None:
        log.init_logger(args.log_filename)
    pod5_paths, bc_paths = zip(*args.pod5_and_bam)
    bam_fhs = [pysam.AlignmentFile(bc_path) for bc_path in bc_paths]
    pod5_fhs = [DatasetReader(pod5_path) for pod5_path in pod5_paths]
    sig_map_refiner = refine_signal_map.SigMapRefiner(
        kmer_model_filename=args.refine_kmer_level_table,
        do_rough_rescale=args.refine_rough_rescale,
        scale_iters=args.refine_scale_iters,
        algo=args.refine_algo,
        half_bandwidth=args.refine_half_bandwidth,
        sd_params=args.refine_short_dwell_parameters,
        do_fix_guage=True,
    )
    highlight_ranges = None
    if args.highlight_ranges is not None:
        highlight_ranges = io.parse_bed(args.highlight_ranges)

    plots = []
    for ref_reg in io.parse_bed_lines(args.ref_regions):
        reg_highlight_ranges = None
        if highlight_ranges is not None:
            try:
                reg_highlight_ranges = [
                    (pos, pos + 1, args.highlight_color)
                    for pos in highlight_ranges[(ref_reg.ctg, ref_reg.strand)]
                    if ref_reg.start <= pos < ref_reg.end
                ]
            except KeyError:
                LOGGER.debug(f"No highlight values for region {ref_reg}")
                pass
        plots.append(
            io.plot_signal_at_ref_region(
                ref_reg,
                zip(pod5_fhs, bam_fhs),
                sig_map_refiner,
                highlight_ranges=reg_highlight_ranges,
            )
        )
    p9.save_as_pdf_pages(plots, args.plots_filename)
    LOGGER.info("Done")


def register_estimate_kmer_levels(parser):
    subparser = parser.add_parser(
        "estimate_kmer_levels",
        description="Estimate k-mer level table",
        help="Estimate k-mer level table",
        formatter_class=SubcommandHelpFormatter,
    )

    in_grp = subparser.add_argument_group("Input Arguments")
    in_grp.add_argument(
        "--pod5-and-bam",
        required=True,
        nargs=2,
        metavar=("POD5", "BAM"),
        action="append",
        help="""POD5 signal path and BAM file path. BAM file must be mapped,
        sorted and indexed and contain move table and MD tags. Multiple
        samples can be supplied and will be aggregated after site level
        extraction""",
    )

    refine_grp = subparser.add_argument_group("Signal Mapping Refine Arguments")
    refine_grp.add_argument(
        "--refine-kmer-level-table",
        help="""Tab-delimited file containing no header and two fields:
        1. string k-mer sequence and 2. float expected normalized level.
        All k-mers must be the same length and all combinations of the bases
        'ACGT' must be present in the file.""",
    )
    refine_grp.add_argument(
        "--refine-rough-rescale",
        action="store_true",
        help="""Apply a rough rescaling using quantiles of signal+move table
        and levels.""",
    )
    refine_grp.add_argument(
        "--refine-scale-iters",
        default=0,
        type=int,
        help="""Number of iterations of signal mapping refinement and signal
        re-scaling to perform. Set to 0 (default) in order to perform signal
        mapping refinement (aka resquiggle), but skip fine re-scaling. Set to
        -1 to skip signal mapping (potentially using levels for rough
        rescaling).""",
    )
    refine_grp.add_argument(
        "--refine-half-bandwidth",
        default=constants.DEFAULT_REFINE_HBW,
        type=int,
        help="""Half bandwidth around signal mapping over which to search for
        new path.""",
    )
    refine_grp.add_argument(
        "--refine-algo",
        default=constants.DEFAULT_REFINE_ALGO,
        choices=constants.REFINE_ALGOS,
        help="Refinement algorithm to apply (if kmer level table is provided).",
    )
    refine_grp.add_argument(
        "--refine-short-dwell-parameters",
        default=constants.DEFAULT_REFINE_SHORT_DWELL_PARAMS,
        type=float,
        nargs=3,
        metavar=("TARGET", "LIMIT", "WEIGHT"),
        help="""Short dwell penalty refiner parameters. Dwells shorter than
        LIMIT will be penalized a value of `WEIGHT * (dwell - TARGET)^2`.""",
    )

    data_grp = subparser.add_argument_group("Data Arguments")
    data_grp.add_argument(
        "--min-coverage",
        type=int,
        default=10,
        help="Miniumum coverage to include a site.",
    )
    data_grp.add_argument(
        "--kmer-context-bases",
        nargs=2,
        default=(2, 2),
        type=int,
        metavar=("BASES_BEFORE", "BASES_AFTER"),
        help="""Definition of k-mer by the number of bases before and after the
        assigned signal position""",
    )

    out_grp = subparser.add_argument_group("Output Arguments")
    out_grp.add_argument(
        "--levels-filename",
        default="remora_kmer_levels.txt",
        help="Output file for kmer levels.",
    )
    out_grp.add_argument(
        "--log-filename",
        help="Log filename. Default: Don't output log file.",
    )

    comp_grp = subparser.add_argument_group("Compute Arguments")
    comp_grp.add_argument(
        "--num-workers",
        type=int,
        default=1,
        help="Number of workers.",
    )
    comp_grp.add_argument(
        "--chunk-width",
        type=int,
        default=1_000,
        help="""Width of reference region to process at one time. Should be
        smaller for very high coverage.""",
    )
    comp_grp.add_argument(
        "--max-chunk-coverage",
        type=int,
        default=100,
        help="Maxiumum mean chunk coverage for each region.",
    )

    subparser.set_defaults(func=run_estimate_kmer_levels)


def run_estimate_kmer_levels(args):
    from itertools import product

    import pysam
    import numpy as np

    from remora import log, io, refine_signal_map

    if args.log_filename is not None:
        log.init_logger(args.log_filename)
    # open first to avoid long process without write access
    out_fh = open(args.levels_filename, "w")

    sig_map_refiner = refine_signal_map.SigMapRefiner(
        kmer_model_filename=args.refine_kmer_level_table,
        do_rough_rescale=args.refine_rough_rescale,
        scale_iters=args.refine_scale_iters,
        algo=args.refine_algo,
        half_bandwidth=args.refine_half_bandwidth,
        sd_params=args.refine_short_dwell_parameters,
        do_fix_guage=True,
    )
    if not sig_map_refiner.is_loaded or sig_map_refiner.scale_iters < 0:
        LOGGER.warning(
            "It is highly recommended to apply signal mapping refinement in "
            "order to output a valid kmer level table."
        )

    kmer_len = sum(args.kmer_context_bases) + 1
    all_kmer_levels = dict(
        ("".join(bs), []) for bs in product("ACGT", repeat=kmer_len)
    )
    for pod5_path, bam_path in args.pod5_and_bam:
        try:
            with pysam.AlignmentFile(bam_path) as bam_fh:
                _ = bam_fh.fetch(bam_fh.header.references[0], 0, 1)
        except ValueError:
            LOGGER.warning(
                "Cannot estimate levels from BAM file without mappings or index"
            )
            continue
        LOGGER.info(f"Extracting levels from {pod5_path} and {bam_path}")
        for kmer, levels in io.get_site_kmer_levels(
            pod5_path,
            bam_path,
            sig_map_refiner,
            args.kmer_context_bases,
            min_cov=args.min_coverage,
            chunk_len=args.chunk_width,
            max_chunk_cov=args.max_chunk_coverage,
            num_workers=args.num_workers,
        ).items():
            all_kmer_levels[kmer].append(levels)
    LOGGER.info("Aggregating and outputting levels")
    been_warned = False
    for kmer, levels in sorted(all_kmer_levels.items()):
        levels = np.concatenate(levels)
        if levels.size == 0:
            if not been_warned:
                LOGGER.warning("Some k-mers not observed.")
                been_warned = True
            out_fh.write(f"{kmer}\tnan\n")
        else:
            out_fh.write(f"{kmer}\t{np.median(levels)}\n")
    out_fh.close()
    LOGGER.info("Done")
