from msegat.client import MsegatClient


def send_sms():
    """
    This API is used to send a sms to one or more recipient
    """
    user_sender = input("Please Enter the user sender:")
    user_name = input("Please Enter the user name:")
    api_key = input("Please Enter the apiKey:")
    numbers = input("Please Enter the numbers:")
    msg = input("Please Enter the msg:")
    return MsegatClient(user_sender, user_name, api_key).send_message(numbers, msg)


if __name__ == '__main__':
    send_sms()
