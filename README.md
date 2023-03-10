# **volatility-tools**

### **PROFILE & SYMBOL VOLATILITY TOOLS**

**DISCLAIMER:**

The `linux` folder is belongs to [`Volatility Foundation's github repository`](https://github.com/volatilityfoundation/volatility/tree/master/tools/linux).

The `dwarf2json` binary file was built from [`Volatility Foundation's github repository`](https://github.com/volatilityfoundation/dwarf2json).

I DO NOT OWN THOSE TWO.

**Requirements:**

Please make sure you have installed the followings in your lab.

+ `make`
+ `go` (version 1.11 or later)

If not, please do the following steps:

```sh
sudo apt install make -y
sudo apt install gccgo-go -y
```

**How to build:**

+ First, clone this repo to your local lab and change dir to `build-volatility`:

```sh
git clone https://github.com/1259iknowthat/volatility-tools.git && cd volatility-tools/build-volatility/
```

+ Second, run the `build.py` file:

```sh
$ python3 build.py -h
usage: build.py [-h] -vol <version> -ver <version>

options:
  -h, --help            show this help message and exit
  -vol <version>, --volatility <version>
                        Version of Volatility
  -ver <version>, --version <version>
                        Version of linux headers/image package
```

+ Last, copy the file you need in output folder to one of the followings:

    + `volatility/plugins/overlays/linux/` if it was volatility 2 profile 
    + `/volatility3/framework/symbols/linux/` if it was volatility 3 symbol

**Caution:**

This tool is just for Ubuntu distro right now.

As far as I know, volatility 2 does not support new Ubuntu kernel anymore. Please use volatility 2 profile function for Ubuntu 18.04 or older.

If you still want to build for new kernel, USE AT YOUR OWN RISK!!!

### **COMMUNITY-PLUGINS**
**DISCLAIMER:** 

*I DO NOT OWN THOSE PLUGINS IN COMMUNITY-PLUGINS FOLDER*

*Those are collected from these links below**

Refs:

```
https://github.com/volatilityfoundation/community/blob/master/FrancescoPicasso/mimikatz.py
https://github.com/superponible/volatility-plugins
```