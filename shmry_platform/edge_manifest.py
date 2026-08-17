from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from shmry_platform.publish import (
    Project,
    PublishError,
    PublishStore,
    Release,
)


class EdgeManifestError(RuntimeError):
    pass


@dataclass(frozen=True)
class EdgeRoute:
    schema: int
    route_id: str
    hostname: str
    project_id: str
    release_id: str
    route_type: str
    origin: str
    health_path: str | None = None

    def __post_init__(self) -> None:
        if self.schema != 1:
            raise EdgeManifestError(
                "unsupported route schema"
            )

        if self.route_type not in {
            "shmry_native",
            "reverse_proxy",
        }:
            raise EdgeManifestError(
                "unsupported route_type"
            )

        if not self.hostname.endswith(
            ".shmry.com"
        ):
            raise EdgeManifestError(
                "route hostname must be Shmry-owned"
            )

        if self.route_type == "shmry_native":
            if not self.origin.startswith(
                "http://127.0.0.1:"
            ):
                raise EdgeManifestError(
                    "native origin must be loopback HTTP"
                )

        if self.route_type == "reverse_proxy":
            if not self.origin.startswith(
                (
                    "http://127.0.0.1:",
                    "http://localhost:",
                )
            ):
                raise EdgeManifestError(
                    "service origin must be local/internal"
                )


@dataclass(frozen=True)
class EdgeSnapshot:
    schema: int
    generation: int
    routes: tuple[EdgeRoute, ...]
    manifest_sha256: str

    def payload_without_digest(
        self,
    ) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "generation": self.generation,
            "routes": [
                asdict(route)
                for route in self.routes
            ],
        }


def canonical_json(
    payload: Any,
) -> str:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def digest_payload(
    payload: Any,
) -> str:
    return sha256(
        canonical_json(
            payload
        ).encode("utf-8")
    ).hexdigest()


class EdgeManifestManager:
    def __init__(
        self,
        store: PublishStore,
        *,
        native_origin: str = "http://127.0.0.1:8088",
    ) -> None:
        if not native_origin.startswith(
            "http://127.0.0.1:"
        ):
            raise EdgeManifestError(
                "native_origin must use 127.0.0.1"
            )

        self.store = store
        self.native_origin = (
            native_origin.rstrip("/")
        )

        self.edge_dir = (
            store.root / "edge"
        )
        self.snapshots_dir = (
            self.edge_dir / "snapshots"
        )
        self.active_path = (
            self.edge_dir / "active.json"
        )

        self.snapshots_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _projects(
        self,
    ) -> list[Project]:
        projects: list[Project] = []

        for record in sorted(
            self.store.projects_dir.glob(
                "*.json"
            )
        ):
            projects.append(
                Project(
                    **self.store._read_json(
                        record
                    )
                )
            )

        return projects

    def _release(
        self,
        project: Project,
    ) -> Release | None:
        if not project.active_release_id:
            return None

        release = self.store.get_release(
            project.active_release_id
        )

        if (
            release.project_id
            != project.project_id
        ):
            raise EdgeManifestError(
                "active release mismatch"
            )

        return release

    def build_routes(
        self,
    ) -> tuple[EdgeRoute, ...]:
        routes: list[EdgeRoute] = []
        hostnames: set[str] = set()

        for project in self._projects():
            if project.visibility != "public":
                continue

            release = self._release(
                project
            )

            if release is None:
                continue

            hostname = (
                project.hostname.lower()
            )

            if hostname in hostnames:
                raise EdgeManifestError(
                    "duplicate hostname"
                )

            hostnames.add(hostname)

            if (
                release.artifact_type
                in {
                    "static_site",
                    "download",
                }
            ):
                routes.append(
                    EdgeRoute(
                        schema=1,
                        route_id=(
                            f"edge-{release.release_id}"
                        ),
                        hostname=hostname,
                        project_id=(
                            project.project_id
                        ),
                        release_id=(
                            release.release_id
                        ),
                        route_type=(
                            "shmry_native"
                        ),
                        origin=(
                            self.native_origin
                        ),
                    )
                )
                continue

            if (
                release.artifact_type
                == "web_service"
            ):
                route_file = (
                    self.store.routes_dir
                    / (
                        "route-"
                        + release.release_id
                        + ".json"
                    )
                )

                route_payload = (
                    self.store._read_json(
                        route_file
                    )
                )

                target = str(
                    route_payload.get(
                        "target",
                        "",
                    )
                )

                health_path = (
                    route_payload.get(
                        "health_path"
                    )
                )

                routes.append(
                    EdgeRoute(
                        schema=1,
                        route_id=(
                            f"edge-{release.release_id}"
                        ),
                        hostname=hostname,
                        project_id=(
                            project.project_id
                        ),
                        release_id=(
                            release.release_id
                        ),
                        route_type=(
                            "reverse_proxy"
                        ),
                        origin=target,
                        health_path=(
                            str(health_path)
                            if health_path
                            else None
                        ),
                    )
                )
                continue

            raise EdgeManifestError(
                "unsupported active release type"
            )

        return tuple(
            sorted(
                routes,
                key=lambda route: (
                    route.hostname,
                    route.route_id,
                ),
            )
        )

    def _next_generation(
        self,
    ) -> int:
        if not self.active_path.is_file():
            return 1

        current = json.loads(
            self.active_path.read_text(
                encoding="utf-8"
            )
        )

        return int(
            current.get(
                "generation",
                0,
            )
        ) + 1

    def build_snapshot(
        self,
    ) -> EdgeSnapshot:
        generation = (
            self._next_generation()
        )
        routes = self.build_routes()

        base = {
            "schema": 1,
            "generation": generation,
            "routes": [
                asdict(route)
                for route in routes
            ],
        }

        digest = digest_payload(
            base
        )

        return EdgeSnapshot(
            schema=1,
            generation=generation,
            routes=routes,
            manifest_sha256=digest,
        )

    @staticmethod
    def validate_snapshot_payload(
        payload: dict[str, Any],
    ) -> None:
        if payload.get("schema") != 1:
            raise EdgeManifestError(
                "invalid snapshot schema"
            )

        if not isinstance(
            payload.get("generation"),
            int,
        ):
            raise EdgeManifestError(
                "generation must be integer"
            )

        raw_routes = payload.get(
            "routes"
        )

        if not isinstance(
            raw_routes,
            list,
        ):
            raise EdgeManifestError(
                "routes must be a list"
            )

        seen_hostnames: set[str] = set()

        for raw in raw_routes:
            route = EdgeRoute(
                **raw
            )

            if (
                route.hostname
                in seen_hostnames
            ):
                raise EdgeManifestError(
                    "duplicate route hostname"
                )

            seen_hostnames.add(
                route.hostname
            )

        expected = payload.get(
            "manifest_sha256"
        )

        if not isinstance(
            expected,
            str,
        ):
            raise EdgeManifestError(
                "manifest_sha256 missing"
            )

        canonical_payload = {
            "schema": payload["schema"],
            "generation": (
                payload["generation"]
            ),
            "routes": raw_routes,
        }

        actual = digest_payload(
            canonical_payload
        )

        if actual != expected:
            raise EdgeManifestError(
                "manifest digest mismatch"
            )

    def write_snapshot(
        self,
        snapshot: EdgeSnapshot,
    ) -> Path:
        payload = {
            **snapshot.payload_without_digest(),
            "manifest_sha256": (
                snapshot.manifest_sha256
            ),
        }

        self.validate_snapshot_payload(
            payload
        )

        path = (
            self.snapshots_dir
            / (
                f"{snapshot.generation:020d}-"
                f"{snapshot.manifest_sha256}.json"
            )
        )

        if path.exists():
            existing = json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )

            if existing != payload:
                raise EdgeManifestError(
                    "immutable snapshot conflict"
                )

            return path

        temp = path.with_suffix(
            ".json.tmp"
        )

        temp.write_text(
            json.dumps(
                payload,
                sort_keys=True,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        temp.replace(path)

        return path

    def activate_snapshot(
        self,
        snapshot_path: Path,
    ) -> dict[str, Any]:
        payload = json.loads(
            snapshot_path.read_text(
                encoding="utf-8"
            )
        )

        self.validate_snapshot_payload(
            payload
        )

        temp = self.active_path.with_suffix(
            ".json.tmp"
        )

        temp.write_text(
            json.dumps(
                payload,
                sort_keys=True,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        temp.replace(
            self.active_path
        )

        return payload

    def publish_snapshot(
        self,
    ) -> dict[str, Any]:
        snapshot = (
            self.build_snapshot()
        )

        path = self.write_snapshot(
            snapshot
        )

        return self.activate_snapshot(
            path
        )
