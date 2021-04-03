#!/bin/bash
cd rpi-rgb-led-matrix
echo "Running rpi-rgb-led-matrix setup..."
sudo apt-get update && sudo apt-get install python3-dev python3-pillow -y
make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)
echo "Done."
echo "Checking out master and pulling the latest changes..."
git reset --hard
git checkout main
git fetch origin --prune
git pull
make
echo "Done."
echo -e "\nYou'll need a config.json file to customize your settings."
read -p "Would you like to create a new one from a template now? [Y/n] " answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
    rm config.json
    cp config.template.json config.json
    echo -e "\nDefault config.json file created.\n"
else
    echo -e "\nSkipping config.json creation.\n"
fi
chown pi:pi config.json
echo "Setup complete!"