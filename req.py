import requests
import base64
import json

# URL de votre API déployée sur Heroku
url = "https://tv1wdm122i.execute-api.eu-west-3.amazonaws.com/default/oma"
# url = "http://localhost:9000/2015-03-31/functions/function/invocations"

# Chemin vers l'image PNG que vous souhaitez envoyer
image_path = "test_data/3.png"
# api_key = "pst9MAyUZw2HKQhfKa1wt1SWQ0ElcanJ13d6OVcI"

# Lire l'image en binaire
# with open(image_path, "rb") as image_file:
#     print("image chargée", image_file)
#     file = {"file": image_file}
#     # headers = {"Authorization": "Bearer " + api_key}
#     response = requests.post(url, files=file)  # , headers=headers)

with open(image_path, "rb") as image_file:
    image_data = image_file.read()
    encoded_image = base64.b64encode(image_data).decode("utf-8")
    # print(encoded_image)
encoded_image = "f"
payload = {"file": encoded_image}

# Envoyer la requête POST avec les données de l'image
response = requests.post(url, json=payload)

bl = '{"file":"f"}'
print(json.loads(bl)["file"])

# Vérifiez la réponse de l'API
if response.status_code == 200:
    data = response.json()
    print(data)
    # nordwood_scale = data["nordwood_scale"]
    # print(f"Nordwood Scale: {nordwood_scale}")
else:
    print(f"Failed to get a response, status code: {response.json()}")
    # print(json.loads(response.json()["error"]["body"]))
    with open("blaf.txt", "w", encoding="utf-8") as file:
        file.write(response.text)
    # print(type(response.json()["error"]))


fhg = {
    "resource": "/oma",
    "path": "/oma",
    "httpMethod": "POST",
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/json",
        "Host": "tv1wdm122i.execute-api.eu-west-3.amazonaws.com",
        "User-Agent": "python-requests/2.32.3",
        "X-Amzn-Trace-Id": "Root=1-666052a7-5c68285a2904f61d491011d0",
        "X-Forwarded-For": "79.174.206.120",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Proto": "https",
    },
    "multiValueHeaders": {
        "Accept": ["*/*"],
        "Accept-Encoding": ["gzip, deflate"],
        "Content-Type": ["application/json"],
        "Host": ["tv1wdm122i.execute-api.eu-west-3.amazonaws.com"],
        "User-Agent": ["python-requests/2.32.3"],
        "X-Amzn-Trace-Id": ["Root=1-666052a7-5c68285a2904f61d491011d0"],
        "X-Forwarded-For": ["79.174.206.120"],
        "X-Forwarded-Port": ["443"],
        "X-Forwarded-Proto": ["https"],
    },
    "queryStringParameters": None,
    "multiValueQueryStringParameters": None,
    "pathParameters": None,
    "stageVariables": None,
    "requestContext": {
        "resourceId": "r8di3v",
        "resourcePath": "/oma",
        "httpMethod": "POST",
        "extendedRequestId": "Y5HaQFJXCGYEQvA=",
        "requestTime": "05/Jun/2024:11:57:27 +0000",
        "path": "/default/oma",
        "accountId": "471112953630",
        "protocol": "HTTP/1.1",
        "stage": "default",
        "domainPrefix": "tv1wdm122i",
        "requestTimeEpoch": 1717588647730,
        "requestId": "c1557cb0-17e6-4360-86f5-33fa76028a77",
        "identity": {
            "cognitoIdentityPoolId": None,
            "accountId": None,
            "cognitoIdentityId": None,
            "caller": None,
            "sourceIp": "79.174.206.120",
            "principalOrgId": None,
            "accessKey": None,
            "cognitoAuthenticationType": None,
            "cognitoAuthenticationProvider": None,
            "userArn": None,
            "userAgent": "python-requests/2.32.3",
            "user": None,
        },
        "domainName": "tv1wdm122i.execute-api.eu-west-3.amazonaws.com",
        "deploymentId": "829hm3",
        "apiId": "tv1wdm122i",
    },
    "body": '{"file": "f"}',
    "isBase64Encoded": False,
}
