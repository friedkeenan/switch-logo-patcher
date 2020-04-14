#!/usr/bin/env python3

import os
import copy
import argparse
import ips
from pathlib import Path

# Build Id: offset
patch_info = {
    # AM patches
    "C79F22F18169FCD3B3698A881394F6240385CDB1000000000000000000000000": 1668164,
    "01890C643E9D6E17B2CDA77A9749ECB9A4F676D6000000000000000000000000": 1962240,
    "C088ADC91417EBAE6ADBDF3E47946858CAFE1A82000000000000000000000000": 1962240,
    "3EC573CB22744A993DFE281701E9CBFE66C03ABD000000000000000000000000": 1716480,

    # Vi patches
    "7B4123290DE2A6F52DE4AB72BEA1A83D11214C71000000000000000000000000": 1831168,
    "723DF02F6955D903DF7134105A16D48F06012DB1000000000000000000000000": 1835264,
    "967F4C3DFC7B165E4F7981373EC1798ACA234A45000000000000000000000000": 1573120,
    "98446A07BC664573F1578F3745C928D05AB73349000000000000000000000000": 1589504,
    "0767302E1881700608344A3859BC57013150A375000000000000000000000000": 1593600,
    "7C5894688EDA24907BC9CE7013630F365B366E4A000000000000000000000000": 1593600,
    "7421EC6021AC73DD60A635BC2B3AD6FCAE2A6481000000000000000000000000": 1536256,
    "96529C3226BEE906EE651754C33FE3E24ECAE832000000000000000000000000": 1544448,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("patch_file", help="The base logo patch", type=Path)
    parser.add_argument("patches_dir", help="The directory where the generated patches will be dumped", type=Path)
    args = parser.parse_args()

    with args.patch_file.open("rb") as f:
        p = ips.Patch.from_buffer(f.read())

    if not args.patches_dir.exists():
        os.makedirs(args.patches_dir)

    for build_id, offset in patch_info.items():
        tmp_p = copy.deepcopy(p)

        for r in tmp_p.records:
            r.offset += offset

        with Path(args.patches_dir, f"{build_id}.ips").open("wb") as f:
            f.write(bytes(tmp_p))