class SendSMSResponse(object):
    """
    This API is used to send a message to one or more recipients
    """

    def to_dictionary(self):
        """
        Return the property of the object as a dictionary
        """
        return {}

    @classmethod
    def form_dictionary(cls, dictionary: dict):
        """
        Creates an instance of this model from a dictionary
        """
        if dictionary is None:
            return None

        # Return an object of this model
        return cls()
