


import urllib.request
import json
import os
import ssl
import json
from dotenv import load_dotenv


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

#allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

load_dotenv()
api_key = os.getenv('API_KEY')
endpoint = os.getenv('ENDPOINT')

# Read input1 from JSON file
with open('input1.json', 'r') as file:
    input1 = json.load(file)

# Read input1 from JSON file
with open('input2.json', 'r') as file:
    input2 = json.load(file)

data = input2
body = str.encode(json.dumps(data))
url = endpoint
# Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint

if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")

headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))
