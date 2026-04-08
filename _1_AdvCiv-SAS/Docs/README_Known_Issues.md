# Known issues (NIF Gallery)

Known issues for AdvCiv-SAS-NIF-Gallery. This file is intentionally short and can be expanded over time.

## Menu

[1 - (Documented - not fixed) Sevopedia leader crash around Nanye-hi (Tomyris)](/_1_AdvCiv-SAS/Docs/README_Known_Issues.md#1---documented---not-fixed-sevopedia-leader-crash-around-nanye-hi-tomyris)  

## 1 - (Documented - not fixed) Sevopedia leader crash around Nanye-hi (Tomyris)

Screenshots/files for this issue: [google drive folder link](https://drive.google.com/drive/folders/1ETNsvHCloYNjmm5I7QJsUelu2J5fir-p?usp=sharing).

Observed behavior:

- In Sevopedia Leaders, moving with keyboard `Up`/`Down` around `Nanye-hi (Tomyris)` can immediately or after a few dozen tries crash the game.
- It can happen quickly or after a few moves, and has been reproduced with both arrow directions.

Crash signature (from dump analysis):

- Exception: `0xc0000005` (`INVALID_POINTER_READ`)
- Module: `Civ4BeyondSword.exe` (`3.1.9.0`)
- Fault region seen at offsets around `0x51958a` and `0x519604`
- Same failure hash observed: `{0a0d0af2-ae71-5e41-a8a8-35f50ff2467b}`
