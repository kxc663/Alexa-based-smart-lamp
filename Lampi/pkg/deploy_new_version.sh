#!/bin/bash
set -e

# copy common code
cp -a ../lamp_common.py lampi/opt/lampi

# copy latest version of lamp_service.py
cp -a ../lamp_service.py lampi/opt/lampi

# copy the Kivy touchscreen code
cp -a ../main.py lampi/opt/lampi/lamp_ui.py
mkdir -p lampi/opt/lampi/lampi
cp -a ../lampi/*.py lampi/opt/lampi/lampi
cp -a ../lampi/*.kv lampi/opt/lampi/lampi
mkdir -p lampi/opt/lampi/images
cp -a ../images/*.png lampi/opt/lampi/images
mkdir -p lampi/opt/lampi/lampi/controls
cp -a ../lampi/controls/*.py lampi/opt/lampi/lampi/controls
cp -a ../lampi/controls/*.kv lampi/opt/lampi/lampi/controls

# copy the Bluetooth code
mkdir -p lampi/opt/lampi/bluetooth
cp -a ../bluetooth/*.js lampi/opt/lampi/bluetooth
mv lampi/opt/lampi/bluetooth/peripheral.js lampi/opt/lampi/bluetooth/bt_peripheral.js

# increment version number
bumpversion minor --allow-dirty

# make a temp directory
tmpdir=`mktemp -d`

cp -a lampi "$tmpdir"

# force package files to be owned by root
sudo chown -R root:root "$tmpdir/lampi"

# build Debian Package
dpkg-deb --build "$tmpdir/lampi"

# deploy package to repository
##  direct reprepro to use the GNUPG files and conf in the ubuntu user directory
reprepro --gnupghome /home/ubuntu/.gnupg -b /home/ubuntu/connected-devices/Web/reprepro/ubuntu/ includedeb eecs397 "$tmpdir/lampi.deb"

# clean up our temporary directory
sudo rm -rf "$tmpdir"
