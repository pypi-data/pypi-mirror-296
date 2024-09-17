import aiofiles
import aiohttp
import asyncio
import re


def http_request(func) -> object:
    """
    :param func:
    :return object:
    """
    def _wrapper(*args, **kwargs) -> None:
        asyncio.run(func(*args, **kwargs))
    return _wrapper


async def http_find_html_pattern(url: str, pattern: str) -> list:
    """
    :param url:
    :param pattern:
    :return list:
    """
    _compile: re.compile = re.compile(pattern=pattern)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return []
                content: str = await response.text()
        matches = _compile.findall(string=content)
        return matches
    except aiohttp.ClientConnectionError:
        return []


async def http_download_file(url: str, folder: str, filename: str) -> bool:
    """
    :param url:
    :param folder:
    :param filename:
    :return:
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return False
                async with aiofiles.open("{0}/{1}".format(folder, filename), mode="wb") as handle:
                    await handle.write(await response.read())
        return True
    except aiohttp.ClientConnectionError:
        return False
