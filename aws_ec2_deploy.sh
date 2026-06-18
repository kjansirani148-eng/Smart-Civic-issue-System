#!/usr/bin/env bash
set -e

echo "Updating package index..."
sudo apt update
sudo apt upgrade -y

echo "Installing dependencies..."
sudo apt install -y python3 python3-venv python3-pip mysql-client git nginx

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Creating .env from example..."
if [ ! -f .env ] && [ -f .env.example ]; then
  cp .env.example .env
  echo "Please update .env with your production values." >&2
fi

echo "Configure database and AWS environment variables in .env."

echo "To run locally: source venv/bin/activate && python run.py"
