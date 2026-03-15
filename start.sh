#! /bin/bash
echo "Running Start Script"

set -e

# cd gmmm-python-server

# echo "Inside prject"

# # print working directory path to console
# echo "Working Directory: $PWD"

# if [ -x .venv/bin/python ]; then
# 	pm2 start src/main.py  --name str_1 --no-autorestart --cron-restart="45 3 * * 1-5" --interpreter .venv/bin/python
# else
# 	pm2 start src/main.py --name str_1 --no-autorestart --cron-restart="45 3 * * 1-5" --interpreter python3
# fi