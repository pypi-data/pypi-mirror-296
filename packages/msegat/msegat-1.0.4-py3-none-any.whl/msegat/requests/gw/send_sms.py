from msegat.configuration import Configuration


class SendSMSRequest(object):
    """
    A class to represent an API request for sending an SMS to one or more recipients.
    """
    USER_NAME = 'userName'
    NUMBERS = 'numbers'
    USER_SENDER = 'userSender'
    API_Key = 'apiKey'
    MSG = 'msg'

    def __init__(self, numbers: str, msg: str):
        """
        Initialize a new instance of SendSMSRequest.

        :param numbers: A comma-separated string of phone numbers.
        :param msg: The message content to be sent.
        """
        self.user_name = Configuration.user_name
        self.user_sender = Configuration.user_sender
        self.api_key = Configuration.api_key
        self.numbers = numbers
        self.msg = msg

    def to_dictionary(self):
        """
        Convert the instance attributes into a dictionary.

        :return: A dictionary representation of the SendSMSRequest instance.
        """
        return {
            self.USER_NAME: self.user_name,
            self.NUMBERS: self.numbers,
            self.USER_SENDER: self.user_sender,
            self.API_Key: self.api_key,
            self.MSG: self.msg
        }

    @classmethod
    def from_dictionary(cls, dictionary: dict):
        """
        Create an instance of SendSMSRequest from a dictionary.

        :param dictionary: A dictionary with keys 'numbers' and 'msg'.
        :return: An instance of SendSMSRequest or None if the dictionary is invalid.
        """
        if dictionary is None:
            return None

        # Extract values from the dictionary
        numbers = dictionary.get(cls.NUMBERS)
        msg = dictionary.get(cls.MSG)

        # Return a new SendSMSRequest instance
        return cls(numbers=numbers, msg=msg)
