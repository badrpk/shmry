from __future__ import annotations

from http.server import (
    BaseHTTPRequestHandler,
    ThreadingHTTPServer,
)
from pathlib import Path
from typing import Type

from shmry_platform.native_server import (
    NativePublisherServer,
    NativeResponse,
    NativeServeError,
)
from shmry_platform.publish import (
    PublishStore,
)


class ShmryNativeHandler(
    BaseHTTPRequestHandler
):
    server_version = "ShmryNative/1"

    def do_GET(self) -> None:
        resolver: NativePublisherServer = (
            self.server.resolver
        )

        host = self.headers.get(
            "Host",
            "",
        )

        try:
            response = resolver.dispatch(
                hostname=host,
                request_path=self.path,
            )
        except (
            NativeServeError,
            Exception,
        ) as exc:
            # Do not expose internal path/backend details.
            response = NativeResponse(
                status=404,
                headers={
                    "content-type": (
                        "text/plain; charset=utf-8"
                    ),
                    "cache-control": (
                        "no-store"
                    ),
                },
                body=b"Not Found\n",
            )

        self.send_response(
            response.status
        )

        for key, value in (
            response.headers.items()
        ):
            self.send_header(
                key,
                value,
            )

        self.end_headers()

        if response.body:
            self.wfile.write(
                response.body
            )

    def log_message(
        self,
        format: str,
        *args,
    ) -> None:
        # Keep Phase 2 deterministic and avoid
        # leaking request metadata in tests.
        return


class ShmryNativeHTTPServer(
    ThreadingHTTPServer
):
    daemon_threads = True

    def __init__(
        self,
        address,
        resolver: NativePublisherServer,
    ):
        super().__init__(
            address,
            ShmryNativeHandler,
        )
        self.resolver = resolver


def build_server(
    root: Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8088,
) -> ShmryNativeHTTPServer:
    store = PublishStore(
        root
    )

    resolver = NativePublisherServer(
        store
    )

    return ShmryNativeHTTPServer(
        (host, port),
        resolver,
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "Run Shmry native HTTP origin"
        )
    )

    parser.add_argument(
        "--root",
        required=True,
    )

    parser.add_argument(
        "--host",
        default="127.0.0.1",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8088,
    )

    args = parser.parse_args()

    server = build_server(
        Path(args.root),
        host=args.host,
        port=args.port,
    )

    print(
        f"Shmry native origin "
        f"http://{args.host}:{args.port}"
    )

    server.serve_forever()


if __name__ == "__main__":
    main()
