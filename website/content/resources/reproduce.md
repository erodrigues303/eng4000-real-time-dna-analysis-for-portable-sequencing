# Reproduce the experiments

The records distinguish a command transcribed from a report from an independently reproducible experiment. No benchmark was rerun to build this website.

## Available historical commands

The supplied weekly log adds commands for [DORADO-001](../experiments/DORADO-001.md), [DORADO-002](../experiments/DORADO-002.md), [DORADO-003](../experiments/DORADO-003.md), [DORADO-004](../experiments/DORADO-004.md), [DORADO-005](../experiments/DORADO-005.md) and [BLITZ-003](../experiments/BLITZ-003.md). Commands appear verbatim in their records. Paths refer to the original machines; the commands have not been tested here.

Dorado records cover Windows CUDA, Windows CPU and macOS Metal. BLITZ-003 records cover caller-thread settings on Ubuntu/WSL. Recover the matching environment, exact input and weights before attempting a faithful rerun. Preserve outputs in a new run directory to avoid replacing earlier evidence.

## Recover a benchmark

1. Select the [experiment](../experiments/index.md) and read its timing scope and limitations.
2. Recover original executable/build, environment, model and dataset files; record hashes and applicable licences.
3. Resolve paths, shell and runtime requirements. A report command alone does not recover these.
4. Apply the [measurement protocol](../docs/methodology.md), recording warm-up, cache policy, repetitions, failures and all measurement boundaries.
5. Archive raw logs, outputs, checksums and validation results following the [results convention](../results/README.md).
6. Obtain independent reproduction before upgrading the scientific claim.

## BLITZ-005 evidence path

The [DeepNano-Blitz CPU Scaling and Energy Efficiency investigation](../benchmarking/cpu-parallelism.md) links to [BLITZ-005](../experiments/BLITZ-005.md), its [configuration](../configs/experiments/BLITZ-005.yaml), the dataset/model/system cards, and [transcribed per-run timings](../evidence/index.md#blitz005). Its exact invocation and raw artifacts are still missing.

## Other tools and private materials

Bonito and DeepNano-Coral were reviewed, not benchmarked. Slorado build and conversion commands are incomplete. Jetson's ARM64 Blitz port patches and original environment must be recovered. SoCall source/weights require confirmed access and publication permissions; only descriptive metadata is included.

## Validate the research records

From the repository root, with Python 3.10 or newer:

```sh
python -m pip install -r requirements-dev.txt
python harness/analysis/validate_metadata.py
python harness/analysis/render_summaries.py --check
```

These validate structure and rendering, not scientific correctness, and do not execute basecallers. See the repository's `website/README.md` for website build and preview commands.
