#

...

##

...

##

...

```shell
#
$ sudo apt install -y cmake libusb-1.0-0-dev make gcc g++ libbluetooth-dev wget pkg-config python3-numpy python3-distutils python3-setuptools

# 
$ sudo apt install -y python3-qtpy
```

## Install libbtbb

...

```shell
wget https://github.com/greatscottgadgets/libbtbb/archive/2020-12-R1.tar.gz -O libbtbb-2020-12-R1.tar.gz
tar -xf libbtbb-2020-12-R1.tar.gz
cd libbtbb-2020-12-R1
mkdir build && cd build
cmake ..
make
sudo make install
sudo ldconfig
```

## Install Ubertooth tools

...

```shell
```


