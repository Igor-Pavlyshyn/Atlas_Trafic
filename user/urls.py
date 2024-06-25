from django.urls import path
from Atlas_Trafic_API.user.views import CreateUserView, CreateTokenView, DeleteTokenView, ManageUserView

app_name = "user"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CreateTokenView.as_view(), name="login"),
    path("logout/", DeleteTokenView.as_view(), name="logout"),
    path("me/", ManageUserView.as_view(), name="manage"),
]
