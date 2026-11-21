# Jetson TX2

Source: P pp.13,15–16; U; see [register](../sources.md).

## Recorded setup

Ubuntu 16.04.5; Jetson Linux R28.2.1; 8 GB shared memory; ARM64. BLITZ-009 used the CPU only with an owned math-library port. INA3221 VDD_IN sampled about every 0.5 s.

## Reproduction gaps and constraints

Do not assume current Dorado supports this TX2. Older compatible software, Blitz, SoCall or owned CUDA work require specific build verification. JetPack/CUDA/driver, power mode, CPU affinity, thermal state, port library and commands are TBD. Idle readings 0.979 W (20 s) and separate initial 1.415 W require sensor scaling/calibration checks. RAM usage and CPU utilization were not captured.

No install commands were present in the supplied reports. Recover original notes before turning this page into an executable recipe.

## JetPack 4.6.6 reflash (2026-11-20, system `jetson-tx2-jp466`)

Source: M. The board was wiped and reflashed; the setup above describes the historical R28.2.1 image used for BLITZ-009 and no longer exists on the device.

- **Image:** JetPack 4.6.6 / L4T R32.7.6, the last JetPack release supporting TX2. Ubuntu 18.04, Python 3.6, CUDA 10.2, cuDNN 8.2.1, TensorRT 8.2.1. PyTorch 1.10.0 from NVIDIA's JetPack 4.6 wheel (final release for Python 3.6); `torch.cuda.is_available()` true.
- **Host:** Windows + WSL2 with an imported Ubuntu 18.04 (`aka.ms/wsl-ubuntu-1804`; 18.04 is no longer in the WSL online list), SDK Manager 26.1.0, usbipd-win for USB passthrough.
- **Known WSL failure modes and fixes:**
  1. SDK Manager's image build hung on an interactive apt prompt it cannot display (`libssl1.1` restart-services). Pre-answer with `debconf-set-selections` and run `apt-get upgrade` non-interactively first.
  2. After the TX2 re-enumerates mid-flash, usbipd marks it "Not shared". Fix: `usbipd policy add --effect Allow --operation AutoBind --hardware-id 0955:7c18`.
  3. SDK Manager probes the board ~2 s after its recovery reboot; WSL re-attach takes 8–25 s, so it fails with "probing the target board failed". Fix: flash directly from `Linux_for_Tegra`: `sudo ./tools/l4t_create_default_user.sh -u <user> -p <password> -n <hostname> --accept-license`, then `sudo ./flash.sh jetson-tx2-devkit mmcblk0p1`.
  4. A failed attempt can leave the module half-initialised ("target is in a bad state"): unplug power, then re-enter recovery from off.
- **Post-flash:** `sudo apt install nvidia-jetpack`; `sudo nvpmodel -m 0`; `sudo jetson_clocks` before every measurement session.
- **Measurement settings:** power via `tegrastats --interval 1000 --logfile`; VDD_IN is module input (INA3221), not wall power. R32 tegrastats lines carry no timestamps.
