from __future__ import annotations

import json
import sys

from shmry_platform.deployment import (
    ShmryDeploymentError,
    deploy_website,
)


def main() -> int:
    try:
        request = json.load(sys.stdin)

        artifact = request.get("artifact")

        if not artifact:
            print(
                json.dumps(
                    {
                        "status": "needs_input",
                        "provider_id": "shmry",
                        "missing_fields": ["artifact"],
                    }
                )
            )
            return 0

        result = deploy_website(
            artifact,
            project_name=request.get("project_name"),
            environment=request.get(
                "environment",
                "production",
            ),
            deployment_root=request.get(
                "deployment_root"
            ),
        )

        print(
            json.dumps(
                result,
                sort_keys=True,
            )
        )

        return 0

    except ShmryDeploymentError as exc:
        print(
            json.dumps(
                {
                    "status": "rejected",
                    "provider_id": "shmry",
                    "error": str(exc),
                }
            )
        )
        return 2

    except Exception as exc:
        print(
            json.dumps(
                {
                    "status": "error",
                    "provider_id": "shmry",
                    "error": str(exc),
                }
            )
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
