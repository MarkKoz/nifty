# Nifty

Command-line tools for NIF (NetImmerse file format) files, used by games to store meshes. You can write scripts that invoke these tools to perform batch operations on many NIF files instead of manually toiling away in NifSkope.

Currently, it has utilities for setting and listing body parts.

## Installation

```sh
pip install 'git+https://github.com/MarkKoz/nifty.git'
```

## Usage

See `nifty --help`.

## Examples

### List body parts

```
❯ nifty body-part list ./tests/resources/cuirass_1.nif
[20:30:10] INFO     Reading file: tests/resources/cuirass_1.nif
[20:30:13] INFO     b'Armor' partition 1: 32
           INFO     b'Armor' partition 2: 32
           INFO     b'FemaleUnderwear' partition 1: 32
           INFO     b'VariantTorso' partition 1: 38
           INFO     b'VariantTorso' partition 2: 32
           INFO     b'VariantTorso' partition 3: 32
           INFO     b'Cuirass_1:1' partition 1: 32
           INFO     b'Cuirass_1:0' partition 1: 38
           INFO     b'Cuirass_1:0' partition 2: 32
           INFO     b'ForswornArmorF' partition 1: 32
           INFO     b'ForswornArmorF' partition 2: 32
           INFO     b'ForswornArmorF' partition 3: 32
           INFO     b'FemaleUnderwearBody:0' partition 1: 34
           INFO     b'FemaleUnderwearBody:0' partition 2: 32
           INFO     b'FemaleUnderwearBody:0' partition 3: 38
           INFO     b'FemaleUnderwearBody:0' partition 4: 32
```

### Replace body part by ID

Dry-run to replace body part ID 32 with 61, and then write the modified file to `out.nif`.

```
❯ nifty body-part set ./tests/resources/cuirass_1.nif 61 --replacing 32 --dest out.nif
[20:28:15] INFO     Reading file: tests/resources/cuirass_1.nif
[20:28:18] INFO     Set b'Armor' partition 1 body part: 32 -> 61
           INFO     Set b'Armor' partition 2 body part: 32 -> 61
           INFO     Set b'FemaleUnderwear' partition 1 body part: 32 -> 61
           INFO     Set b'VariantTorso' partition 2 body part: 32 -> 61
           INFO     Set b'VariantTorso' partition 3 body part: 32 -> 61
           INFO     Set b'Cuirass_1:1' partition 1 body part: 32 -> 61
           INFO     Set b'Cuirass_1:0' partition 2 body part: 32 -> 61
           INFO     Set b'ForswornArmorF' partition 1 body part: 32 -> 61
           INFO     Set b'ForswornArmorF' partition 2 body part: 32 -> 61
           INFO     Set b'ForswornArmorF' partition 3 body part: 32 -> 61
           INFO     Set b'FemaleUnderwearBody:0' partition 2 body part: 32 -> 61
           INFO     Set b'FemaleUnderwearBody:0' partition 4 body part: 32 -> 61
```

### Replace body part by name

Dry-run to replace body parts in geometry whose name matches the regular expression `Cuirass_1:\d`, and then write the modified file to `out.nif`.

```
❯ nifty body-part set ./tests/resources/cuirass_1.nif 61 --name 'Cuirass_1:\d' --dest out.nif
[20:42:56] INFO     Reading file: tests/resources/cuirass_1.nif
[20:43:00] INFO     Set b'Cuirass_1:1' partition 1 body part: 32 -> 61
           INFO     Set b'Cuirass_1:0' partition 1 body part: 38 -> 61
           INFO     Set b'Cuirass_1:0' partition 2 body part: 32 -> 61
```

### Bulk replace body part

Shell script to bulk set body parts using [fd] and [rust-parallel].

```sh
#!/usr/bin/env bash
set -euo pipefail

fd -t file --glob "*.nif" \
| rust-parallel -r '(.+)' nifty body-part set {1} 40 "$@"
```

### Delete files without body parts

Shell script to delete files without any body parts.

```sh
#!/usr/bin/env bash
set -euo pipefail

command = 'nifty body-part list "{1}" --error || rm -- "{1}" && rmdir -p --ignore-fail-on-non-empty "$(dirname -- "{1}")"'

fd -t file --glob "*.nif" \
| rust-parallel \
  -r '(.+)' \
  --shell-path bash \
  --shell-argument=-c --shell "$command"
```

[fd]: https://github.com/sharkdp/fd
[rust-parallel]: https://github.com/aaronriekenberg/rust-parallel
