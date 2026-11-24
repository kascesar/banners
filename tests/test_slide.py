"""Tests for `Slide`: rendering through the template and standalone content elements."""

import ssl
from pathlib import Path

import pytest

import banners
from banners import Background, Slide, Text, configure
from banners.content import AnimatedGraph, Graph
from banners.slides import Cover


def test_default_template_without_configure():
    """With no template configured, slides render on the default 16:9 canvas."""
    configure(template=None)
    assert "aspect-ratio:16/9" in Cover(title="A").render().text


def test_display_returns_render():
    """`_display_` shows the same canvas as `render()`."""
    slide = Cover(title="A")
    assert slide._display_().text == slide.render().text


def test_content_elements_render_without_configure():
    """Content elements render in a plain cell, with no slide or configuration."""
    assert Text("**a**").render() is not None
    assert Graph("graph LR\n A-->B").render() is not None
    assert AnimatedGraph("graph LR\n A-->B").render() is not None


def test_content_elements_do_not_import_config():
    """No file in `banners/content/` imports slides or `banners.config`."""
    content_dir = Path(banners.__file__).parent / "content"
    for path in content_dir.glob("*.py"):
        source = path.read_text()
        assert "from .." not in source, path.name
        assert "banners.config" not in source, path.name


class _FakeResponse:
    """Minimal stand-in for the response of `urllib.request.urlopen`."""

    def __init__(self) -> None:
        """Set the response headers."""
        self.headers = {"Content-Type": "image/svg+xml"}

    def __enter__(self):
        """Enter the `with` block.

        Returns:
            The response itself.
        """
        return self

    def __exit__(self, *exc):
        """Leave the `with` block without handling exceptions.

        Args:
            *exc: Exception type, value and traceback, if any.

        Returns:
            `False`, so exceptions propagate.
        """
        return False

    def read(self) -> bytes:
        """Return the downloaded bytes.

        Returns:
            A tiny SVG document.
        """
        return b"<svg/>"


def test_icon_src_verifies_tls(monkeypatch):
    """Images downloaded by URL verify the certificate and the host name."""
    seen = {}

    def fake_urlopen(req, timeout, context):
        seen["context"] = context
        return _FakeResponse()

    monkeypatch.setattr("banners.slide.urllib.request.urlopen", fake_urlopen)
    Slide._icon_src("https://example.org/logo.svg")
    assert seen["context"].verify_mode == ssl.CERT_REQUIRED
    assert seen["context"].check_hostname is True


def test_background_image_with_bad_certificate_raises(monkeypatch):
    """`Background.image(url)` fails when the certificate cannot be verified."""

    def fake_urlopen(req, timeout, context):
        if context.verify_mode == ssl.CERT_REQUIRED:
            raise ssl.SSLCertVerificationError("certificate verify failed")
        return _FakeResponse()

    monkeypatch.setattr("banners.slide.urllib.request.urlopen", fake_urlopen)
    with pytest.raises(ssl.SSLCertVerificationError):
        Background.image("https://bad.example/photo.jpg")
