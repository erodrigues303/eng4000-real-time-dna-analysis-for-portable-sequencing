<p class="eyebrow">Benchmarking study · Preliminary</p>

# How close is the TX2 CPU baseline to real-time capacity?

The tested ARM64 DeepNano-Blitz CPU port reaches **214,574 samples/s** at eight caller threads, or **10.48%** of the D4-matched theoretical full-channel target. This establishes a reported CPU reference point; it is neither a SoCall result nor a GPU benchmark. [BLITZ-009 evidence](../evidence/index.md#tx2).

## Experimental design

[BLITZ-009](../experiments/BLITZ-009.md) uses [D4](../datasets/D4.md), network 64, beam 5, and 1/2/4/8 caller threads on [Jetson TX2](../systems/jetson-tx2.md). Each setting has one excluded warm-up and three complete-command timing runs. The installed CUDA stack was unused. B2 pp.4,13 describes monotonic timing and both OpenMP and OpenBLAS thread controls.

## Results and interpretation

[Timing, throughput and provisional power table](../evidence/index.md#tx2).

Four threads report **207,860 samples/s**, close to eight-thread throughput. Stage-level profiling is needed to explain the limited additional scaling. The capacity denominator is **512 × 4,000 = 2,048,000 samples/s**, based on inspected D4 acquisition metadata and continuously active channels. It is not measured instrument yield.

## Limitations

The workload has only 48 historical FAST5 reads. All measured outputs reportedly match; biological accuracy and equivalence to the unmodified x86 build are unverified. Module-input sensor scaling remains uncertain, so watts and joules are provisional and cannot be ranked against Ryzen CPU-package power. Memory, thermal state and power mode are incomplete.

## Next investigation

Recover the ARM64 patches and original evidence, verify the sensor scale, and collect sustained throughput, queue length and latency on timestamped arrivals. Establish SoCall correctness and its own baseline separately before evaluating CUDA or other optimizations.

## Supporting experiment and reproduction

[BLITZ-009](../experiments/BLITZ-009.md) · [Jetson compatibility notes](../docs/platforms/jetson-tx2.md) · [SoCall engineering](../socall/index.md) · [Reproduction guide](../resources/reproduce.md).
