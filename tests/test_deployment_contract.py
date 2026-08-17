from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from shmry_platform.deployment import (
    ShmryDeploymentError,
    deploy_website,
)


class ShmryWebsiteDeploymentTests(unittest.TestCase):
    def test_deploy_html_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            artifact = root / "product.html"

            artifact.write_text(
                "<!doctype html><h1>Hello</h1>",
                encoding="utf-8",
            )

            result = deploy_website(
                str(artifact),
                project_name="Example Product",
                deployment_root=str(
                    root / "deployments"
                ),
            )

            self.assertEqual(
                result["provider_id"],
                "shmry",
            )

            self.assertEqual(
                result["status"],
                "ready",
            )

            deployed = (
                Path(
                    result["deployment_root"]
                )
                / "index.html"
            )

            self.assertTrue(
                deployed.is_file()
            )

    def test_missing_artifact_rejected(self):
        with self.assertRaises(
            ShmryDeploymentError
        ):
            deploy_website(
                "/does/not/exist.html"
            )

    def test_non_html_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact = (
                Path(tmp)
                / "file.txt"
            )

            artifact.write_text(
                "no",
                encoding="utf-8",
            )

            with self.assertRaises(
                ShmryDeploymentError
            ):
                deploy_website(
                    str(artifact)
                )

    def test_cli_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            artifact = root / "index.html"

            artifact.write_text(
                "<html>ok</html>",
                encoding="utf-8",
            )

            proc = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "shmry_platform.deployment_cli",
                ],
                input=json.dumps(
                    {
                        "artifact": str(artifact),
                        "project_name": "cli-test",
                        "deployment_root": str(
                            root / "deployments"
                        ),
                    }
                ),
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(
                proc.returncode,
                0,
                proc.stderr,
            )

            response = json.loads(
                proc.stdout
            )

            self.assertEqual(
                response["provider_id"],
                "shmry",
            )

            self.assertEqual(
                response["status"],
                "ready",
            )


if __name__ == "__main__":
    unittest.main()
