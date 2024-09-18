import logging

from no996.platform.config import settings
from no996.platform.network.request import RequestContent
from app.models import NotifyBark

logger = logging.getLogger(__name__)


class BarkNotification(RequestContent):
    def __init__(self, token, **kwargs):
        super().__init__()
        self.token = token
        self.url = settings.notify.BARK_URL

    async def post_msg(self, notify_: NotifyBark):
        notify = NotifyBark.model_validate(notify_.model_dump())

        body = {
            "title": notify.title,
            "body": notify.message,
            "device_key": self.token,
            "sound": notify.sound,
            "badge": notify.badge,
            "icon": notify.poster_path,
            "group": notify.group,
        }

        if "copy_" in notify:
            body["copy"] = notify.copy_value

        response = await self.post_data(self.url, body)
        logger.info(f"[Bark Notification] {response.status}")
        return response.status == 200
