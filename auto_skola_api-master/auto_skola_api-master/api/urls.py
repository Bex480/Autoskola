from django.urls import re_path as url

from api.admin.views.registration import CreateUserView
from api.admin.views.update_user import UpdateUserView
from api.users.views.user import CurrentUserView
from api.views.registration import ActivateAccountView
from api.views.health import HealthCheckView
from api.views.auth import AuthenticationView


urlpatterns = [
    # Auth
    url(r"^auth/login/?$", AuthenticationView.as_view(), name="auth"),
    url(r"^auth/activate/(?P<token>\w{0,32})/?$", ActivateAccountView.as_view(), name="activate_account"),

    url(r"^health/?$", HealthCheckView.as_view(), name='health_check'),

    # Admin Endpoints
    url(r"^admin/registration/?$", CreateUserView.as_view(), name="admin_account_create"),
    url(r"^admin/user/(?P<pk>[0-9]+)/?$", UpdateUserView.as_view(), name="admin_update_user"),

    # new endpoints -------------------------------------------------------------------------------
    url(r"^user/current?$", CurrentUserView.as_view(), name="current"),
]
