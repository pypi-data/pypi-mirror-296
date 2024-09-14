from msegat.configuration import Configuration
from msegat.requests.gw.send_sms import SendSMSRequest
from msegat.handlers.msgs.send_sms import send_sms_handler


class MsegatClient(object):
    """
    A client class for interacting with the Msegat SMS service API.
    """
    config = Configuration

    def __init__(self, user_sender, user_name, api_key):
        """
        Initializes the MsegatClient with the required credentials.

        :param user_sender: The sender's identifier (e.g., phone number or username).
        :param user_name: The username for authentication.
        :param api_key: The API token for authenticating requests.
        """
        Configuration.user_sender = user_sender
        Configuration.user_name = user_name
        Configuration.api_key = api_key

    def send_message(self, numbers, msg):
        """
        Sends an SMS message to one or more recipients via the Msegat API.

        :param numbers: A comma-separated string of recipient phone numbers.
                        Can send to one or multiple numbers (up to 500 per request).
        :param msg: The content of the SMS message. The system automatically handles encoding for different languages.

        :return: An HTTP response. If successful, returns status 200 with the result in the response body as JSON.
                 On failure, returns an HTTP error response with a JSON body containing an error code and description.
        """
        return send_sms_handler(request=SendSMSRequest(numbers, msg))

