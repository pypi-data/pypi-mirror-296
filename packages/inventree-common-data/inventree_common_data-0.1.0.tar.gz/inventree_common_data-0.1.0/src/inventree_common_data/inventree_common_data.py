"""Selection Data for common use cases."""

from plugin import InvenTreePlugin

# from plugin.mixins import SettingsMixin
# from django.utils.translation import gettext_lazy as _


class InvenTreeCommonDataPlugin(InvenTreePlugin):
    """Selection Data for common use cases."""

    NAME = "InvenTree Common Data"
    SLUG = "inventree_common_data"

    def your_function_here(self):
        """Do something."""
        pass
