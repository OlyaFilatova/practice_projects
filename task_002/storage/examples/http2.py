import asyncio
from urllib.request import urlopen
from .test_url import url


async def fetch(url):
    def _get():
        with urlopen(url) as response:
            body = response.read()
            status = response.status
            headers = response.headers.items()

            return status, headers, body

    return await asyncio.to_thread(_get)


async def main():
    request_task = asyncio.create_task(fetch(url))
    status, headers, body = await request_task
    print(status)
    print(headers)
    # print(body)


if __name__ == "__main__":
    asyncio.run(main())
