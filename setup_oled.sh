#!/bin/bash
# Setup script for SunFounder OLED display dependencies

echo "🔧 Setting up SunFounder OLED display dependencies..."

# Enable I2C
echo "Enabling I2C interface..."
sudo raspi-config nonint do_i2c 0

# Install required packages
echo "Installing system packages..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev python3-pil i2c-tools libopenjp2-7

# Install Python libraries for luma.oled
echo "Installing Python libraries..."
pip3 install luma.oled
pip3 install pillow

# Test I2C connection
echo -e "\n📟 Checking for I2C devices..."
i2cdetect -y 1

echo -e "\n✅ Setup complete!"
echo "If you see a device at address 0x3C, your OLED is connected properly."
echo "Run: python3 color_symphony_oled.py"