"""Page Object Model for FSM automation"""

from .login_page import LoginPage
from .payables_page import PayablesPage
from .work_units_page import WorkUnitsPage

__all__ = [
    "LoginPage",
    "PayablesPage",
    "WorkUnitsPage",
]
