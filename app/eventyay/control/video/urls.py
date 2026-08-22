from django.urls import include, path
from django.views.generic import RedirectView
from eventyay.control.views import admin_views as views

urlpatterns = [
    # Authentication URLs
    path("auth/profile/", views.ProfileView.as_view(), name="auth.profile"),
    path("auth/signup", views.SignupView.as_view(), name="auth.signup"),
    # User Management URLs
    path("users/", views.UserList.as_view(), name="user.list"),
    path("users/<int:pk>/", views.UserUpdate.as_view(), name="user.update"),
    # Video Settings URL
    path("settings/", views.VideoSettingsView.as_view(), name="settings"),
    # Redirect old server list URLs to Video Settings with section anchor
    path("bbbs/", RedirectView.as_view(url="/admin/video/settings/#bbb", permanent=False), name="bbbserver.list"),
    path("janus/", RedirectView.as_view(url="/admin/video/settings/#janus", permanent=False), name="janusserver.list"),
    path("jitsi/", RedirectView.as_view(url="/admin/video/settings/#jitsi", permanent=False), name="jitsiserver.list"),
    path("turns/", RedirectView.as_view(url="/admin/video/settings/#turn", permanent=False), name="turnserver.list"),
    path("streamingservers/", RedirectView.as_view(url="/admin/video/settings/#streaming", permanent=False), name="streamingserver.list"),
    # BBB Server Management URLs
    path("bbbs/moveroom/", views.BBBMoveRoom.as_view(), name="bbbserver.moveroom"),
    path("bbbs/new/", views.BBBServerCreate.as_view(), name="bbbserver.create"),
    path("bbbs/<uuid:pk>/delete", views.BBBServerDelete.as_view(), name="bbbserver.delete"),
    path("bbbs/<uuid:pk>/", views.BBBServerUpdate.as_view(), name="bbbserver.update"),
    # Janus Server Management URLs
    path("janus/new/", views.JanusServerCreate.as_view(), name="janusserver.create"),
    path("janus/<uuid:pk>/delete", views.JanusServerDelete.as_view(), name="janusserver.delete"),
    path("janus/<uuid:pk>/", views.JanusServerUpdate.as_view(), name="janusserver.update"),
    # Jitsi Server Management URLs
    path("jitsi/new/", views.JitsiServerCreate.as_view(), name="jitsiserver.create"),
    path("jitsi/<uuid:pk>/delete", views.JitsiServerDelete.as_view(), name="jitsiserver.delete"),
    path("jitsi/<uuid:pk>/", views.JitsiServerUpdate.as_view(), name="jitsiserver.update"),
    # Turn Server Management URLs
    path("turns/new/", views.TurnServerCreate.as_view(), name="turnserver.create"),
    path("turns/<uuid:pk>/delete", views.TurnServerDelete.as_view(), name="turnserver.delete"),
    path("turnservers/<uuid:pk>/", views.TurnServerUpdate.as_view(), name="turnserver.update"),
    # Streaming Server Management URLs
    path("streamkey/", views.StreamkeyGenerator.as_view(), name="streamkey"),
    path("streamingservers/new/", views.StreamingServerCreate.as_view(), name="streamingserver.create"),
    path("streamingservers/<uuid:pk>/delete", views.StreamingServerDelete.as_view(), name="streamingserver.delete"),
    path("streamingservers/<uuid:pk>/", views.StreamingServerUpdate.as_view(), name="streamingserver.update"),
    # Event Management URLs
    path("events/", views.EventList.as_view(), name="event.list"),
    path("events/new/", views.EventCreate.as_view(), name="event.create"),
    path("events/calendar", views.EventCalendar.as_view(), name="event.calendar"),
    path("events/<slug:pk>/admin", views.EventAdminToken.as_view(), name="event.admin"),
    path("events/<slug:pk>/clear", views.EventClear.as_view(), name="event.clear"),
    path("events/<slug:pk>/", views.EventUpdate.as_view(), name="event.update"),
    # SystemLog Management URLs
    path("systemlog/", views.SystemLogList.as_view(), name="systemlog.list"),
    path("systemlog/<uuid:pk>/", views.SystemLogDetail.as_view(), name="systemlog.detail"),
    # Default index view -> VideoSettingsView
    path("", views.VideoSettingsView.as_view(), name="index"),
]
