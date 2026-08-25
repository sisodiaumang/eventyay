import datetime
import pytest
from django.utils.timezone import now

from eventyay.base.models.auth import ShortToken


@pytest.mark.django_db
class TestKioskShortTokenLogin:
    def test_valid_short_token_redirects_to_video_spa_on_main_domain(self, client, event):
        exp = now() + datetime.timedelta(days=30)
        st = ShortToken.objects.create(
            event=event,
            short_token="testKioskToken123",
            long_token="jwt.long.kiosk.token.payload",
            expires=exp,
        )

        response = client.get(f"/login/{st.short_token}")
        assert response.status_code == 302
        assert response.url == f"/{event.organizer.slug}/{event.slug}/video/#token={st.long_token}"

    def test_valid_short_token_with_trailing_slash(self, client, event):
        exp = now() + datetime.timedelta(days=30)
        st = ShortToken.objects.create(
            event=event,
            short_token="testKioskTokenSlash",
            long_token="jwt.long.kiosk.token.payload.slash",
            expires=exp,
        )

        response = client.get(f"/login/{st.short_token}/")
        assert response.status_code == 302
        assert response.url == f"/{event.organizer.slug}/{event.slug}/video/#token={st.long_token}"

    def test_valid_short_token_redirects_to_custom_domain_if_configured(self, client, event):
        event.domain = "kiosk.eventdomain.example.com"
        event.save()

        exp = now() + datetime.timedelta(days=30)
        st = ShortToken.objects.create(
            event=event,
            short_token="customDomainToken",
            long_token="jwt.custom.domain.payload",
            expires=exp,
        )

        response = client.get(f"/login/{st.short_token}")
        assert response.status_code == 302
        assert response.url == f"http://kiosk.eventdomain.example.com/#token={st.long_token}"

    def test_invalid_short_token_returns_404(self, client):
        response = client.get("/login/nonExistentToken123")
        assert response.status_code == 404
        assert "Unknown access token" in response.content.decode("utf-8")

    def test_expired_short_token_returns_410(self, client, event):
        exp = now() - datetime.timedelta(days=1)
        st = ShortToken.objects.create(
            event=event,
            short_token="expiredToken123",
            long_token="jwt.expired.token.payload",
            expires=exp,
        )

        response = client.get(f"/login/{st.short_token}")
        assert response.status_code == 410
        assert "expired" in response.content.decode("utf-8")
