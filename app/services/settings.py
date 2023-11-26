
from ..models.user import Users
from ..models.settings import Settings
from ..schemas.settings import SettingsSchema
import bson


class SettingsService:
    @staticmethod
    def create_or_update_setting(user: Users, data: SettingsSchema) -> Settings:
        setting = SettingsService.get_setting_by_user(user)
        if not setting:
            setting:  Settings = Settings(user=user)

        if data.ninety_days_chat_limit:
            setting.ninety_days_chat_limit = data.ninety_days_chat_limit

        if data.text_size:
            setting.text_size = data.text_size

        if data.display:
            setting.display = data.display

        setting.save()
        return setting

    @staticmethod
    def get_setting_by_user(user: Users) -> Settings:
        setting = Settings.objects(user=user).first()
        return setting
