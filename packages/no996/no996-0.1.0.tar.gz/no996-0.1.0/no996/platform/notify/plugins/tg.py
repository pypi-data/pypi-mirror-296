import logging

from no996.platform.network.request import RequestContent
from app.models import NotifyTg

logger = logging.getLogger(__name__)


class TelegramNotification(RequestContent):
    def __init__(self, token, chat_id, **kwargs):
        super().__init__(is_proxy=True)
        self.token = token
        self.chat_id = chat_id
        self.message_url = f"https://api.telegram.org/bot{token}/sendMessage"

    async def post_msg(self, data: NotifyTg):
        data = {
            "chat_id": self.chat_id,
            "caption": data.message,
            "text": data.message,
            "disable_notification": False,
        }
        response = await self.post_data(self.message_url, data)

        logger.info(f"[Telegram Notification] {response.status}")
        return response.status == 200
