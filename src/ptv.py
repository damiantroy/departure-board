import hmac
from hashlib import sha1


def sign_url(config, request):
    api_key = config.api_key.encode("utf-8")
    dev_id = config.dev_id

    request = request + ("&" if ("?" in request) else "?")
    raw = request + "devid={dev_id}".format(dev_id=dev_id)
    hashed = hmac.new(api_key, raw.encode("utf-8"), sha1)
    signature = hashed.hexdigest()
    return config.base_url + raw + "&signature={signature}".format(signature=signature)
