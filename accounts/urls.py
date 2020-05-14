from django.conf.urls import url
from .views import ThunesUserAccountAPI, ThunesTransactionAPI
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Account API')

urlpatterns = [
    url(r'^', ThunesUserAccountAPI.as_view(), name='account_create'),
    url(r'^/transactions/', ThunesTransactionAPI.as_view(), name='send_to_user'),
    url(r'^', schema_view)
]