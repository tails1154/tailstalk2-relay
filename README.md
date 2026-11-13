# tailstalk2-relay

A plain-TCP to TLS relay for the TailsTalk 2 PS4 build.

The PS4 SDK's SSL header has no usable raw-socket API, so the console speaks plain websocket to this relay and the relay forwards the bytes to the TailsTalk 2 events service over TLS. The relay does not read or change the traffic.

## Run

```sh
python3 ws_relay.py --listen 0.0.0.0:9963
```

or with Docker:

```sh
docker build -t tailstalk2-relay .
docker run --rm -p 9963:9963 tailstalk2-relay
```

The upstream is `wss://tails1154.com:9961/ws`, set in `ws_relay.py` (`UPSTREAM_HOST` and `UPSTREAM_PORT`).

## Security

Traffic between the console and the relay is plain text, so the session token and anything else sent to the events service crosses your LAN unencrypted. Only run the relay on a network you trust. Anyone who can reach the relay port can use it to reach the events service.

## Licence

AGPL-3.0-or-later, the same as the TailsTalk 2 backend.
