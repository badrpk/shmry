from __future__ import annotations

import hashlib
import json
import os
import shutil
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DeploymentResult:
    status: str
    provider_id: str
    deployment_id: str
    artifact: str
    project_name: str
    environment: str
    deployment_root: str
    url: str
    sha256: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class ShmryDeploymentError(RuntimeError):
    pass


def _digest(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


def _safe_project_name(value: str) -> str:
    cleaned = "".join(
        c.lower() if c.isalnum() else "-"
        for c in value.strip()
    )

    cleaned = "-".join(
        part
        for part in cleaned.split("-")
        if part
    )

    return (cleaned or "nifdu-site")[:63]


def deploy_website(
    artifact: str,
    *,
    project_name: str | None = None,
    environment: str = "production",
    deployment_root: str | None = None,
) -> dict[str, Any]:
    source = Path(artifact).expanduser().resolve()

    if not source.is_file():
        raise ShmryDeploymentError(
            f"artifact does not exist: {source}"
        )

    if source.suffix.lower() not in {
        ".html",
        ".htm",
    }:
        raise ShmryDeploymentError(
            "Shmry website deployment currently requires "
            "an HTML artifact"
        )

    project = _safe_project_name(
        project_name
        or source.parent.name
        or "nifdu-site"
    )

    root = Path(
        deployment_root
        or os.environ.get(
            "SHMRY_DEPLOYMENT_ROOT",
            str(
                Path.home()
                / ".local"
                / "share"
                / "shmry"
                / "deployments"
            ),
        )
    ).expanduser().resolve()

    root.mkdir(
        parents=True,
        exist_ok=True,
    )

    digest = _digest(source)

    deployment_id = (
        f"shmry-{int(time.time())}-{digest[:12]}"
    )

    target = root / project / deployment_id

    target.mkdir(
        parents=True,
        exist_ok=False,
    )

    target_index = target / "index.html"

    shutil.copy2(
        source,
        target_index,
    )

    manifest = {
        "schema": 1,
        "provider_id": "shmry",
        "deployment_id": deployment_id,
        "project_name": project,
        "environment": environment,
        "source_artifact": str(source),
        "deployed_artifact": str(target_index),
        "sha256": digest,
        "status": "ready",
    }

    (
        target / "deployment.json"
    ).write_text(
        json.dumps(
            manifest,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    return DeploymentResult(
        status="ready",
        provider_id="shmry",
        deployment_id=deployment_id,
        artifact=str(source),
        project_name=project,
        environment=environment,
        deployment_root=str(target),
        url=f"shmry://{project}/{deployment_id}",
        sha256=digest,
    ).as_dict()
