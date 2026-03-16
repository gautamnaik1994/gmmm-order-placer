module.exports = {
  apps: [
    {
      name: "main",
      script: "src/main.py",
      interpreter: require("fs").existsSync("./.venv/bin/python")
        ? "./.venv/bin/python"
        : "python3",
      kill_signal: "SIGTERM",
      kill_timeout: 15000,
    }
  ],
};
