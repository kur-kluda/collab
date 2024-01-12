from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy

class FakeValidator:
    def validate(self, password, user=None):
        return True
    message = _("Enter a valid value.")
    def get_help_text(self):
        return "anything goes"
    def get_help_text_html(self):
        return "<p>enter anything you wish :))</p>"