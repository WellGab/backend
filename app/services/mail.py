import requests
import logging
from app.utils.setup import config
from fastapi.templating import Jinja2Templates
from pathlib import Path


BASE_PATH = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_PATH.joinpath("templates")))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MailService:
    @staticmethod
    def get_html_string(context, template_name):
        template = templates.get_template(template_name)
        return template.render(context)

    @staticmethod
    def get_headers():
        return {"api-key": config.SENDINBLUE_API_KEY}

    @classmethod
    def send_mail(
        cls,
        subject,
        email,
        template_context,
        template_name: str = "default_template.html",
    ):
        body = {
            "sender": {"name": "WellGab", "email": "support@wellgab.com"},
            "to": [{"email": email}],
            "subject": subject,
            "htmlContent": cls.get_html_string(template_context, template_name),
        }
        response = requests.post(
            config.SENDINBLUE_API_URL,
            headers=cls.get_headers(),
            json=body,
        )
        if response.status_code == 201:
            return True
        logger.error(response.text)
        return False
