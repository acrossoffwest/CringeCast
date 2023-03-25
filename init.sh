#!/usr/bin/env bash

sudo ln -s $(pwd)/utils/pulseaudio.service /etc/systemd/system/pulseaudio.service
sudo systemctl enable pulseaudio.service