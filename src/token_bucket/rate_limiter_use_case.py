from typing import List
import asyncio
import aiohttp

from rate_limiter import RateLimiter


async def send_request(client_session: aiohttp.ClientSession, url: str, rate_limiter: RateLimiter):
    async with rate_limiter.throttle():
        print(f'sending url: {url}')
        response = await client_session.get(url)
        print(f'releasing throttler')

    print(f'reading stream of response from {url}')
    response_text = await response.text()
    response.release()

    return response_text


async def send_multiple_requests(urls: List[str]):
    async with RateLimiter(rate_limit=3, concurrency_limit=3) as rate_limiter:
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.ensure_future(
                    send_request(client_session=session,
                                 url=url,
                                 rate_limiter=rate_limiter)
                )
                for url in urls
            ]

            return await asyncio.gather(*tasks)


async def main():
    return await send_multiple_requests(['https://google.com/',
                                         'https://bing.com/',
                                         'https://wikipedia.com/'])


def run_main():
    asyncio.run(main())


run_main()
