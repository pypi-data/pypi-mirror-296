from msegat.handlers.handler import Handler
from msegat.helpers.api_helper import APIHelper
from msegat.responses.gw import send_sms as response
from msegat.requests.gw import send_sms as requests


class SendSMSHandler(Handler):
    """
    This API is used to send a sms to one or more recipient
    """

    path = '/gw/sendsms.php'
    response_model = response.SendSMSResponse

    def __call__(self, request: requests.SendSMSRequest):
        """
        In Python, classes, methods, and instances are callable because calling a class returns a new instance.
        Instances are callable if their class includes __call__() method.
        """
        parameters = request.to_dictionary()
        request = self.http_client.post(self.path, parameters=parameters)
        context = self.execute_request(request)
        return APIHelper.json_deserialize(context.response.raw_body, self.response_model.form_dictionary)


send_sms_handler = SendSMSHandler()
