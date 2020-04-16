#!/usr/bin/env python3

import os
import copy
import io
import argparse
import ips
from pathlib import Path
from PIL import Image

# Build Id: offset
patch_info = {
    # AM patches
    "C79F22F18169FCD3B3698A881394F6240385CDB1": 1668164,
    "01890C643E9D6E17B2CDA77A9749ECB9A4F676D6": 1962240,
    "C088ADC91417EBAE6ADBDF3E47946858CAFE1A82": 1962240,
    "3EC573CB22744A993DFE281701E9CBFE66C03ABD": 1716480,

    # Vi patches
    "7B4123290DE2A6F52DE4AB72BEA1A83D11214C71": 1831168,
    "723DF02F6955D903DF7134105A16D48F06012DB1": 1835264,
    "967F4C3DFC7B165E4F7981373EC1798ACA234A45": 1573120,
    "98446A07BC664573F1578F3745C928D05AB73349": 1589504,
    "0767302E1881700608344A3859BC57013150A375": 1593600,
    "7C5894688EDA24907BC9CE7013630F365B366E4A": 1593600,
    "7421EC6021AC73DD60A635BC2B3AD6FCAE2A6481": 1536256,
    "96529C3226BEE906EE651754C33FE3E24ECAE832": 1544448,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("old_logo", help="The original logo image", type=Image.open)
    parser.add_argument("new_logo", help="The new logo image", type=Image.open)
    parser.add_argument("patches_dir", help="The directory where the generated patches will be dumped", type=Path)
    args = parser.parse_args()

    args.old_logo.convert("RGBA")
    args.new_logo.convert("RGBA")

    base_patch = ips.Patch.create(args.old_logo.tobytes(), args.new_logo.tobytes())

    if not args.patches_dir.exists():
        os.makedirs(args.patches_dir)

    for build_id, offset in patch_info.items():
        tmp_p = copy.deepcopy(base_patch)

        for r in tmp_p.records:
            r.offset += offset

            if r.offset > 0xFFFFFF:
                tmp_p.ips32 = True

        with Path(args.patches_dir, f"{build_id}.ips").open("wb") as f:
            f.write(bytes(tmp_p))