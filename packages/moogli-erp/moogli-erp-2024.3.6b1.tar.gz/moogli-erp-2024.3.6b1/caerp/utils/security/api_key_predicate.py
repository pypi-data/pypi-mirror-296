import logging
import time
from hashlib import md5


# 30 minutes tolerance (vms can be late ...)
DEFAULT_TOLERANCE = 60 * 30
logger = logging.getLogger(__name__)


def get_timestamp_from_request(request):
    """
    Retrieve a timestamp in the request's headers

    :param obj request: The Pyramid request object
    :returns: A timestamp
    :rtype: int
    """
    result = None
    if "timestamp" in request.headers:
        result = request.headers.get("timestamp")
    elif "Timestamp" in request.headers:
        result = request.headers.get("Timestamp")
    else:
        logger.error("No timestamp header found in the request")
        logger.error(list(request.headers.items()))
        raise KeyError("No timestamp header found")

    return result


def check_timestamp(timestamp, tolerance=DEFAULT_TOLERANCE):
    """
    Check that a timestamp is 'actual' it doesn't differ from now too much

    :param str timestamp: A time stamp in string format
    :param int tolerance: The difference we accept between now and the given
    timestamp (request original time)
    :returns: True if the timestamp is close enough
    :rtype: bool
    """
    timestamp = float(timestamp)
    current_second = time.time()
    return abs(timestamp - current_second) < tolerance


def get_clientsecret_from_request(request):
    """
    Retrieve a client secret from the request headers
    "Authorization" headers are checked

    :param obj request: The Pyramid request object
    :returns: An encoded client secret
    :rtype: str
    """
    auth = ""
    # request.headers is a case insensitive dict
    if "authorization" in request.headers:
        auth = request.headers.get("authorization")
    else:
        logger.error("No authorization header found")
        logger.error(list(request.headers.items()))
        raise KeyError("No Authorization header found")

    parts = auth.split()
    if len(parts) != 2:
        logger.error("Invalid Authorization header")
        logger.error(auth)
        raise KeyError("Invalid Authorization header")

    token_type = parts[0].lower()
    if token_type != "hmac-md5":
        logger.error("Invalid token type")
        logger.error(token_type)
        raise ValueError("Invalid token format %s" % token_type)
    else:
        client_secret = parts[1]
    return client_secret


def check_secret(client_secret, timestamp, api_key):
    """
    Check the client_secret matches

    :param str client_secret: The client secret sent by the client app
    :param int timestamp: The time stamp provided with the key
    :param str api_key: The configured api_key
    :returns: True/False
    :rtype: bool
    """
    secret = "{0}-{1}".format(timestamp, api_key)
    secret = secret.encode("utf-8")
    encoded = md5(secret).hexdigest()
    if encoded != client_secret:
        return False
    return True


class ApiKeyAuthenticationPredicate:
    """
    Custom view predicate validating the api key "key" passed in the headers

    api key can be set in the ini file under caerp.apikey

    the client app should :

        1- encode the api key with md5 then concatenate it with
    a salt grain and a timestamp then encode the key again
        2- Send the hash in the request header and the timestamp as request.GET
        param


    This predicate check the salt matches the apikey
    It also checks the timestamp is not too far from the current time
    """

    def __init__(self, val, config):
        self.key = val

    def text(self):
        return "Api Key Authentication = {0}".format(self.key)

    phash = text

    def _find_api_key(self, request):
        """
        Try to retrieve the api key from the current registry's settings
        """
        api_key = None
        if self.key in request.registry.settings:
            api_key = request.registry.settings[self.key]
        else:
            raise Exception(
                "The settings ini file doesn't contain any key "
                "named {}".format(self.key)
            )
        return api_key

    def __call__(self, context, request):
        """
        1- find the salt key in the headers
        2- check the timestamp
        3- check the salt
        4- True/False
        """
        logger.debug("Calling the api key predicate")
        timestamp = get_timestamp_from_request(request)

        if timestamp is None:
            logger.error("No timestamp provided in the headers")
            return False

        if not check_timestamp(timestamp):
            logger.error(
                "Invalid timestamp current time is {0} while "
                "timestamp is {1}".format(time.time(), timestamp)
            )
            return False

        client_secret = get_clientsecret_from_request(request)

        if client_secret is None:
            logger.error("No client secret provided in the headers")
            return False

        api_key = self._find_api_key(request)
        if api_key is None:
            logger.error("No api key could be found")
            return False

        if not check_secret(client_secret, timestamp, api_key):
            logger.error("Error checking the secret")
            return False

        return True
