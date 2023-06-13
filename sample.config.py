import os

MS_ENDPOINT = 'https://graph.microsoft.com/v1.0/'
MS_SCOPE = ['User.ReadBasic.All']
MS_CLIENT_ID = 'your-clientid-here'
MS_CLIENT_SECRET = 'your-secret-here'
MS_AUTHORITY = 'https://login.microsoftonline.com/your-uuid-here'
MS_AUTH_RESPONSE = '/msauth_response'
SESSION_TYPE = 'filesystem'
APP_VERSION = '0.1 BETA'
SECRET_KEY = os.urandom(12).hex()