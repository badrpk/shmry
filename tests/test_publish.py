from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import tempfile
import unittest

from shmry_platform.publish import (
    PublishError,
    PublishStore,
    validate_slug,
)


class PublishTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.store = PublishStore(
            self.root / "publish"
        )

    def tearDown(self):
        self.tmp.cleanup()

    def static_project(self):
        return self.store.create_project(
            owner_id="badar",
            slug="steelcalc",
            title="Steel Calculator",
            artifact_type="static_site",
        )

    def test_slug_validation(self):
        self.assertEqual(
            validate_slug("hello-world"),
            "hello-world",
        )

        for value in (
            "../bad",
            "Bad_Name",
            "-bad",
            "bad-",
            "bad space",
        ):
            with self.assertRaises(
                PublishError
            ):
                validate_slug(value)

    def test_stable_project_urls(self):
        project = self.static_project()

        self.assertEqual(
            project.hostname,
            "steelcalc-badar.shmry.com",
        )

        self.assertEqual(
            project.project_url,
            "https://shmry.com/@badar/steelcalc",
        )

    def test_duplicate_project_rejected(self):
        self.static_project()

        with self.assertRaises(
            PublishError
        ):
            self.static_project()

    def test_static_site_release_is_immutable(self):
        project = self.static_project()

        site = self.root / "site"
        site.mkdir()
        (site / "index.html").write_text(
            "<h1>Hello</h1>",
            encoding="utf-8",
        )

        release = (
            self.store.publish_static_site(
                project.project_id,
                site,
                version="1.0.0",
            )
        )

        saved = self.store.get_release(
            release.release_id
        )

        self.assertEqual(
            saved.artifact_sha256,
            release.artifact_sha256,
        )

        hosted = (
            self.root
            / "publish"
            / release.storage_key
            / "index.html"
        )

        self.assertEqual(
            hosted.read_text(
                encoding="utf-8"
            ),
            "<h1>Hello</h1>",
        )

    def test_static_digest_changes_with_content(self):
        project = self.static_project()

        site = self.root / "site"
        site.mkdir()

        index = site / "index.html"
        index.write_text(
            "one",
            encoding="utf-8",
        )

        one = self.store.publish_static_site(
            project.project_id,
            site,
            version="1.0.0",
        )

        index.write_text(
            "two",
            encoding="utf-8",
        )

        two = self.store.publish_static_site(
            project.project_id,
            site,
            version="2.0.0",
        )

        self.assertNotEqual(
            one.artifact_sha256,
            two.artifact_sha256,
        )

    def test_static_requires_index(self):
        project = self.static_project()

        site = self.root / "site"
        site.mkdir()

        with self.assertRaises(
            PublishError
        ):
            self.store.publish_static_site(
                project.project_id,
                site,
                version="1",
            )

    def test_activate_and_rollback(self):
        project = self.static_project()

        site = self.root / "site"
        site.mkdir()

        index = site / "index.html"

        index.write_text(
            "one",
            encoding="utf-8",
        )

        one = self.store.publish_static_site(
            project.project_id,
            site,
            version="1",
        )

        index.write_text(
            "two",
            encoding="utf-8",
        )

        two = self.store.publish_static_site(
            project.project_id,
            site,
            version="2",
        )

        active = self.store.activate(
            project.project_id,
            two.release_id,
        )

        self.assertEqual(
            active.active_release_id,
            two.release_id,
        )

        rolled = self.store.rollback(
            project.project_id,
            one.release_id,
        )

        self.assertEqual(
            rolled.active_release_id,
            one.release_id,
        )

        self.assertEqual(
            self.store.get_release(
                two.release_id
            ).artifact_sha256,
            two.artifact_sha256,
        )

    def test_download_artifact_and_latest(self):
        project = self.store.create_project(
            owner_id="badar",
            slug="myapp",
            title="My App",
            artifact_type="download",
        )

        artifact = (
            self.root / "myapp.apk"
        )
        artifact.write_bytes(
            b"apk-data"
        )

        release = (
            self.store.publish_download(
                project.project_id,
                artifact,
                version="1.2.3",
                platform="android",
            )
        )

        self.assertEqual(
            release.artifact_sha256,
            sha256(
                b"apk-data"
            ).hexdigest(),
        )

        self.store.activate(
            project.project_id,
            release.release_id,
        )

        latest = (
            self.store.latest_release(
                project.project_id
            )
        )

        self.assertEqual(
            latest.release_id,
            release.release_id,
        )

        self.assertEqual(
            self.store.download_url(
                project.project_id,
                platform="android",
            ),
            "https://shmry.com/d/badar/myapp/latest/android",
        )

    def test_download_storage_is_content_addressed(self):
        project = self.store.create_project(
            owner_id="badar",
            slug="binary",
            title="Binary",
            artifact_type="download",
        )

        artifact = self.root / "tool.zip"
        artifact.write_bytes(
            b"payload"
        )

        release = (
            self.store.publish_download(
                project.project_id,
                artifact,
                version="1",
            )
        )

        self.assertIn(
            release.artifact_sha256,
            release.storage_key,
        )

    def test_static_route_manifest_for_veyron(self):
        project = self.static_project()

        site = self.root / "site"
        site.mkdir()
        (site / "index.html").write_text(
            "ok",
            encoding="utf-8",
        )

        release = (
            self.store.publish_static_site(
                project.project_id,
                site,
                version="1",
            )
        )

        route = self.store.route_for_static(
            project.project_id,
            release.release_id,
        )

        self.assertEqual(
            route.hostname,
            "steelcalc-badar.shmry.com",
        )
        self.assertEqual(
            route.mode,
            "static",
        )

    def test_web_service_route_contract(self):
        project = self.store.create_project(
            owner_id="badar",
            slug="agent-api",
            title="Agent API",
            artifact_type="web_service",
        )

        release, route = (
            self.store.register_web_service(
                project.project_id,
                version="1",
                backend="http://127.0.0.1:9010",
                health_path="/health",
            )
        )

        self.assertEqual(
            route.mode,
            "reverse_proxy",
        )
        self.assertEqual(
            route.release_id,
            release.release_id,
        )

        public = route.public_dict()

        self.assertEqual(
            public["target"],
            "internal",
        )

        self.assertNotIn(
            "127.0.0.1",
            str(public),
        )

    def test_nonlocal_backend_rejected_phase1(self):
        project = self.store.create_project(
            owner_id="badar",
            slug="remote-api",
            title="Remote",
            artifact_type="web_service",
        )

        with self.assertRaises(
            PublishError
        ):
            self.store.register_web_service(
                project.project_id,
                version="1",
                backend="https://private.example.com",
            )

    def test_public_metadata_has_no_private_backend(self):
        project = self.store.create_project(
            owner_id="badar",
            slug="service",
            title="Service",
            artifact_type="web_service",
        )

        release, _ = (
            self.store.register_web_service(
                project.project_id,
                version="1",
                backend="http://localhost:9000",
            )
        )

        self.store.activate(
            project.project_id,
            release.release_id,
        )

        public = self.store.public_project(
            project.project_id
        )

        rendered = str(public)

        self.assertNotIn(
            "localhost",
            rendered,
        )
        self.assertNotIn(
            "127.0.0.1",
            rendered,
        )

    def test_release_cannot_cross_project(self):
        one = self.static_project()

        other = self.store.create_project(
            owner_id="badar",
            slug="other",
            title="Other",
            artifact_type="static_site",
        )

        site = self.root / "site"
        site.mkdir()
        (site / "index.html").write_text(
            "x",
            encoding="utf-8",
        )

        release = (
            self.store.publish_static_site(
                one.project_id,
                site,
                version="1",
            )
        )

        with self.assertRaises(
            PublishError
        ):
            self.store.activate(
                other.project_id,
                release.release_id,
            )


if __name__ == "__main__":
    unittest.main()
