import base64
import responder

api = responder.API()


@api.route("/status")
def status(req, resp):
    resp.media = {"status": "ok"}


@api.route("/data/upload",)
async def upload_image_file(req, resp):
    data = await req.media()
    print(data)
    file_name = data["fileName"]
    content_type = data["contentType"]
    images_b64 = data["images"]
    write_image(images_b64, "png")


def write_image(images_b64, extension):
    for i, content in enumerate(images_b64):
        image = base64.b64decode(content)
        file_name = str(i) + "." + extension
        with open(file_name, "wb") as f:
            f.write(image)
    return True




if __name__ == '__main__':
    api.run(port=8080)
