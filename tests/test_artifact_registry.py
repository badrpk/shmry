import unittest

from platform.artifact_registry import Artifact, ArtifactRegistry


class ArtifactRegistryTests(unittest.TestCase):
    def make(self, registry, artifact_id="a1", data=b"hello", **kwargs):
        artifact = Artifact(
            artifact_id=artifact_id,
            name=kwargs.pop("name", "bundle"),
            version=kwargs.pop("version", "1.0.0"),
            owner=kwargs.pop("owner", "shmry"),
            service=kwargs.pop("service", "downloads"),
            sha256=registry.digest(data),
            size_bytes=len(data),
            **kwargs,
        )
        registry.register(artifact)
        return artifact

    def test_verify_bytes(self):
        r = ArtifactRegistry()
        self.make(r)
        self.assertTrue(r.verify_bytes("a1", b"hello"))
        self.assertFalse(r.verify_bytes("a1", b"HELLO"))

    def test_duplicate_id_rejected(self):
        r = ArtifactRegistry()
        a = self.make(r)
        with self.assertRaises(ValueError):
            r.register(a)

    def test_unknown_parent_rejected(self):
        r = ArtifactRegistry()
        with self.assertRaises(ValueError):
            self.make(r, parent_id="missing")

    def test_lineage(self):
        r = ArtifactRegistry()
        self.make(r, "a1")
        self.make(r, "a2", data=b"two", version="2.0.0", parent_id="a1")
        self.assertEqual([x.artifact_id for x in r.lineage("a2")], ["a1", "a2"])

    def test_visibility_filter(self):
        r = ArtifactRegistry()
        self.make(r, "pub")
        self.make(r, "priv", data=b"secret-meta", visibility="private")
        self.assertEqual([x.artifact_id for x in r.list(visibility="public")], ["pub"])

    def test_public_manifest_excludes_private(self):
        r = ArtifactRegistry()
        self.make(r, "pub")
        self.make(r, "priv", data=b"private", visibility="private")
        ids = [x["artifact_id"] for x in r.manifest()["artifacts"]]
        self.assertEqual(ids, ["pub"])

    def test_manifest_is_deterministic(self):
        r = ArtifactRegistry()
        self.make(r, "b", data=b"b", name="z")
        self.make(r, "a", data=b"a", name="a")
        self.assertEqual(r.manifest(), r.manifest())

    def test_service_filter(self):
        r = ArtifactRegistry()
        self.make(r, "d", service="downloads")
        self.make(r, "s", data=b"s", service="storage")
        self.assertEqual([x.artifact_id for x in r.list(service="storage")], ["s"])

    def test_invalid_digest_rejected(self):
        with self.assertRaises(ValueError):
            Artifact("a", "n", "1", "o", "s", "not-a-digest", 1)


if __name__ == "__main__":
    unittest.main()
