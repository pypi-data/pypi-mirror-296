from django.urls import reverse


def test_timeit_decorator(client, settings, capsys):
    settings.DEBUG = True
    client.get(reverse("endpoint_with_timeview_decorator"))

    out = capsys.readouterr().out

    assert "Function time" in out
    assert "endpoint_with_timeview_decorator" in out
