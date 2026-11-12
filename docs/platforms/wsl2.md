# Windows / Ubuntu / WSL

Source: B pp.4,7–8,11–15; see [register](../sources.md).

## Recorded setup

5700U used Ubuntu 22.04 / WSL2; 7800X3D used Windows 11 with Ubuntu/WSL (exact WSL version TBD). Blitz deepnano2 0.1 follow-up build: commit 15bd04b94c291debac75823811a2c86820dda589, Python 3.9.23, Rust nightly-2021-01-03, conda-forge mkl-static/mkl-include 2026.1.0, NumPy 2.0.2, h5py 3.14.0, ont-fast5-api 4.1.3. Legacy MKL URL failed HTTP 403; Conda libraries used.

## Reproduction gaps and constraints

These are reported dependency versions, not a tested installation recipe. Recover exports and exact build commands. Record WSL/kernel/filesystem placement and thread affinity. GNU Time covers guest command time/RSS; HWiNFO host timestamps require America/Toronto to UTC alignment. Do not attribute host package power solely to the guest process.

No install commands were present in the supplied reports. Recover original notes before turning this page into an executable recipe.
