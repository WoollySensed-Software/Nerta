import tempfile
import json

from streamlit import secrets


DEBUG = secrets['dev']['debug']
TABLE_NAME = secrets['dev']['table_name']
DB_URL = secrets['database']['url']
DB_KEY = secrets['database']['key']

if DEBUG:
    temp_path = 'creds.json'
else:
    credits = {
        'type': secrets['credits']['type'], 
        'project_id': secrets['credits']['project_id'], 
        'private_key_id': secrets['credits']['private_key_id'], 
        'private_key': secrets['credits']['private_key'], 
        'client_email': secrets['credits']['client_email'], 
        'client_id': secrets['credits']['client_id'], 
        'auth_uri': secrets['credits']['auth_uri'], 
        'token_uri': secrets['credits']['token_uri'], 
        'auth_provider_x509_cert_url': secrets['credits']['auth_provider_x509_cert_url'], 
        'client_x509_cert_url': secrets['credits']['client_x509_cert_url'], 
        'universe_domain': secrets['credits']['universe_domain']
    }

    with tempfile.NamedTemporaryFile(
        mode='w', 
        delete=False, 
        suffix='.json', 
        encoding='utf-8'
    ) as tmp_file:
        json.dump(credits, tmp_file, indent=4)
        temp_path = tmp_file.name
