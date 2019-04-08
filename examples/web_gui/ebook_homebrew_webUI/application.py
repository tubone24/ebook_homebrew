# -*- coding: utf-8 -*-
"""Creating PDF for Image files with Web GUI
"""
from flask import Flask, request, make_response, jsonify, render_template
import os
import sys
import werkzeug
from ebook_homebrew.convert import Image2PDF

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

UPLOAD_DIR = "."


@app.route("/")
def index():
    """Index Page
    """
    return render_template("index.html")


@app.route("/upload")
def uploader():
    """Upload GUI
    """
    return render_template("upload.html")


@app.route("/data/upload", methods=["POST"])
def create_pdf():
    """Create PDF input images
    """
    digits = ""
    extension = ""

    if "digits" in request.form:
        digits = str(request.form["digits"])
    if "extension" in request.form:
        extension = str(request.form["extension"])
    if "uploadFile" not in request.files:
        make_response(jsonify({"result": "uploadFile is required."}))

    sys.stderr.write("digits = " + digits + "\n")
    upload_files = request.files.getlist("uploadFiles")
    response = make_response()
    for file in upload_files:
        file_name = file.filename
        sys.stderr.write("fileName = " + file_name + "\n")
        save_file_name = werkzeug.utils.secure_filename(file_name)
        file.save(os.path.join(UPLOAD_DIR, save_file_name))
    converter = Image2PDF(digits, extension, UPLOAD_DIR)
    converter.make_pdf("result.pdf", True)

    with open("result.pdf", "rb") as f:
        response.data = f.read()
        downloadFileName = "result.pdf"
        response.headers["Content-Disposition"] = "attachment; filename=" + downloadFileName
        response.mimetype = "application/pdf"
    return response


@app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
def handle_over_max_file_size(error):
    """
    Args:
        error:

    Returns:

    """
    print("werkzeug.exceptions.RequestEntityTooLarge" + error)
    return 'result : file size is overed.'


if __name__ == "__main__":
    print(app.url_map)
    app.run(host="0.0.0.0", port=8080)
