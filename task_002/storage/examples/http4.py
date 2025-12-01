import asyncio
import ssl
from urllib.parse import urlparse
from .test_url import url


def decode_chunked(body: str) -> str:
    result = []
    i = 0
    length = len(body)

    while i < length:
        line_end = body.find("\r\n", i)
        chunk_size_hex = body[i:line_end]
        chunk_size = int(chunk_size_hex, 16)
        i = line_end + 2

        if chunk_size == 0:
            break

        chunk = body[i : i + chunk_size]
        result.append(chunk)
        i += chunk_size + 2

    return "".join(result)


async def fetch(url: str):
    parsed = urlparse(url)

    ssl_ctx = ssl.create_default_context()

    reader, writer = await asyncio.open_connection(parsed.hostname, 443, ssl=ssl_ctx)

    request = (
        f"GET {parsed.path or "/"} HTTP/1.1\r\n"
        f"Host: {parsed.hostname}\r\n"
        "User-Agent: Task 002 - approach 4\r\n"
        "Accept: application/vnd.github+json\r\n"
        "Connection: close\r\n"
        "\r\n"
    )

    writer.write(request.encode())
    await writer.drain()

    data = await reader.read()
    writer.close()
    await writer.wait_closed()

    decoded_data = data.decode()

    head, body = decoded_data.split("\r\n\r\n", 1)
    if "Transfer-Encoding: chunked".lower() in head.lower():
        body = decode_chunked(body)

    lines = head.split("\r\n")
    status_code = lines[0].split(" ")[1]
    header_lines = lines[1:]

    formatted_headers = [
        (header.split(":", maxsplit=1)[0], header.split(":", maxsplit=1)[1].strip())
        for header in header_lines
    ]

    return status_code, formatted_headers, body


async def main():
    request_task = fetch(url)
    status_code, headers, body = await request_task

    print(status_code)
    print(headers)
    print(body)


if __name__ == "__main__":
    asyncio.run(main())
