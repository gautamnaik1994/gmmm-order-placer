module.exports = {
  apps: [
    {
      name: "main",
      script: "src/main.py",
      interpreter: require("fs").existsSync("./.venv/bin/python")
        ? "./.venv/bin/python"
        : "python3",
    }
  ],
};
