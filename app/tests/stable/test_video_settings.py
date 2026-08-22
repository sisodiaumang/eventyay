import pytest
from django.urls import resolve, reverse

from eventyay.base.models import (
    BBBServer,
    JanusServer,
    JitsiServer,
    StreamingServer,
    TurnServer,
)
from eventyay.base.models.auth import StaffSession
from eventyay.control.navigation import get_admin_navigation


@pytest.mark.django_db
class TestVideoSettings:
    def test_video_settings_requires_staff(self, client):
        response = client.get(reverse("eventyay_admin:video_admin:settings"))
        assert response.status_code in [302, 403]

    def test_video_settings_accessible_for_staff(self, staff_client, staff_user):
        StaffSession.objects.create(
            user=staff_user,
            session_key=staff_client.session.session_key,
        )
        bbb = BBBServer.objects.create(url="https://bbb.example.com/bigbluebutton/", secret="bbb-secret")
        jitsi = JitsiServer.objects.create(url="https://jitsi.example.com", app_id="test_app", app_secret="secret")
        janus = JanusServer.objects.create(url="https://janus.example.com")
        turn = TurnServer.objects.create(hostname="turn.example.com", auth_secret="turn-secret")
        streaming = StreamingServer.objects.create(name="Stream Server 1", token_secret="secret123")

        response = staff_client.get(reverse("eventyay_admin:video_admin:settings"))
        assert response.status_code == 200
        content = response.content.decode("utf-8")
        assert "Video settings" in content
        assert "Server configurations" in content
        assert bbb.url in content
        assert jitsi.url in content
        assert janus.url in content
        assert turn.hostname in content
        assert streaming.name in content

    def test_old_server_list_urls_redirect(self, staff_client, staff_user):
        StaffSession.objects.create(
            user=staff_user,
            session_key=staff_client.session.session_key,
        )
        for url_name, expected_hash in [
            ("bbbserver.list", "/admin/video/settings/#bbb"),
            ("janusserver.list", "/admin/video/settings/#janus"),
            ("jitsiserver.list", "/admin/video/settings/#jitsi"),
            ("turnserver.list", "/admin/video/settings/#turn"),
            ("streamingserver.list", "/admin/video/settings/#streaming"),
        ]:
            response = staff_client.get(reverse(f"eventyay_admin:video_admin:{url_name}"))
            assert response.status_code == 302
            assert response.url == expected_hash

    def test_navigation_structure(self, rf, staff_user):
        url_path = reverse("eventyay_admin:video_admin:settings")
        request = rf.get(url_path)
        request.resolver_match = resolve(url_path)
        request.user = staff_user
        nav = get_admin_navigation(request)
        video_nav = next((item for item in nav if str(item["label"]) == "Video Admin"), None)
        assert video_nav is not None

        labels = [str(child["label"]) for child in video_nav["children"]]
        assert "Video settings" in labels
        assert "Dashboard" not in labels
        assert "BBB servers" not in labels
        assert "Janus servers" not in labels
        assert "Jitsi servers" not in labels
        assert "TURN servers" not in labels
        assert "Streaming servers" not in labels
