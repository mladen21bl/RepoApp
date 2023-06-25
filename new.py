import json

json_data = '''
{"web":
    {
    "client_id": "89314030326-b9rlc2650qahknh3ftj19n1o9ojt16fp.apps.googleusercontent.com",
    "project_id": "mojprojekat-390613",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "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",
    "redirect_uris": ["http://localhost:8000"],
    "javascript_origins": ["http://localhost:8000"]
    }
}
'''

data = json.loads(json_data)
refresh_token = None

if "web" in data:
    web_data = data["web"]
    if "refresh_token" in web_data:
        refresh_token = web_data["refresh_token"]

print(refresh_token)
