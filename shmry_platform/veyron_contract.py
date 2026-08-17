from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from shmry_platform.edge_manifest import (
    EdgeManifestError,
    EdgeManifestManager,
    EdgeRoute,
)


class VeyronContractError(RuntimeError):
    pass


def load_veyron_routes(
    manifest_path: Path,
) -> tuple[EdgeRoute, ...]:
    payload: dict[str, Any] = json.loads(
        manifest_path.read_text(
            encoding="utf-8"
        )
    )

    EdgeManifestManager.validate_snapshot_payload(
        payload
    )

    routes = tuple(
        EdgeRoute(
            **raw
        )
        for raw in payload["routes"]
    )

    return routes


def export_veyron_route_registry(
    manifest_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    routes = load_veyron_routes(
        manifest_path
    )

    output = {
        "schema": 1,
        "routes": [
            {
                "hostname": route.hostname,
                "backend": route.origin,
                "mode": (
                    "proxy"
                    if route.route_type
                    == "reverse_proxy"
                    else "shmry-origin"
                ),
                "project_id": (
                    route.project_id
                ),
                "release_id": (
                    route.release_id
                ),
                "health_path": (
                    route.health_path
                ),
            }
            for route in routes
        ],
    }

    temp = output_path.with_suffix(
        output_path.suffix + ".tmp"
    )

    temp.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temp.write_text(
        json.dumps(
            output,
            sort_keys=True,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    temp.replace(
        output_path
    )

    return output
