#!/bin/bash

apt-get update
apt-get install -y xfonts-75dpi
apt-get install -y xfonts-base
apt-get install -y libjpeg62-turbo

wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltox_0.12.6-1.focal_amd64.deb
dpkg -i wkhtmltox_0.12.6-1.focal_amd64.deb
cp /usr/local/bin/wkhtmltopdf /usr/bin/wkhtmltopdf
