from __future__ import annotations

from dataclasses import asdict, dataclass, field
from hashlib import sha256
import json
import mimetypes
from pathlib import Path
import re
import shutil
import time
from typing import Any


class PublishError(RuntimeError):
    pass


_SLUG = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")
_VERSION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$")


def validate_slug(value: str, *, field_name: str = "slug") -> str:
    value = value.strip().lower()

    if not _SLUG.fullmatch(value):
        raise PublishError(
            f"invalid {field_name}: use lowercase letters, numbers and hyphens"
        )

    return value


def validate_version(value: str) -> str:
    value = value.strip()

    if not _VERSION.fullmatch(value):
        raise PublishError("invalid version")

    return value


def sha256_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def _canonical(payload: Any) -> str:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


@dataclass(frozen=True)
class Project:
    project_id: str
    owner_id: str
    slug: str
    title: str
    artifact_type: str
    visibility: str
    hostname: str
    project_url: str
    created_at: int
    active_release_id: str | None = None

    def __post_init__(self) -> None:
        validate_slug(self.owner_id, field_name="owner_id")
        validate_slug(self.slug)

        if self.artifact_type not in {
            "static_site",
            "download",
            "web_service",
        }:
            raise PublishError("unsupported artifact_type")

        if self.visibility not in {"public", "private"}:
            raise PublishError("unsupported visibility")


@dataclass(frozen=True)
class Release:
    release_id: str
    project_id: str
    version: str
    artifact_sha256: str
    artifact_size: int
    artifact_type: str
    created_at: int
    status: str
    storage_key: str | None
    filename: str | None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        validate_version(self.version)

        if (
            len(self.artifact_sha256) != 64
            or any(
                c not in "0123456789abcdef"
                for c in self.artifact_sha256
            )
        ):
            raise PublishError("invalid artifact_sha256")

        if self.artifact_size < 0:
            raise PublishError("artifact_size cannot be negative")


@dataclass(frozen=True)
class RouteManifest:
    schema: int
    route_id: str
    hostname: str
    mode: str
    target: str
    project_id: str
    release_id: str
    health_path: str | None = None

    def __post_init__(self) -> None:
        if self.schema != 1:
            raise PublishError("unsupported route schema")

        if self.mode not in {
            "static",
            "reverse_proxy",
        }:
            raise PublishError("unsupported route mode")

        if (
            self.mode == "reverse_proxy"
            and not self.target.startswith(
                ("http://127.0.0.1:", "http://localhost:")
            )
        ):
            raise PublishError(
                "web-service backend must be local/internal in phase 1"
            )

    def public_dict(self) -> dict[str, Any]:
        payload = asdict(self)

        # Backend targets are control-plane data, not public project metadata.
        if self.mode == "reverse_proxy":
            payload["target"] = "internal"

        return payload


class PublishStore:
    """
    Durable local registry for Shmry Publish.

    Registry files are control-plane state. Immutable release payloads live
    below artifacts/<digest>/ and static releases below sites/<release_id>/.
    """

    def __init__(
        self,
        root: Path,
        *,
        base_domain: str = "shmry.com",
    ) -> None:
        self.root = root
        self.base_domain = base_domain.strip().lower()

        self.projects_dir = root / "projects"
        self.releases_dir = root / "releases"
        self.artifacts_dir = root / "artifacts"
        self.sites_dir = root / "sites"
        self.routes_dir = root / "routes"

        for directory in (
            self.projects_dir,
            self.releases_dir,
            self.artifacts_dir,
            self.sites_dir,
            self.routes_dir,
        ):
            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        if not path.is_file():
            raise PublishError(
                f"registry record not found: {path.name}"
            )

        return json.loads(
            path.read_text(encoding="utf-8")
        )

    @staticmethod
    def _write_atomic(
        path: Path,
        payload: dict[str, Any],
    ) -> None:
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        temp = path.with_suffix(
            path.suffix + ".tmp"
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

    def _project_path(
        self,
        project_id: str,
    ) -> Path:
        return (
            self.projects_dir
            / f"{project_id}.json"
        )

    def _release_path(
        self,
        release_id: str,
    ) -> Path:
        return (
            self.releases_dir
            / f"{release_id}.json"
        )

    def create_project(
        self,
        *,
        owner_id: str,
        slug: str,
        title: str,
        artifact_type: str,
        visibility: str = "public",
    ) -> Project:
        owner = validate_slug(
            owner_id,
            field_name="owner_id",
        )
        slug = validate_slug(slug)

        project_id = (
            f"proj-{owner}-{slug}"
        )

        path = self._project_path(
            project_id
        )

        if path.exists():
            raise PublishError(
                "project already exists"
            )

        hostname = (
            f"{slug}-{owner}."
            f"{self.base_domain}"
        )

        project_url = (
            f"https://{self.base_domain}"
            f"/@{owner}/{slug}"
        )

        project = Project(
            project_id=project_id,
            owner_id=owner,
            slug=slug,
            title=title.strip()
            or slug,
            artifact_type=artifact_type,
            visibility=visibility,
            hostname=hostname,
            project_url=project_url,
            created_at=int(time.time()),
        )

        self._write_atomic(
            path,
            asdict(project),
        )

        return project

    def get_project(
        self,
        project_id: str,
    ) -> Project:
        return Project(
            **self._read_json(
                self._project_path(
                    project_id
                )
            )
        )

    def get_release(
        self,
        release_id: str,
    ) -> Release:
        return Release(
            **self._read_json(
                self._release_path(
                    release_id
                )
            )
        )

    def _write_release(
        self,
        release: Release,
    ) -> None:
        path = self._release_path(
            release.release_id
        )

        if path.exists():
            existing = self._read_json(
                path
            )

            if existing != asdict(
                release
            ):
                raise PublishError(
                    "immutable release conflict"
                )

            return

        self._write_atomic(
            path,
            asdict(release),
        )

    def _release_id(
        self,
        project: Project,
        version: str,
        digest: str,
    ) -> str:
        seed = (
            f"{project.project_id}\n"
            f"{version}\n"
            f"{digest}"
        )

        return (
            "rel-"
            + sha256(
                seed.encode("utf-8")
            ).hexdigest()[:20]
        )

    def publish_download(
        self,
        project_id: str,
        source: Path,
        *,
        version: str,
        platform: str = "generic",
    ) -> Release:
        project = self.get_project(
            project_id
        )

        if project.artifact_type != "download":
            raise PublishError(
                "project is not a download project"
            )

        source = source.resolve()

        if not source.is_file():
            raise PublishError(
                "download source must be a file"
            )

        version = validate_version(
            version
        )

        data = source.read_bytes()
        digest = sha256_bytes(data)

        artifact_dir = (
            self.artifacts_dir
            / digest
        )

        artifact_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        safe_name = Path(
            source.name
        ).name

        destination = (
            artifact_dir
            / safe_name
        )

        if destination.exists():
            if (
                sha256_bytes(
                    destination.read_bytes()
                )
                != digest
            ):
                raise PublishError(
                    "immutable artifact conflict"
                )
        else:
            destination.write_bytes(data)

        release_id = self._release_id(
            project,
            version,
            digest,
        )

        release = Release(
            release_id=release_id,
            project_id=project.project_id,
            version=version,
            artifact_sha256=digest,
            artifact_size=len(data),
            artifact_type="download",
            created_at=int(time.time()),
            status="stored",
            storage_key=(
                f"artifacts/{digest}/"
                f"{safe_name}"
            ),
            filename=safe_name,
            metadata={
                "platform": platform,
                "content_type": (
                    mimetypes.guess_type(
                        safe_name
                    )[0]
                    or "application/octet-stream"
                ),
            },
        )

        self._write_release(
            release
        )

        return release

    def publish_static_site(
        self,
        project_id: str,
        source_dir: Path,
        *,
        version: str,
    ) -> Release:
        project = self.get_project(
            project_id
        )

        if project.artifact_type != "static_site":
            raise PublishError(
                "project is not a static_site project"
            )

        source_dir = source_dir.resolve()

        if not source_dir.is_dir():
            raise PublishError(
                "static source must be a directory"
            )

        index = source_dir / "index.html"

        if not index.is_file():
            raise PublishError(
                "static site requires index.html"
            )

        version = validate_version(
            version
        )

        entries: list[
            tuple[str, bytes]
        ] = []

        for path in sorted(
            source_dir.rglob("*")
        ):
            if not path.is_file():
                continue

            relative = path.relative_to(
                source_dir
            )

            if (
                ".."
                in relative.parts
            ):
                raise PublishError(
                    "path traversal rejected"
                )

            entries.append(
                (
                    relative.as_posix(),
                    path.read_bytes(),
                )
            )

        manifest = [
            {
                "path": name,
                "sha256": sha256_bytes(
                    data
                ),
                "size": len(data),
            }
            for name, data in entries
        ]

        digest = sha256(
            _canonical(
                manifest
            ).encode("utf-8")
        ).hexdigest()

        release_id = self._release_id(
            project,
            version,
            digest,
        )

        destination = (
            self.sites_dir
            / release_id
        )

        if not destination.exists():
            destination.mkdir(
                parents=True,
                exist_ok=False,
            )

            for name, data in entries:
                target = (
                    destination / name
                )

                target.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                target.write_bytes(data)

        release = Release(
            release_id=release_id,
            project_id=project.project_id,
            version=version,
            artifact_sha256=digest,
            artifact_size=sum(
                len(data)
                for _, data in entries
            ),
            artifact_type="static_site",
            created_at=int(time.time()),
            status="stored",
            storage_key=(
                f"sites/{release_id}"
            ),
            filename=None,
            metadata={
                "file_count": len(entries),
                "manifest": manifest,
            },
        )

        self._write_release(
            release
        )

        return release

    def register_web_service(
        self,
        project_id: str,
        *,
        version: str,
        backend: str,
        health_path: str = "/",
    ) -> tuple[Release, RouteManifest]:
        project = self.get_project(
            project_id
        )

        if project.artifact_type != "web_service":
            raise PublishError(
                "project is not a web_service project"
            )

        version = validate_version(
            version
        )

        digest = sha256(
            (
                project.project_id
                + "\n"
                + version
                + "\n"
                + backend
            ).encode("utf-8")
        ).hexdigest()

        release_id = self._release_id(
            project,
            version,
            digest,
        )

        release = Release(
            release_id=release_id,
            project_id=project.project_id,
            version=version,
            artifact_sha256=digest,
            artifact_size=0,
            artifact_type="web_service",
            created_at=int(time.time()),
            status="registered",
            storage_key=None,
            filename=None,
            metadata={
                "health_path": health_path,
            },
        )

        self._write_release(
            release
        )

        route = RouteManifest(
            schema=1,
            route_id=f"route-{release_id}",
            hostname=project.hostname,
            mode="reverse_proxy",
            target=backend,
            project_id=project.project_id,
            release_id=release_id,
            health_path=health_path,
        )

        self._write_atomic(
            self.routes_dir
            / f"{route.route_id}.json",
            asdict(route),
        )

        return release, route

    def route_for_static(
        self,
        project_id: str,
        release_id: str,
    ) -> RouteManifest:
        project = self.get_project(
            project_id
        )
        release = self.get_release(
            release_id
        )

        if (
            release.project_id
            != project.project_id
        ):
            raise PublishError(
                "release does not belong to project"
            )

        if release.artifact_type != "static_site":
            raise PublishError(
                "release is not static"
            )

        route = RouteManifest(
            schema=1,
            route_id=f"route-{release_id}",
            hostname=project.hostname,
            mode="static",
            target=str(
                (
                    self.root
                    / str(
                        release.storage_key
                    )
                ).resolve()
            ),
            project_id=project.project_id,
            release_id=release.release_id,
        )

        self._write_atomic(
            self.routes_dir
            / f"{route.route_id}.json",
            asdict(route),
        )

        return route

    def activate(
        self,
        project_id: str,
        release_id: str,
    ) -> Project:
        project = self.get_project(
            project_id
        )
        release = self.get_release(
            release_id
        )

        if (
            release.project_id
            != project.project_id
        ):
            raise PublishError(
                "release does not belong to project"
            )

        updated = Project(
            **{
                **asdict(project),
                "active_release_id": (
                    release.release_id
                ),
            }
        )

        self._write_atomic(
            self._project_path(
                project.project_id
            ),
            asdict(updated),
        )

        return updated

    def rollback(
        self,
        project_id: str,
        release_id: str,
    ) -> Project:
        return self.activate(
            project_id,
            release_id,
        )

    def latest_release(
        self,
        project_id: str,
    ) -> Release:
        project = self.get_project(
            project_id
        )

        if not project.active_release_id:
            raise PublishError(
                "project has no active release"
            )

        return self.get_release(
            project.active_release_id
        )

    def public_project(
        self,
        project_id: str,
    ) -> dict[str, Any]:
        project = self.get_project(
            project_id
        )

        payload = asdict(project)

        if project.active_release_id:
            release = self.get_release(
                project.active_release_id
            )

            payload["active_release"] = {
                "release_id": (
                    release.release_id
                ),
                "version": (
                    release.version
                ),
                "sha256": (
                    release.artifact_sha256
                ),
                "size": (
                    release.artifact_size
                ),
                "filename": (
                    release.filename
                ),
                "metadata": (
                    release.metadata
                ),
            }

        return payload

    def download_url(
        self,
        project_id: str,
        *,
        version: str = "latest",
        platform: str = "generic",
    ) -> str:
        project = self.get_project(
            project_id
        )

        return (
            f"https://{self.base_domain}"
            f"/d/{project.owner_id}"
            f"/{project.slug}"
            f"/{version}"
            f"/{platform}"
        )
