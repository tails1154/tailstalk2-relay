#!/usr/bin/env python3
"""Plain-TCP to TLS relay for the TailsTalk 2 PS4 build.

The PS4 SDK's SSL header has no usable raw-socket API, so the console speaks
plain websocket to this relay on the LAN, and the relay forwards the bytes to
the events service over TLS. The relay does not read or change the traffic.

Run on a machine on the same LAN as the console:
    python3 tools/ws_relay.py --listen 0.0.0.0:9963

Anything that reaches the relay port can talk to the events service, so only
run it on a trusted network.
"""

import argparse
import asyncio
import ssl

UPSTREAM_HOST = "tails1154.com"
UPSTREAM_PORT = 9961


async def pipe(reader, writer):
    try:
        while True:
            data = await reader.read(65536)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except (ConnectionError, OSError):
        pass
    finally:
        try:
            writer.close()
        except OSError:
            pass


async def handle(client_reader, client_writer):
    try:
        upstream_reader, upstream_writer = await asyncio.open_connection(
            UPSTREAM_HOST,
            UPSTREAM_PORT,
            ssl=ssl.create_default_context(),
            server_hostname=UPSTREAM_HOST,
        )
    except OSError:
        client_writer.close()
        return
    await asyncio.gather(
        pipe(client_reader, upstream_writer),
        pipe(upstream_reader, client_writer),
    )


async def main(host, port):
    server = await asyncio.start_server(handle, host, port)
    print(f"ws relay listening on {host}:{port} -> wss://{UPSTREAM_HOST}:{UPSTREAM_PORT}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--listen", default="0.0.0.0:9963")
    args = parser.parse_args()
    host, _, port = args.listen.rpartition(":")
    asyncio.run(main(host or "0.0.0.0", int(port)))
