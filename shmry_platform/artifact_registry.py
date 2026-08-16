from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
import json
from typing import Iterable


@dataclass(frozen=True)
class Artifact:
    artifact_id: str
    name: str
    version: str
    owner: str
    service: str
    sha256: str
    size_bytes: int
    visibility: str = "public"
    parent_id: str | None = None

    def __post_init__(self) -> None:
        if not self.artifact_id.strip():
            raise ValueError("artifact_id is required")
        if not self.name.strip() or not self.version.strip():
            raise ValueError("name and version are required")
        if not self.owner.strip() or not self.service.strip():
            raise ValueError("owner and service are required")
        if self.visibility not in {"public", "private", "internal"}:
            raise ValueError("invalid visibility")
        if self.size_bytes < 0:
            raise ValueError("size_bytes must be >= 0")
        if len(self.sha256) != 64 or any(c not in "0123456789abcdef" for c in self.sha256):
            raise ValueError("sha256 must be lowercase hex")


class ArtifactRegistry:
    def __init__(self) -> None:
        self._items: dict[str, Artifact] = {}

    @staticmethod
    def digest(data: bytes) -> str:
        return sha256(data).hexdigest()

    def register(self, artifact: Artifact) -> Artifact:
        if artifact.artifact_id in self._items:
            raise ValueError("artifact_id already exists")
        if artifact.parent_id is not None and artifact.parent_id not in self._items:
            raise ValueError("parent artifact does not exist")
        self._items[artifact.artifact_id] = artifact
        return artifact

    def get(self, artifact_id: str) -> Artifact:
        try:
            return self._items[artifact_id]
        except KeyError as exc:
            raise KeyError(f"unknown artifact: {artifact_id}") from exc

    def verify_bytes(self, artifact_id: str, data: bytes) -> bool:
        artifact = self.get(artifact_id)
        return len(data) == artifact.size_bytes and self.digest(data) == artifact.sha256

    def list(self, *, visibility: str | None = None, service: str | None = None) -> list[Artifact]:
        items: Iterable[Artifact] = self._items.values()
        if visibility is not None:
            items = (x for x in items if x.visibility == visibility)
        if service is not None:
            items = (x for x in items if x.service == service)
        return sorted(items, key=lambda x: (x.service, x.name, x.version, x.artifact_id))

    def lineage(self, artifact_id: str) -> list[Artifact]:
        out: list[Artifact] = []
        seen: set[str] = set()
        current = self.get(artifact_id)
        while True:
            if current.artifact_id in seen:
                raise ValueError("artifact lineage cycle")
            seen.add(current.artifact_id)
            out.append(current)
            if current.parent_id is None:
                break
            current = self.get(current.parent_id)
        out.reverse()
        return out

    def manifest(self, *, include_private: bool = False) -> dict:
        items = [
            asdict(x)
            for x in self.list()
            if include_private or x.visibility == "public"
        ]
        payload = {"schema": 1, "artifacts": items}
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return {**payload, "manifest_sha256": sha256(canonical.encode()).hexdigest()}
