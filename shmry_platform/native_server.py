from __future__ import annotations

from dataclasses import dataclass
import mimetypes
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from shmry_platform.publish import (
    Project,
    PublishError,
    PublishStore,
    Release,
)


class NativeServeError(RuntimeError):
    pass


@dataclass(frozen=True)
class NativeResponse:
    status: int
    headers: dict[str, str]
    body: bytes


def _safe_relative_path(raw: str) -> Path:
    raw = unquote(raw)
    raw = raw.lstrip("/")

    if not raw:
        raw = "index.html"

    path = Path(raw)

    if (
        path.is_absolute()
        or ".." in path.parts
        or any(part in {"", "."} for part in path.parts)
    ):
        raise NativeServeError(
            "invalid request path"
        )

    return path


class NativePublisherServer:
    """
    Provider-independent Shmry native publishing resolver.

    This class does not open sockets and does not terminate TLS.
    Veyron/VPS can forward ordinary HTTP requests to this layer.
    """

    def __init__(
        self,
        store: PublishStore,
    ) -> None:
        self.store = store

    def project_for_hostname(
        self,
        hostname: str,
    ) -> Project:
        hostname = (
            hostname.split(":", 1)[0]
            .strip()
            .lower()
        )

        matches: list[Project] = []

        for record in sorted(
            self.store.projects_dir.glob(
                "*.json"
            )
        ):
            payload = (
                self.store._read_json(
                    record
                )
            )

            project = Project(
                **payload
            )

            if (
                project.hostname.lower()
                == hostname
            ):
                matches.append(
                    project
                )

        if not matches:
            raise NativeServeError(
                "unknown hostname"
            )

        if len(matches) != 1:
            raise NativeServeError(
                "ambiguous hostname"
            )

        return matches[0]

    def active_release(
        self,
        project: Project,
    ) -> Release:
        if not project.active_release_id:
            raise NativeServeError(
                "project has no active release"
            )

        release = self.store.get_release(
            project.active_release_id
        )

        if (
            release.project_id
            != project.project_id
        ):
            raise NativeServeError(
                "active release mismatch"
            )

        return release

    def resolve_static(
        self,
        *,
        hostname: str,
        request_path: str,
    ) -> NativeResponse:
        project = self.project_for_hostname(
            hostname
        )

        release = self.active_release(
            project
        )

        if (
            release.artifact_type
            != "static_site"
        ):
            raise NativeServeError(
                "active release is not static"
            )

        if not release.storage_key:
            raise NativeServeError(
                "static release missing storage"
            )

        relative = _safe_relative_path(
            request_path
        )

        root = (
            self.store.root
            / release.storage_key
        ).resolve()

        candidate = (
            root / relative
        ).resolve()

        try:
            candidate.relative_to(
                root
            )
        except ValueError as exc:
            raise NativeServeError(
                "path escaped release root"
            ) from exc

        if candidate.is_dir():
            candidate = (
                candidate / "index.html"
            ).resolve()

        if not candidate.is_file():
            # SPA/static-site convenience fallback.
            fallback = (
                root / "index.html"
            ).resolve()

            if fallback.is_file():
                candidate = fallback
            else:
                return NativeResponse(
                    status=404,
                    headers={
                        "content-type": (
                            "text/plain; charset=utf-8"
                        ),
                        "cache-control": "no-store",
                    },
                    body=b"Not Found\n",
                )

        content_type = (
            mimetypes.guess_type(
                candidate.name
            )[0]
            or "application/octet-stream"
        )

        data = candidate.read_bytes()

        return NativeResponse(
            status=200,
            headers={
                "content-type": content_type,
                "content-length": str(
                    len(data)
                ),
                "etag": (
                    f'"{release.artifact_sha256}"'
                ),
                "x-shmry-project": (
                    project.project_id
                ),
                "x-shmry-release": (
                    release.release_id
                ),
                "x-content-type-options": (
                    "nosniff"
                ),
            },
            body=data,
        )

    def resolve_download(
        self,
        *,
        owner: str,
        slug: str,
        version: str,
        platform: str,
    ) -> NativeResponse:
        project_id = (
            f"proj-{owner}-{slug}"
        )

        project = self.store.get_project(
            project_id
        )

        if (
            project.artifact_type
            != "download"
        ):
            raise NativeServeError(
                "project is not a download project"
            )

        if version == "latest":
            release = self.active_release(
                project
            )
        else:
            release = (
                self._release_by_version(
                    project,
                    version,
                    platform,
                )
            )

        if (
            release.artifact_type
            != "download"
        ):
            raise NativeServeError(
                "release is not downloadable"
            )

        if not release.storage_key:
            raise NativeServeError(
                "download release missing storage"
            )

        artifact = (
            self.store.root
            / release.storage_key
        ).resolve()

        artifact_root = (
            self.store.artifacts_dir
        ).resolve()

        try:
            artifact.relative_to(
                artifact_root
            )
        except ValueError as exc:
            raise NativeServeError(
                "artifact escaped storage root"
            ) from exc

        if not artifact.is_file():
            raise NativeServeError(
                "artifact missing"
            )

        data = artifact.read_bytes()

        if (
            self.store.get_release(
                release.release_id
            ).artifact_sha256
            != release.artifact_sha256
        ):
            raise NativeServeError(
                "release registry mismatch"
            )

        from hashlib import sha256

        if (
            sha256(data).hexdigest()
            != release.artifact_sha256
        ):
            raise NativeServeError(
                "artifact digest verification failed"
            )

        filename = (
            release.filename
            or "download.bin"
        )

        content_type = (
            release.metadata.get(
                "content_type"
            )
            or "application/octet-stream"
        )

        return NativeResponse(
            status=200,
            headers={
                "content-type": str(
                    content_type
                ),
                "content-length": str(
                    len(data)
                ),
                "content-disposition": (
                    'attachment; filename="'
                    + filename.replace(
                        '"',
                        "",
                    )
                    + '"'
                ),
                "etag": (
                    f'"{release.artifact_sha256}"'
                ),
                "x-shmry-project": (
                    project.project_id
                ),
                "x-shmry-release": (
                    release.release_id
                ),
                "x-shmry-sha256": (
                    release.artifact_sha256
                ),
                "x-content-type-options": (
                    "nosniff"
                ),
            },
            body=data,
        )

    def _release_by_version(
        self,
        project: Project,
        version: str,
        platform: str,
    ) -> Release:
        matches: list[Release] = []

        for record in sorted(
            self.store.releases_dir.glob(
                "*.json"
            )
        ):
            release = Release(
                **self.store._read_json(
                    record
                )
            )

            if (
                release.project_id
                != project.project_id
            ):
                continue

            if (
                release.version
                != version
            ):
                continue

            release_platform = str(
                release.metadata.get(
                    "platform",
                    "generic",
                )
            )

            if (
                platform
                not in {
                    "generic",
                    release_platform,
                }
            ):
                continue

            matches.append(
                release
            )

        if not matches:
            raise NativeServeError(
                "release version not found"
            )

        if len(matches) != 1:
            raise NativeServeError(
                "ambiguous release version"
            )

        return matches[0]

    def dispatch(
        self,
        *,
        hostname: str,
        request_path: str,
    ) -> NativeResponse:
        path = (
            request_path.split(
                "?",
                1,
            )[0]
        )

        parts = [
            unquote(part)
            for part in path.split("/")
            if part
        ]

        if (
            hostname.split(":", 1)[0]
            .lower()
            == self.store.base_domain
            and len(parts) == 5
            and parts[0] == "d"
        ):
            return self.resolve_download(
                owner=parts[1],
                slug=parts[2],
                version=parts[3],
                platform=parts[4],
            )

        return self.resolve_static(
            hostname=hostname,
            request_path=path,
        )
