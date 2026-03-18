module.exports = {
  apps: [
    {
      name: "main",
      script: "src/main.py",
      interpreter: require("fs").existsSync("./.venv/bin/python")
        ? "./.venv/bin/python"
        : "python3",
      env: {
        PYTHONUNBUFFERED: "1",
        LOG_LEVEL: "INFO",
      },
      kill_signal: "SIGTERM",
      kill_timeout: 15000,
    }
  ],
};
