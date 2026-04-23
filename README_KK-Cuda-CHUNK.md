<!--
  KeyKiller-Cuda-CHUNK
  https://github.com/egorrushka/KeyKiller-Cuda-CHUNK
  Copyright (C) 2025  egorrushka
  Licensed under GNU AGPL v3 — see LICENSE.txt
  Original code: https://github.com/Qalander/KeyKiller-Cuda
-->

# main.cpp — KeyKiller with Chunk Support

**Based on:** [KeyKiller-Cuda](https://github.com/Qalander/KeyKiller-Cuda)  
**Original authors:** Jean-Luc Pons / VanitySearch, FixedPaul, 8891689  
**Tested on:** NVIDIA RTX A4000 (48×128 cores, SM86), Windows 10 x64

---

## What was changed

This is a **drop-in replacement** for the original `main.cpp`.  

### Added: `-s` / `-e` flags (chunk mode)

The original program only supported `-r <bits>` which always searches  
the **entire** bit range (e.g. `-r 71` = full 2^70 → 2^71-1).

The new flags allow searching any **arbitrary sub-range (chunk)**:

| Flag | Description |
|------|-------------|
| `-s <hex>` | Chunk start address (hex, with or without `0x` prefix) |
| `-e <hex>` | Chunk end address (hex, with or without `0x` prefix) |

`-s` and `-e` must always be used together.  
The `-r` flag (original bit-range mode) is fully preserved and still works.

### Added: `parseHex()` function

Internal helper that parses 256-bit hex values (with or without `0x` prefix)  
into the `Int` type used by the engine.

---

## Usage

```bat
:: Original mode — full puzzle range
kk.exe -a 1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU -r 71

:: Chunk mode — specific sub-range
kk.exe -a 1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU -s 0x400000000000000000 -e 0x43ffffffffffffff

:: Chunk mode — without 0x prefix
kk.exe -a 1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU -s 400000000000000000 -e 43ffffffffffffff

:: All original flags still work
kk.exe -a <addr> -r 71 -R          (random mode)
kk.exe -a <addr> -r 71 -b          (backup / resume)
kk.exe -a <addr> -r 71 -G 1        (GPU device ID)
kk.exe -p <pubkey> -s <hex> -e <hex>
```

---

## Compile (Windows, CUDA 12, VS Build Tools)

Open **x64 Native Tools Command Prompt** and run:

```bat
nvcc main.cpp Vanity.cpp SECP256K1.cpp Int.cpp IntMod.cpp IntGroup.cpp ^
     Point.cpp Timer.cpp Random.cpp Base58.cpp Bech32.cpp Wildcard.cpp ^
     GPU\GPUEngine.cu GPU\GPUGenerate.cpp ^
     hash\ripemd160.cpp hash\ripemd160_sse.cpp ^
     hash\sha256.cpp hash\sha256_sse.cpp hash\sha512.cpp ^
     -o kk.exe ^
     -O3 --use_fast_math ^
     -gencode=arch=compute_86,code=sm_86 ^
     -m64 -Xcompiler "/W0" -DWIN64 ^
     -Xlinker advapi32.lib
```

> Change the `-gencode` architecture for your GPU:  
> RTX A4000 / RTX 3090 / RTX 3080 → `compute_86,code=sm_86`  
> RTX 4090 / RTX 4080 → `compute_89,code=sm_89`  
> RTX 2080 Ti → `compute_75,code=sm_75`  
> GTX 1080 Ti → `compute_61,code=sm_61`

---

## Benchmark results on RTX A4000

| Mode | Speed |
|------|-------|
| Address mode (P2PKH Compressed) | ~1560 Mkey/s |
| Public key mode (-p) | ~2× faster (no hashing required) |

---

## Full flags reference

```
kk.exe [-a <addr> | -p <pubkey>]  [keyspace]  [options]

Target:
  -a <b58_addr>    Search for P2PKH Bitcoin address (compressed)
  -p <pubkey>      Search for compressed public key (hex)

Keyspace (choose one):
  -r <bits>        Full bit-range: 2^(bits-1) to 2^bits-1
  -s <hex>         Chunk start  (must be used with -e)
  -e <hex>         Chunk end    (must be used with -s)

Options:
  -R               Random mode
  -b               Backup / resume mode (saves progress to schedule_gpu0.dat)
  -G <id>          GPU device ID (default: 0)
  -h, --help       Show this help

Key 'p' = pause / resume     Ctrl+C = graceful stop
```

---

## Notes

- Only **Compressed P2PKH** addresses are supported (puzzles #51 and above)
- Puzzles #1–#50 use Uncompressed keys — kk.exe will not find them
- Found keys are saved to `found.txt` automatically
- Backup file: `schedule_gpu0.dat` (created when `-b` flag is active)
