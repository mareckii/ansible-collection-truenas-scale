import json
import os
from pathlib import Path
from typing import Any, Dict

# Copyright: (c) 2024, Marek Marecki (@mareckii)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

try:
    from truenas_api_client import Client
except ImportError:  # pragma: no cover
    Client = None


def _build_backend() -> Client:
    backend = os.environ.get("TRUENAS_CLIENT_BACKEND", "api").lower()
    if backend == "stub":
        return _StubApiClient()
    if Client is None:
        raise ModuleNotFoundError(
            "The 'truenas_api_client' package is required when TRUENAS_CLIENT_BACKEND=api"
        )
    return Client()


class TruenasClient:
    _client: Client = None

    def __init__(self):
        self._client = _build_backend()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._client.close()

    def find_application(self, name: str):
        apps = self._client.call("app.query")
        filtered = list(filter(lambda app: app.get("name") == name, apps))
        if len(filtered) == 1:
            return filtered[0]
        else:
            return None

    def create_app(self, name: str, compose_config: dict):
        app = self._client.call(
            "app.create",
            {
                "app_name": name,
                "custom_app": True,
                "custom_compose_config": compose_config,
            },
            job=True,
        )
        return app

    def update_app(self, name: str, compose_config: dict):
        app = self._client.call(
            "app.update",
            name,
            {
                "custom_compose_config": compose_config,
            },
            job=True,
        )
        return app

    def delete_app(self, name: str):
        app = self._client.call("app.delete", name, job=True)
        return app

    def stop_app(self, name: str):
        app = self._client.call("app.stop", name, job=True)
        return app

    def start_app(self, name: str):
        app = self._client.call("app.start", name, job=True)
        return app


class _StubApiClient:
    """File-backed stub used for ansible-test integration runs."""

    def __init__(self):
        workspace = os.environ.get("TRUENAS_STUB_WORKSPACE")
        if workspace:
            workspace_path = Path(workspace)
            workspace_path.mkdir(parents=True, exist_ok=True)
            state_path = workspace_path / "state.json"
        else:
            state_path = Path(
                os.environ.get("TRUENAS_STUB_STATE", "/tmp/truenas_stub_state.json")
            )
        state_path.parent.mkdir(parents=True, exist_ok=True)
        self._state_path = state_path
        app_root = Path(
            os.environ.get("TRUENAS_APP_CONFIG_ROOT", "/mnt/.ix-apps/app_configs")
        )
        app_root.mkdir(parents=True, exist_ok=True)
        self._app_root = app_root

    def close(self):
        return None

    def call(self, method: str, *args: Any, **kwargs: Any):
        state = self._load_state()
        if method == "app.query":
            return [dict(app) for app in state["apps"]]
        if method == "app.create":
            payload = args[0]
            return self._create_app(state, payload)
        if method == "app.update":
            name = args[0]
            payload = args[1]
            return self._update_app(state, name, payload)
        if method == "app.delete":
            name = args[0]
            return self._delete_app(state, name)
        if method == "app.stop":
            name = args[0]
            return self._set_state(state, name, "STOPPED")
        if method == "app.start":
            name = args[0]
            return self._set_state(state, name, "DEPLOYING")
        raise ValueError("Unsupported stub call: {}".format(method))

    def _create_app(self, state: Dict[str, Any], payload: Dict[str, Any]):
        apps = state["apps"]
        name = payload["app_name"]
        if any(app["name"] == name for app in apps):
            raise ValueError("Application '{}' already exists".format(name))
        version = payload.get("version") or "1"
        compose_config = payload.get("custom_compose_config", {})
        app = {
            "name": name,
            "custom_app": payload.get("custom_app", True),
            "version": version,
            "state": "DEPLOYING",
        }
        apps.append(app)
        self._write_state(state)
        self._write_user_config(name, version, compose_config)
        return dict(app)

    def _update_app(self, state: Dict[str, Any], name: str, payload: Dict[str, Any]):
        compose_config = payload.get("custom_compose_config", {})
        apps = state["apps"]
        for app in apps:
            if app["name"] == name:
                version = app.get("version") or "1"
                app["state"] = "UPDATING"
                self._write_state(state)
                self._write_user_config(name, version, compose_config)
                return dict(app)
        raise ValueError("Application '{}' not found".format(name))

    def _delete_app(self, state: Dict[str, Any], name: str):
        apps = state["apps"]
        remaining = [app for app in apps if app["name"] != name]
        state["apps"] = remaining
        self._write_state(state)
        return {"name": name, "state": "DELETING"}

    def _set_state(self, state: Dict[str, Any], name: str, value: str):
        for app in state["apps"]:
            if app["name"] == name:
                app["state"] = value
                self._write_state(state)
                return dict(app)
        raise ValueError("Application '{}' not found".format(name))

    def _write_user_config(self, name: str, version: str, compose: Dict[str, Any]):
        if yaml is None:
            raise ModuleNotFoundError("PyYAML is required to serialize compose manifests.")
        target = self._app_root / name / "versions" / str(version) / "user_config.yaml"
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(compose or {}, handle)

    def _load_state(self) -> Dict[str, Any]:
        if self._state_path.exists():
            with self._state_path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        return {"apps": []}

    def _write_state(self, state: Dict[str, Any]):
        with self._state_path.open("w", encoding="utf-8") as handle:
            json.dump(state, handle)
