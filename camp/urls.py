
from django.conf.urls import include, url
from rest_framework import routers


from .views import UserViewSet, CollectiveViewSet, MembersOfCollectiveViewSet, LoginViewSet, UserPartialUpdateView

# Создаем router и регистрируем наш ViewSet
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'collectives', CollectiveViewSet)
router.register(r'membersofcollective', MembersOfCollectiveViewSet)
router.register(r'login', LoginViewSet)
# router.register(r'profile', ProfileViewset)
# URLs настраиваются автоматически роутером
# urlpatterns = router.urls
urlpatterns = [
    # url(r'^auth', views.auth),
    url(r'^', include(router.urls)),
    url(r'^users/partly/(?P<pk>\d+)/$', UserPartialUpdateView.as_view(), name='user_partial_update'),
    url(r'^^users/partly/groupupd/', UserPartialUpdateView.group_points_update, name='group_points_update')
]