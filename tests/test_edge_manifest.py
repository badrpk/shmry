from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from shmry_platform.edge_manifest import (
    EdgeManifestError,
    EdgeManifestManager,
)
from shmry_platform.publish import (
    PublishStore,
)
from shmry_platform.veyron_contract import (
    export_veyron_route_registry,
    load_veyron_routes,
)


class EdgeManifestTests(
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

    def tearDown(self):
        self.tmp.cleanup()

    def make_static(
        self,
        owner="badar",
        slug="steelcalc",
    ):
        project = (
            self.store.create_project(
                owner_id=owner,
                slug=slug,
                title="Static",
                artifact_type=(
                    "static_site"
                ),
            )
        )

        source = (
            Path(self.tmp.name)
            / f"site-{slug}"
        )

        source.mkdir()

        (
            source / "index.html"
        ).write_text(
            "hello",
            encoding="utf-8",
        )

        release = (
            self.store.publish_static_site(
                project.project_id,
                source,
                version="1",
            )
        )

        self.store.activate(
            project.project_id,
            release.release_id,
        )

        return project, release

    def test_static_project_becomes_native_edge_route(self):
        project, release = (
            self.make_static()
        )

        manager = (
            EdgeManifestManager(
                self.store,
                native_origin=(
                    "http://127.0.0.1:8088"
                ),
            )
        )

        routes = manager.build_routes()

        self.assertEqual(
            len(routes),
            1,
        )

        route = routes[0]

        self.assertEqual(
            route.hostname,
            project.hostname,
        )

        self.assertEqual(
            route.release_id,
            release.release_id,
        )

        self.assertEqual(
            route.route_type,
            "shmry_native",
        )

        self.assertEqual(
            route.origin,
            "http://127.0.0.1:8088",
        )

    def test_unactivated_project_not_published(self):
        self.store.create_project(
            owner_id="badar",
            slug="draft",
            title="Draft",
            artifact_type="static_site",
        )

        manager = (
            EdgeManifestManager(
                self.store
            )
        )

        self.assertEqual(
            manager.build_routes(),
            (),
        )

    def test_private_project_not_published(self):
        project = (
            self.store.create_project(
                owner_id="badar",
                slug="private",
                title="Private",
                artifact_type="static_site",
                visibility="private",
            )
        )

        source = (
            Path(self.tmp.name)
            / "private-site"
        )

        source.mkdir()
        (
            source / "index.html"
        ).write_text(
            "private",
            encoding="utf-8",
        )

        release = (
            self.store.publish_static_site(
                project.project_id,
                source,
                version="1",
            )
        )

        self.store.activate(
            project.project_id,
            release.release_id,
        )

        manager = (
            EdgeManifestManager(
                self.store
            )
        )

        self.assertEqual(
            manager.build_routes(),
            (),
        )

    def test_web_service_becomes_reverse_proxy_route(self):
        project = (
            self.store.create_project(
                owner_id="badar",
                slug="agent-api",
                title="Agent API",
                artifact_type="web_service",
            )
        )

        release, _ = (
            self.store.register_web_service(
                project.project_id,
                version="1",
                backend=(
                    "http://127.0.0.1:9100"
                ),
                health_path="/health",
            )
        )

        self.store.activate(
            project.project_id,
            release.release_id,
        )

        manager = (
            EdgeManifestManager(
                self.store
            )
        )

        routes = manager.build_routes()

        self.assertEqual(
            len(routes),
            1,
        )

        route = routes[0]

        self.assertEqual(
            route.route_type,
            "reverse_proxy",
        )

        self.assertEqual(
            route.origin,
            "http://127.0.0.1:9100",
        )

        self.assertEqual(
            route.health_path,
            "/health",
        )

    def test_snapshot_digest_is_deterministic(self):
        self.make_static()

        manager = (
            EdgeManifestManager(
                self.store
            )
        )

        one = manager.build_snapshot()

        # Same generation inputs yield same digest.
        payload = {
            "schema": one.schema,
            "generation": one.generation,
            "routes": [
                route.__dict__
                for route in one.routes
            ],
        }

        from shmry_platform.edge_manifest import (
            digest_payload,
        )

        self.assertEqual(
            one.manifest_sha256,
            digest_payload(payload),
        )

    def test_atomic_active_snapshot(self):
        self.make_static()

        manager = (
            EdgeManifestManager(
                self.store
            )
        )

        payload = (
            manager.publish_snapshot()
        )

        self.assertTrue(
            manager.active_path.is_file()
        )

        active = json.loads(
            manager.active_path.read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(
            active,
            payload,
        )

    def test_generation_increments(self):
        self.make_static()

        manager = (
            EdgeManifestManager(
                self.store
            )
        )

        one = manager.publish_snapshot()
        two = manager.publish_snapshot()

        self.assertEqual(
            two["generation"],
            one["generation"] + 1,
        )

    def test_tampered_snapshot_rejected(self):
        self.make_static()

        manager = (
            EdgeManifestManager(
                self.store
            )
        )

        payload = (
            manager.publish_snapshot()
        )

        payload["routes"][0][
            "hostname"
        ] = "tampered.shmry.com"

        with self.assertRaises(
            EdgeManifestError
        ):
            (
                manager.validate_snapshot_payload(
                    payload
                )
            )

    def test_nonloopback_native_origin_rejected(self):
        with self.assertRaises(
            EdgeManifestError
        ):
            EdgeManifestManager(
                self.store,
                native_origin=(
                    "http://192.168.1.10:8088"
                ),
            )

    def test_veyron_registry_export(self):
        project, release = (
            self.make_static()
        )

        manager = (
            EdgeManifestManager(
                self.store
            )
        )

        manager.publish_snapshot()

        output = (
            Path(self.tmp.name)
            / "veyron-routes.json"
        )

        registry = (
            export_veyron_route_registry(
                manager.active_path,
                output,
            )
        )

        self.assertEqual(
            registry["schema"],
            1,
        )

        self.assertEqual(
            registry["routes"][0][
                "hostname"
            ],
            project.hostname,
        )

        self.assertEqual(
            registry["routes"][0][
                "release_id"
            ],
            release.release_id,
        )

    def test_veyron_loader_rejects_bad_digest(self):
        self.make_static()

        manager = (
            EdgeManifestManager(
                self.store
            )
        )

        manager.publish_snapshot()

        payload = json.loads(
            manager.active_path.read_text(
                encoding="utf-8"
            )
        )

        payload[
            "manifest_sha256"
        ] = "0" * 64

        manager.active_path.write_text(
            json.dumps(payload),
            encoding="utf-8",
        )

        with self.assertRaises(
            EdgeManifestError
        ):
            load_veyron_routes(
                manager.active_path
            )


if __name__ == "__main__":
    unittest.main()
