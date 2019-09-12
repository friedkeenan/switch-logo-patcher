# Switch Logo Patcher

### How to use

First you need to make a base IPS patch of the raw bytes of the original logo and the raw bytes of the logo you want to use ([flips](https://github.com/Alcaro/Flips) is good for that), and then run `./gen_patches.py <patch file> <patches dir>`.

More detaied command usage:

```
usage: gen_patches.py [-h] patch_file patches_dir

positional arguments:
  patch_file   The base logo patch
  patches_dir  The directory where the generated patches will be dumped

optional arguments:
  -h, --help   show this help message and exit
```