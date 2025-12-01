import asyncio
import http.client
from urllib.parse import urlparse

from .test_url import url


async def fetch(url):
    def _get():
        parsed = urlparse(url)
        conn = http.client.HTTPSConnection(parsed.netloc)
        headers = {"User-Agent": "Task 002 - approach 3"}
        conn.request("GET", parsed.path or "/", headers=headers)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        return res.status, res.headers.items(), data

    return await asyncio.to_thread(_get)


async def main():
    request_task = fetch(url)
    status, headers, body = await request_task

    print(status)
    print(headers)
    print(body)


if __name__ == "__main__":
    asyncio.run(main())
