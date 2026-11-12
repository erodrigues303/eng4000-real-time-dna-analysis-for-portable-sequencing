# Jetson TX2

Source: P pp.13,15–16; U; see [register](../sources.md).

## Recorded setup

Ubuntu 16.04.5; Jetson Linux R28.2.1; 8 GB shared memory; ARM64. BLITZ-009 used the CPU only with an owned math-library port. INA3221 VDD_IN sampled about every 0.5 s.

## Reproduction gaps and constraints

Do not assume current Dorado supports this TX2. Older compatible software, Blitz, SoCall or owned CUDA work require specific build verification. JetPack/CUDA/driver, power mode, CPU affinity, thermal state, port library and commands are TBD. Idle readings 0.979 W (20 s) and separate initial 1.415 W require sensor scaling/calibration checks. RAM usage and CPU utilization were not captured.

No install commands were present in the supplied reports. Recover original notes before turning this page into an executable recipe.
