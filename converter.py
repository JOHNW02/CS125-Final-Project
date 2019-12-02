import json
import base64

data = {}
with open('imageToSend.jpg', mode='rb') as file:
    img = file.read()
data['img'] = base64.encodebytes(img).decode("utf-8")

json_data = json.dumps(data)
with open('toUpdate.json', mode='w') as another_file:
    another_file.write(json_data)