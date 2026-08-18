from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from shmry_platform.native_server import (
    NativePublisherServer,
    NativeServeError,
)
from shmry_platform.publish import (
    PublishStore,
)


class NativePublisherTests(
    unittest.TestCase
):
    def setUp(self):
        self.tmp = (
            tempfile.TemporaryDirectory()
        )

        self.root = (
            Path(self.tmp.name)
            / "publish"
        )

        self.store = PublishStore(
            self.root
        )

        self.server = (
            NativePublisherServer(
                self.store
            )
        )

    def tearDown(self):
        self.tmp.cleanup()

    def make_static(
        self,
        *,
        body="hello",
    ):
        project = (
            self.store.create_project(
                owner_id="badar",
                slug="steelcalc",
                title="Steel Calc",
                artifact_type="static_site",
            )
        )

        site = (
            Path(self.tmp.name)
            / "site"
        )

        site.mkdir(
            exist_ok=True
        )

        (
            site / "index.html"
        ).write_text(
            body,
            encoding="utf-8",
        )

        release = (
            self.store.publish_static_site(
                project.project_id,
                site,
                version="1",
            )
        )

        self.store.activate(
            project.project_id,
            release.release_id,
        )

        return (
            project,
            release,
        )

    def test_hostname_resolves_active_project(self):
        project, release = (
            self.make_static()
        )

        response = (
            self.server.resolve_static(
                hostname=(
                    "steelcalc-badar."
                    "shmry.com"
                ),
                request_path="/",
            )
        )

        self.assertEqual(
            response.status,
            200,
        )

        self.assertEqual(
            response.body,
            b"hello",
        )

        self.assertEqual(
            response.headers[
                "x-shmry-release"
            ],
            release.release_id,
        )

    def test_host_port_is_accepted(self):
        self.make_static()

        response = (
            self.server.resolve_static(
                hostname=(
                    "steelcalc-badar."
                    "shmry.com:443"
                ),
                request_path="/",
            )
        )

        self.assertEqual(
            response.status,
            200,
        )

    def test_unknown_hostname_rejected(self):
        self.make_static()

        with self.assertRaises(
            NativeServeError
        ):
            self.server.resolve_static(
                hostname=(
                    "unknown.shmry.com"
                ),
                request_path="/",
            )

    def test_unactivated_site_rejected(self):
        project = (
            self.store.create_project(
                owner_id="badar",
                slug="draft",
                title="Draft",
                artifact_type=(
                    "static_site"
                ),
            )
        )

        with self.assertRaises(
            NativeServeError
        ):
            self.server.resolve_static(
                hostname=(
                    project.hostname
                ),
                request_path="/",
            )

    def test_static_asset(self):
        project = (
            self.store.create_project(
                owner_id="badar",
                slug="assets",
                title="Assets",
                artifact_type=(
                    "static_site"
                ),
            )
        )

        site = (
            Path(self.tmp.name)
            / "assets-site"
        )

        (
            site / "css"
        ).mkdir(
            parents=True
        )

        (
            site / "index.html"
        ).write_text(
            "index",
            encoding="utf-8",
        )

        (
            site / "css/app.css"
        ).write_text(
            "body{}",
            encoding="utf-8",
        )

        release = (
            self.store.publish_static_site(
                project.project_id,
                site,
                version="1",
            )
        )

        self.store.activate(
            project.project_id,
            release.release_id,
        )

        response = (
            self.server.resolve_static(
                hostname=(
                    project.hostname
                ),
                request_path=(
                    "/css/app.css"
                ),
            )
        )

        self.assertEqual(
            response.body,
            b"body{}",
        )

        self.assertEqual(
            response.headers[
                "content-type"
            ],
            "text/css",
        )

    def test_path_traversal_rejected(self):
        project, _ = (
            self.make_static()
        )

        with self.assertRaises(
            NativeServeError
        ):
            self.server.resolve_static(
                hostname=(
                    project.hostname
                ),
                request_path=(
                    "/../secret"
                ),
            )

    def test_latest_download(self):
        project = (
            self.store.create_project(
                owner_id="badar",
                slug="myapp",
                title="My App",
                artifact_type="download",
            )
        )

        file = (
            Path(self.tmp.name)
            / "myapp.apk"
        )

        file.write_bytes(
            b"apk-payload"
        )

        release = (
            self.store.publish_download(
                project.project_id,
                file,
                version="1.2.3",
                platform="android",
            )
        )

        self.store.activate(
            project.project_id,
            release.release_id,
        )

        response = (
            self.server.dispatch(
                hostname="shmry.com",
                request_path=(
                    "/d/badar/myapp/"
                    "latest/android"
                ),
            )
        )

        self.assertEqual(
            response.status,
            200,
        )

        self.assertEqual(
            response.body,
            b"apk-payload",
        )

        self.assertIn(
            "attachment;",
            response.headers[
                "content-disposition"
            ],
        )

        self.assertEqual(
            response.headers[
                "x-shmry-sha256"
            ],
            release.artifact_sha256,
        )

    def test_versioned_download(self):
        project = (
            self.store.create_project(
                owner_id="badar",
                slug="tool",
                title="Tool",
                artifact_type="download",
            )
        )

        file = (
            Path(self.tmp.name)
            / "tool.zip"
        )

        file.write_bytes(
            b"one"
        )

        release = (
            self.store.publish_download(
                project.project_id,
                file,
                version="4.5.6",
                platform="linux",
            )
        )

        response = (
            self.server.dispatch(
                hostname="shmry.com",
                request_path=(
                    "/d/badar/tool/"
                    "4.5.6/linux"
                ),
            )
        )

        self.assertEqual(
            response.body,
            b"one",
        )

        self.assertEqual(
            response.headers[
                "x-shmry-release"
            ],
            release.release_id,
        )

    def test_tampered_download_rejected(self):
        project = (
            self.store.create_project(
                owner_id="badar",
                slug="tampered",
                title="Tampered",
                artifact_type="download",
            )
        )

        file = (
            Path(self.tmp.name)
            / "app.bin"
        )

        file.write_bytes(
            b"original"
        )

        release = (
            self.store.publish_download(
                project.project_id,
                file,
                version="1",
            )
        )

        self.store.activate(
            project.project_id,
            release.release_id,
        )

        stored = (
            self.store.root
            / release.storage_key
        )

        stored.write_bytes(
            b"modified"
        )

        with self.assertRaises(
            NativeServeError
        ):
            self.server.resolve_download(
                owner="badar",
                slug="tampered",
                version="latest",
                platform="generic",
            )

    def test_static_etag_is_release_digest(self):
        project, release = (
            self.make_static()
        )

        response = (
            self.server.resolve_static(
                hostname=(
                    project.hostname
                ),
                request_path="/",
            )
        )

        self.assertEqual(
            response.headers["etag"],
            (
                '"'
                + release.artifact_sha256
                + '"'
            ),
        )


if __name__ == "__main__":
    unittest.main()
