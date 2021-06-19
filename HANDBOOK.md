# Handbook for mqttwarn-contrib

  * [Notification services](#notification-services)


## Notification services

* [cloudflare_zone](#cloudflare_zone)


### `cloudflare_zone`


#### Introduction

The `cloudflare_zone` service can update Cloudflare A record DNS entries with
your current IP address. It works well with the function
`publish_public_ip_address` in `samplefuncs.py` where the payload is an IP
address. It acts as a kind of a replacement to DynDNS or No-ip services.

Originally, this code has been published at https://github.com/jpmens/mqttwarn/pull/370.
Thanks, David!


#### Configuration

This section refers to the configuration snippet for the mqttwarn configuration
file `mqttwarn.ini`.

`auth-email` is a cloudflare login address with its `auth-key` (api key)
used for authenticating with the cloudflare API.

In the `targets` section, a `<zone id>` is the ID of one of your domains. You
can find the ID on the bottom right of a domain overview page in the API
section listed as "Zone ID".

Using the special name of `all` for a zone will update all A records for that
domain to the respective IP address. Otherwise, set the parm 2 of a target to
the full FQDN of the A record + domain. For example, A record `WWW` for domain
`mydomain.com` for the example `www2` target above.

Or you can obtain the record via `curl` command:
```
 curl -X GET "https://api.cloudflare.com/client/v4/zones/<zone id>/dns_records?type=A&page=1&per_page=20&order=type&direction=desc&match=all" -H "X-Auth-Email: <auth-email>"  -H "X-Auth-key: <auth-key>"  -H "Content-Type: application/json"
```

For the resulting JSON, you want the "id" field of the result entry.

In the configuration above, when a new IP address is posted to
`mqttwarn/ip/<server>`, it will fire off the cloudflare service to update `all`
of the A records for the zone and then the `www2` A record for zone id
`12345657891234`.


#### Example configuration snippets

```ini
[defaults]
functions = 'samplefuncs.py'

[cron]
publish_public_ip_address = 60; now=true

[config:cloudflare_zone]
auth-email  = '<your cloudflare@email.address>'
auth-key    = '<your cloudflare api key>'
targets = {
    'all': ['<zone id>','all'],
    'www': ['<zone id>','<full domain name>',''],
    'www2': ['12345657891234','www.mydomain.com',''],
    'vpn': ['12345657891234','','12345613247']
  }

[dyndns/ip/#]
targets = cloudflare_zone:all, cloudflare_zone:www2
```

```python
def publish_public_ip_address(srv=None):
    """
    Custom function used as a periodic task for publishing your public ip address to the MQTT bus.
    Obtains service object.
    Returns None.
    """

    import socket
    import requests

    hostname = socket.gethostname()
    ip_address = requests.get('https://httpbin.org/ip').json().get('origin')

    if srv is not None:

        # optional debug logger
        srv.logging.debug('Publishing public ip address "{ip_address}" of host "{hostname}"'.format(**locals()))

        # publish ip address to mqtt
        srv.mqttc.publish('dyndns/ip/{hostname}'.format(**locals()), ip_address)
```
