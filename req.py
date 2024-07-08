import requests
import base64

# URL de votre API déployée sur Heroku
url = "https://tv1wdm122i.execute-api.eu-west-3.amazonaws.com/default/oma"

# Chemin vers l'image PNG que vous souhaitez envoyer
# image_path = "test_data/4.png"
image_path = "training/datasets/hair_norwood_hamilton-1/train/6/20231102123718HfjxlX_gauss_jpg.rf.c581bbd43daf80c55fcdd5c613c18506.jpg"

with open(image_path, "rb") as image_file:
    image_data = image_file.read()
    encoded_image = base64.b64encode(image_data).decode("utf-8")
    payload = {"file": encoded_image}

# Envoyer la requête POST avec les données de l'image
response = requests.post(url, json=payload)

# Vérifiez la réponse de l'API
if response.status_code == 200:
    data = response.json()
    nordwood_scale = data["nordwood_scale"]
    print(f"Nordwood Scale: {nordwood_scale}")
else:
    print(f"Failed to get a response, status code: {response.json()}")
