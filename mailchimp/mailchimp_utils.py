import requests
from django.conf import settings
import json


MAILCHIMP_API_URL = f'https://{settings.MAILCHIMP_DATA_CENTER}.api.mailchimp.com/3.0'


def subscribe_email(email):
    """
    Subscribe an email to the Mailchimp audience list.
    :param email: Email address of the user to subscribe.
    :return: Response from Mailchimp API.
    """
    # API endpoint to add members to the list
    url = f"{MAILCHIMP_API_URL}/lists/{settings.MAILCHIMP_LIST_ID}/members/"
    
    # Payload with the email and status (subscribed)
    payload = {
        "email_address": email,
        "status": "subscribed"
    }
    
    headers = {
        "Authorization": f"apikey {settings.MAILCHIMP_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Make the API request to subscribe the user
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    return response
