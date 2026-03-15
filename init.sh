#! /bin/bash
echo "Running Init Script"

set -e

cd gmmm-python-server

echo "Inside project"

# print working directory path to console
echo "Working Directory: $PWD"
git reset --hard
git pull origin main

if ! command -v uv >/dev/null 2>&1; then
	echo "uv not found; installing..."
	if command -v curl >/dev/null 2>&1; then
		curl -LsSf https://astral.sh/uv/install.sh | sh
	elif command -v wget >/dev/null 2>&1; then
		wget -qO- https://astral.sh/uv/install.sh | sh
	else
		echo "Neither curl nor wget found; trying pip user install for uv..."
		python3 -m pip install --user -U uv
	fi
	export PATH="$HOME/.local/bin:$PATH"
fi

if [ -f uv.lock ]; then
	uv sync --frozen
else
	uv sync
fi

pm2 delete all
if [ -x .venv/bin/python ]; then
	pm2 start src/main.py --interpreter .venv/bin/python --name main
else
	pm2 start src/main.py --interpreter python3 --name main
fi
pm2 save


# crontab -l > mycron
# echo "45 3 * * 1-5 pm2 start gmmm-python-server/price_crossover_detector.py --interpreter python3 " >> mycron
# crontab mycron
# rm mycron
