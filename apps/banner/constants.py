from django.db import models

class BannerStatus(models.TextChoices):
    ENABLED = "enabled"
    DISABLED = "disabled"

DEFAULT_STYLE = {
    "background_color": "black",
    "text_color": "white",
    "height": "100px",
    "padding":"35px",
    "text_align": "center"
}

DEFAULT_TEXT = "Add some alluring text here"