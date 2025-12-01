from urllib import request

from .test_url import url


if __name__ == "__main__":
    with request.urlopen(url) as response:
        body = response.read()
        status = response.status
        headers = response.headers.items()

    print(status)
    print(headers)
    print(body)
