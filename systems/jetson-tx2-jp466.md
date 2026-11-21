# jetson-tx2-jp466

Generated from `jetson-tx2-jp466.json`; edit the JSON and rerun the renderer.

| Field | Recorded value |
|---|---|
| system id | jetson-tx2-jp466 |
| name | NVIDIA Jetson TX2 developer kit, reflashed with JetPack 4.6.6 (2026-11-20) |
| cpu | 6 ARM64 cores (tegrastats reports six CPU clusters at ~2.03 GHz in MAXN); exact Denver/A57 split per NVIDIA docs, not probed |
| gpu | Integrated NVIDIA Tegra X2 GPU (torch.cuda.get_device_name), GR3D clock 1300 MHz under jetson_clocks |
| ram | 8 GB shared CPU/GPU (7858 MB reported by tegrastats), 3.9 GB zram swap |
| os | Ubuntu 18.04 (L4T R32.7.6, aarch64) |
| architecture | ARM64; module P3310-1000 (B02, rev E.0) on carrier P2597-0000 (rev D.0), board config jetson-tx2-devkit |
| cuda | 10.2.300 |
| driver | L4T R32.7.6 BSP (GCID 38171779) |
| jetpack | 4.6.6 (nvidia-jetpack 4.6.6-b24); cuDNN 8.2.1.32; TensorRT 8.2.1.9 |
| power mode | MAXN (nvpmodel -m 0) with jetson_clocks; fan mode unset (jetson_clocks drives fan) |
| provenance | ["M"] |
| limitations | ["Same physical board as the historical jetson-tx2 record (BLITZ-009) but a different OS/BSP; results are not interchangeable with BLITZ-009.", "INA3221 VDD_IN scaling not independently calibrated against a wall meter.", "Idle VDD_IN about 3.29 W in MAXN with jetson_clocks (tegrastats, 23 s, 2026-11-20); not comparable to the historical 0.979 W idle reading taken under R28.2.1 and an unknown power mode."] |

Source IDs refer to the [evidence register](../docs/sources.md). Unknown fields are not inferred from product names or chemistry.
