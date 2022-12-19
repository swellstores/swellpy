import json

from requests import Response
from requests.exceptions import HTTPError


def response_formatter(res: Response) -> str:
    method = res.request.method
    url = res.url
    status = res.status_code
    msg = f'{method} {url} [HTTP {status}'

    return msg


def handle_requests_response(swell, res):

    if not res:
        raise Exception("No response received")

    swell.logger.debug(response_formatter(res))

    if res.status_code == 200:
        jsonRes = {}

        try:
            jsonRes = res.json()
        except json.JSONDecodeError:
            swell.logger.debug(
                f'Response could not be serialized. Check if record exists.')

        if 'errors' in jsonRes:
            swell.logger.debug(jsonRes['errors'])

    else:
        raise HTTPError(f'HTTP Error {res.status_code}: {res.reason}')

    return jsonRes
