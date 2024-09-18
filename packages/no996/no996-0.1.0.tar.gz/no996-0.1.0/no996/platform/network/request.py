import asyncio
import json
from logging import getLogger

import aiohttp
from aiohttp_socks import ChainProxyConnector, ProxyConnector
from faker import Faker

from no996.platform.config import settings

logger = getLogger(__name__)


class RequestURL:
    def __init__(self, is_proxy: bool = False):
        faker = Faker()
        self.header = {"user-agent": faker.user_agent(), "Accept": "application/json"}
        self.is_proxy = is_proxy
        self.session = None

    async def start_session(self):
        connector = None
        if self.is_proxy and settings.proxy.PROXY_ENABLE:
            if settings.proxy.PROXY_TYPE == "http":
                connector = ChainProxyConnector.from_urls([settings.proxy.PROXY_URI])
            elif settings.proxy.PROXY_TYPE == "socks5":
                connector = ProxyConnector.from_url(settings.proxy.PROXY_URI)
            else:
                logger.error("[网络连接]:不支持的代理类型")
                raise ValueError("[网络连接]:不支持的代理类型")

        timeout = aiohttp.ClientTimeout()
        self.session = aiohttp.ClientSession(
            headers=self.header,
            connector=connector,
            json_serialize=json.dumps,
            timeout=timeout,
        )

    async def close_session(self):
        await self.session.close()

    async def __aenter__(self):
        await self.start_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_session()

    async def check_url(self, url) -> bool:
        if not url.startswith("http"):
            url = f"http://{url}"
        try:
            async with self.session.head(url, allow_redirects=True) as response:
                if response.status == 200:
                    return True
                else:
                    raise aiohttp.ClientResponseError(
                        response.request_info,
                        response.history,
                        status=response.status,
                        message=f"[网络连接]:请求失败: {url}， status：{response.status}",
                        headers=response.headers,
                    )
        except aiohttp.ClientResponseError:
            logger.error(f"[网络连接]:请求失败: {url}")
            return False

    async def get_url(self, url, retry=3):
        retry_time = 0
        while True:
            try:
                async with self.session.get(url) as response:
                    response.raise_for_status()
                    logger.info(
                        f"[网络连接] 成功连接到 {url}. Status: {response.status}"
                    )
                    await response.read()
                    return response
            except aiohttp.ClientResponseError:
                logger.error(f"[网络连接]:无法连接到 {url}，请等待 5 秒后重试")
                retry_time += 1
                if retry_time >= retry:
                    raise ValueError(f"[网络连接] 无法连接到 {url}, 请检查网络连接设置")
                await asyncio.sleep(5)

    async def post_url(self, url, data: dict, retry=3):
        retry_time = 0
        while True:
            try:
                async with self.session.post(url, data=data) as response:
                    response.raise_for_status()
                    logger.info(
                        f"[网络连接] 成功连接到 {url}. Status: {response.status}"
                    )
                    await response.read()
                    return response
            except aiohttp.ClientResponseError:
                logger.error(f"[网络连接]:无法连接到 {url}，请等待 5 秒后重试")
                retry_time += 1
                if retry_time >= retry:
                    raise ValueError(f"[网络连接] 无法连接到 {url}, 请检查网络连接设置")
                await asyncio.sleep(5)

    async def post_form(self, url, data: dict, files: dict, retry=3):
        retry_time = 0
        while True:
            try:
                data.update(files)
                async with self.session.post(url, data=data) as response:
                    response.raise_for_status()
                    logger.info(
                        f"[网络连接] 成功连接到 {url}. Status: {response.status}"
                    )
                    await response.read()
                    return response
            except aiohttp.ClientResponseError:
                logger.error(f"[网络连接]:无法连接到 {url}，请等待 5 秒后重试")
                retry_time += 1
                if retry_time >= retry:
                    raise ValueError(f"[网络连接] 无法连接到 {url}, 请检查网络连接设置")
                await asyncio.sleep(5)


class RequestContent(RequestURL):
    async def get_json(self, url) -> dict:
        response = await self.get_url(url)
        if response:
            return await response.json()

    async def get_html(self, url):
        response = await self.get_url(url)
        if response:
            return await response.text()

    async def post_json(self, url, data: dict) -> dict:
        response = await self.post_url(url, data)
        if response:
            return await response.json()

    async def post_data(self, url, data: dict):
        response = await self.post_url(url, data)
        if response:
            return response

    async def post_files(self, url, data: dict, files: dict):
        return await self.post_form(url, data, files)
