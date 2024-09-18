from sqlmodel import Session

from no996.platform.notify.plugins.bark import BarkNotification
from no996.platform.notify.plugins.tg import TelegramNotification
from app.models import NotifyConfig, NotifyMessage, NotifyTokenType
from app.repository.notify_config import NotifyConfigRepository


class Notify:
    def __init__(self, session: Session, user_id: int):
        self.notify_config_repository = NotifyConfigRepository(session)

        self.token_obj_list: [
            NotifyConfig
        ] = self.notify_config_repository.all_by_fields({"user_id": user_id})

    async def post_msg(
        self, message_type: NotifyTokenType, message: NotifyMessage
    ) -> bool:
        token_obj_list: list[NotifyConfig] = list(
            filter(lambda x: x.type_ == message_type, self.token_obj_list)
        )

        if not token_obj_list:
            return False

        if message_type == NotifyTokenType.BARK:
            async with BarkNotification(token_obj_list[0].token) as bn:
                return await bn.post_msg(message)

        if message_type in (NotifyTokenType.TG_ORDER, NotifyTokenType.TG_SYSTEM):
            if token_obj_list:
                token, chat_id = token_obj_list[0].token.split("|x|x|")

                async with TelegramNotification(token, chat_id) as tn:
                    return await tn.post_msg(message)
        return False
