import requests # Import the requests module for making HTTP requests
from flask_babel import _ # Import the _ function for translations from flask_babel
from app import app # Import the Flask app instance

def translate(text, source_language, dest_language):
    # Check if the translation service is configured
    if 'MS_TRANSLATOR_KEY' not in app.config or \
            not app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    
    # Set up the authentication headers for the translation API
    auth = {
        'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY'],
        'Ocp-Apim-Subscription-Region': 'australiaeast',
    }
    # Make a POST request to the Microsoft Translator API
    r = requests.post(
        'https://api.cognitive.microsofttranslator.com'
        '/translate?api-version=3.0&from={}&to={}'.format(
            source_language, dest_language), headers=auth, json=[{'Text': text}])
    # Check if the request was successful
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    # Return the translated text from the response
    return r.json()[0]['translations'][0]['text']