import logging

import responses

from mqttwarn.util import load_module_from_file
from tests.util import ProcessorItem as Item


def add_successful_mock_response():
    responses.add(
        responses.GET,
        "https://api.cloudflare.com/client/v4/zones/0815/dns_records?type=A&name=www.example.org",
        json={"success": True, "result": {"id": "0815", "type": "A", "content": "192.168.0.1", "name": "www.example.org"}},
        status=200,
    )
    responses.add(
        responses.PUT,
        "https://api.cloudflare.com/client/v4/zones/0815/dns_records/0815",
        json={"success": True},
        status=200,
    )


@responses.activate
def test_cloudflare_zone_success(srv, caplog):

    module = load_module_from_file("mqttwarn_contrib/services/cloudflare_zone.py")

    item = Item(
        config={"auth-email": "foo", "auth-key": "bar"},
        target="test",
        addrs=['0815', 'www.example.org', ''],
        message="192.168.0.2",
        data={},
    )

    with caplog.at_level(logging.DEBUG):

        add_successful_mock_response()
        outcome = module.plugin(srv, item)

        assert len(responses.calls) == 2

        # Verify first request to get record information.
        assert (
            responses.calls[0].request.url == "https://api.cloudflare.com/client/v4/zones/0815/dns_records?type=A&name=www.example.org"
        )
        assert (
            responses.calls[0].request.params
            == {'name': 'www.example.org', 'type': 'A'}
        )
        #assert responses.calls[0].request.headers["User-Agent"] == "mqttwarn"
        assert responses.calls[0].request.headers["X-Auth-Email"] == "foo"
        assert responses.calls[0].request.headers["X-Auth-Key"] == "bar"

        assert responses.calls[0].response.status_code == 200
        assert responses.calls[0].response.text == '{"success": true, "result": {"id": "0815", "type": "A", "content": "192.168.0.1", "name": "www.example.org"}}'

        # Verify second request to update record information.
        assert (
            responses.calls[1].request.url == "https://api.cloudflare.com/client/v4/zones/0815/dns_records/0815"
        )
        assert (
            responses.calls[1].request.body
            == b'{"type": "A", "content": "192.168.0.2", "name": "www.example.org", "ttl": 1, "proxied": true}'
        )
        #assert responses.calls[1].request.headers["User-Agent"] == "mqttwarn"
        assert responses.calls[1].request.headers["X-Auth-Email"] == "foo"
        assert responses.calls[1].request.headers["X-Auth-Key"] == "bar"

        assert responses.calls[1].response.status_code == 200
        assert responses.calls[1].response.text == '{"success": true}'

        # Verify log messages.
        assert outcome is True
        assert "IP address needs update for record: www.example.org from: 192.168.0.1 to: 192.168.0.2" in caplog.text
