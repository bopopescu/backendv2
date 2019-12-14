
from django.conf.urls import include, url
from rest_framework import routers


from .views import UserViewSet, CollectiveViewSet, MembersOfCollectiveViewSet, LoginViewSet, UserPartialUpdateView,\
    TelegramViewSet, PlanViewSet, EventViewSet

# Создаем router и регистрируем наш ViewSet
router = routers.DefaultRouter()
router.register(r'users', viewset=UserViewSet)
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
    url(r'^users/partly/groupupd/', UserPartialUpdateView.group_points_update, name='group_points_update'),
    url(r'^collective/new/', CollectiveViewSet.new_collective, name='new_collective'),
    url(r'^collectives2/my/', CollectiveViewSet.my_collectives, name='my_collectives'),
    url(r'^telegram/', TelegramViewSet.printer, name='printer'),
    url(r'^plan/new/', PlanViewSet.create, name='create'),
    url(r'^plan/all', PlanViewSet.all, name='all'),
    url(r'^plan/(\d+)/(\d+)/(\d+)/$', PlanViewSet.get_session_by_day, name='qq'),
    url(r'^plan/(?P<pk>\d+)/$', PlanViewSet.get_session_by_id, name='qq'),
    url(r'^plan/update/', PlanViewSet.update_plan, name='qq'),
    url(r'^event/all', EventViewSet.all, name='all'),
    url(r'^event/new/', EventViewSet.create, name='create'),
]