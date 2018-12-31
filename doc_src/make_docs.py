# -*- coding: utf-8 -*-
import subprocess


def run():
    cmd_api = "sphinx-apidoc -f -o ../doc_src ../"
    cmd_doc = "sphinx-build -b html -d ../doc_src/doctrees   ../doc_src ../doc_src/html"
    cmd_rm = "rm -rf ../docs"
    cmd_cp = "cp -rf ../doc_src/html ../docs"

    for cmd in [cmd_api, cmd_doc, cmd_rm, cmd_cp]:
        result = subprocess.call(cmd.split())
        print(result)


if __name__ == '__main__':
    run()
