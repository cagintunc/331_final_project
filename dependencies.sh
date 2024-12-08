#!/bin/bash

set -e

echo "Updating system packages..."
sudo apt update

echo "Installing required packages..."
sudo apt install -y unzip build-essential zlib1g-dev libbz2-dev liblzma-dev libcurl4-openssl-dev libssl-dev nodejs npm

echo "Installing JBrowse CLI..."
sudo npm install -g @jbrowse/cli

if [ ! -d "htslib-1.17" ]; then
  echo "htslib source directory not found. Downloading..."
  wget https://github.com/samtools/htslib/releases/download/1.17/htslib-1.17.tar.bz2
  tar -xjf htslib-1.17.tar.bz2
fi

echo "Building and installing htslib..."
cd htslib-1.17
./configure --disable-lzma
make
sudo make install
cd ..

echo "Installing samtools..."
sudo apt install -y samtools

echo "Updating system packages (final check)..."
sudo apt update

echo "Setup completed successfully!"
