#!/usr/bin/env python3
import os
import subprocess
import pycurl
import json
from time import time
from shutil import rmtree

try:
    print("Running npm init...")
    subprocess.run(
        ["npm", "init", "-y"], capture_output=True, universal_newlines=True, check=True
    )
    dirs = (
        "src",
        "dist",
        "src/server",
        "src/server/utils",
        "src/static",
        "src/static/styles",
        "src/static/static",
        "src/static/javascript",
        "src/views",
        "src/views/pages",
        "src/views/partials",
    )

    print("Creating directories...")
    for dir in dirs:
        os.mkdir(dir)

    print("Installing dev dependencies...")
    subprocess.run(
        [
            "npm",
            "i",
            "--save-dev",
            "tailwindcss",
            "@tailwindcss/cli",
            "autoprefixer",
            "postcss",
            "postcss-cli",
            "nodemon",
            "prettier",
            "prettier-plugin-tailwindcss",
            "tsx",
            "typescript",
            "@types/express",
            "@types/validator",
        ],
        capture_output=True,
        universal_newlines=True,
        check=True,
    )
    print("Dev dependencies installed successfully!")

    print("Installing production dependencies...")
    subprocess.run(
        ["npm", "i", "express", "validator", "dotenv", "ejs"],
        capture_output=True,
        universal_newlines=True,
        check=True,
    )
    print("Production dependencies installed successfully!")

    print("Getting template files...")

    template_file_names = (
        ".prettierrc",
        "nodemon.json",
        "postcss.config.js",
        "tailwind.config.js",
        "tsconfig.json",
        "copyAssets.js",
        "index.html",
        "input.css",
    )
    for file in template_file_names:
        with open(file, "wb") as f:
            curl = pycurl.Curl()
            curl.setopt(
                curl.URL,
                (
                    "https://raw.githubusercontent.com/Nathanael-Allen/"
                    f"my_template/refs/heads/master/{file}"
                ),
            )
            curl.setopt(curl.WRITEDATA, f)
            curl.perform()
            curl.close()
    os.rename("input.css", "src/static/input.css")
    os.rename("index.html", "src/index.html")
    open("src/server.ts", "a").close()
    print("Files successfully copied!")

    print("Writing scripts to package.json...")
    with open("package.json", "r") as f:
        py_json = json.loads(f.read())

    with open("package.json", "w") as f:
        py_json["type"] = "module"
        py_json["scripts"]["dev"] = "nodemon"
        py_json["scripts"]["build-tw"] = (
            ("@tailwindcss/cli -i ./src/styles/input.css "),
            ("-o ./src/styles/output.css"),
        )
        py_json["scripts"]["copy-assets"] = "node copyAssets.js"
        py_json["scripts"]["build"] = "npm run build-tw && npm run copy-assets && tsc"
        new_json = json.dumps(py_json)
        f.write(new_json)
    subprocess.run(
        ["git", "init", "-b", "main"],
        capture_output=True,
        universal_newlines=True,
        check=True,
    )
    print("Scripts successfully written!")
    print("Template set up successfully!\n")
except Exception as e:
    now = time()
    print("*" * 50)
    print("\n")
    print(e)
    print("\n")
    print("Something went wrong... Cleaning up files...")
    print("\n")
    for dir in os.listdir():
        if (now - os.path.getctime(dir)) < 20:
            if dir in dirs:
                rmtree(dir, ignore_errors=True)
            elif dir in template_file_names:
                os.remove(dir)
            elif dir == "node_modules":
                rmtree(dir, ignore_errors=True)
            elif dir == "package.json":
                os.remove(dir)
            elif dir == "package-lock.json":
                os.remove(dir)
        else:
            continue
    print("Template files and directories purged...\n")
