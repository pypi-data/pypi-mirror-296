import pytest

from django.test import Client
from django.urls import reverse

from tests.factory import create_product_with_variants


def test_exception_if_debug_is_false(client):
    with pytest.raises(Exception) as error:
        client.get(reverse("endpoint"))

    assert "can only be initialized if DEBUG is True." in str(error)


def test_request_timer_config_enabled(client, settings, capsys):
    settings.DEBUG = True
    setattr(settings, "GAJO_UTILS_CONFIG", {"REQUEST_TIMER": True})

    client.get(reverse("endpoint"))

    assert "Request actual time" in capsys.readouterr().out


def test_request_delay_config_enabled(client, settings, capsys):
    settings.DEBUG = True
    setattr(settings, "GAJO_UTILS_CONFIG", {"REQUEST_DELAY": True})

    client.get(reverse("endpoint"))

    assert "Request delay time" in capsys.readouterr().out


def test_request_cookies_config_enabled(client: Client, settings, capsys):
    settings.DEBUG = True
    setattr(settings, "GAJO_UTILS_CONFIG", {"REQUEST_COOKIES": True})

    client.cookies["cookie"] = "cookie_value"
    client.get(reverse("endpoint"))

    out = capsys.readouterr().out

    assert "Request cookies" in out
    assert "cookie_value" in out


def test_response_cookies_config_enabled(client: Client, settings, capsys):
    settings.DEBUG = True
    setattr(settings, "GAJO_UTILS_CONFIG", {"RESPONSE_COOKIES": True})

    client.get(reverse("endpoint_with_cookies"))

    out = capsys.readouterr().out

    assert "Response cookies" in out
    assert "cookie_value" in out


def test_response_content_config_enabled(client: Client, settings, capsys):
    settings.DEBUG = True
    setattr(settings, "GAJO_UTILS_CONFIG", {"RESPONSE_CONTENT": True})

    res = client.get(reverse("endpoint_with_content"))

    assert "simple content" in str(res.content)
    assert "simple content" in capsys.readouterr().out


def test_response_queries_config_enabled_response_without_queries(
    client, settings, capsys
):
    settings.DEBUG = True
    setattr(settings, "GAJO_UTILS_CONFIG", {"RESPONSE_QUERIES": True})

    client.get(reverse("endpoint_with_content"))

    out = capsys.readouterr().out

    assert "Response queries" in out
    assert "None" in out


@pytest.mark.django_db
def test_response_queries_config_enabled_print_query_statement(
    client, settings, capsys
):
    settings.DEBUG = True
    setattr(settings, "GAJO_UTILS_CONFIG", {"RESPONSE_QUERIES": True})

    client.get(reverse("endpoint_with_all_products_query"))

    assert "Query statement #1" in capsys.readouterr().out


@pytest.mark.django_db
def test_response_queries_config_enabled_print_unoptimized_similar_queries(
    client, settings, capsys
):
    settings.DEBUG = True
    setattr(settings, "GAJO_UTILS_CONFIG", {"RESPONSE_QUERIES": True})

    create_product_with_variants(num_of_variants=3)
    create_product_with_variants(num_of_variants=3)

    client.get(reverse("endpoint_with_all_products_query_without_prefetch"))

    assert "2 times" in capsys.readouterr().out


@pytest.mark.django_db
def test_response_queries_config_enabled_print_optimized_similar_queries(
    client, settings, capsys
):
    settings.DEBUG = True
    setattr(settings, "GAJO_UTILS_CONFIG", {"RESPONSE_QUERIES": True})

    create_product_with_variants(num_of_variants=3)
    create_product_with_variants(num_of_variants=3)

    client.get(reverse("endpoint_with_all_products_query_with_prefetch"))

    assert "{}" in capsys.readouterr().out
