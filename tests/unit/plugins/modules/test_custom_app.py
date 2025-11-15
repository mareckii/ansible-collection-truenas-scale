import textwrap
from types import SimpleNamespace

import pytest

from plugins.modules import custom_app


class ModuleExit(Exception):
    def __init__(self, kwargs):
        self.kwargs = kwargs


class ModuleFail(Exception):
    def __init__(self, kwargs):
        self.kwargs = kwargs


class DummyModule:
    def __init__(self, params, check_mode=False):
        self.params = params
        self.check_mode = check_mode

    def exit_json(self, **kwargs):
        raise ModuleExit(kwargs)

    def fail_json(self, **kwargs):
        raise ModuleFail(kwargs)


def _patch_module(monkeypatch, params, check_mode=False):
    module_params = dict(params)
    module_params.setdefault("state", "present")

    monkeypatch.setattr(
        custom_app,
        "AnsibleModule",
        lambda *args, **kwargs: DummyModule(module_params, check_mode=check_mode),
    )


def _write_user_config(tmp_path, app_name, version, text):
    config_dir = tmp_path / app_name / "versions" / version
    config_dir.mkdir(parents=True)
    (config_dir / "user_config.yaml").write_text(text)


def test_custom_app_creates_new_application(monkeypatch):
    params = {
        "name": "redis",
        "compose_config": {"services": {"redis": {"image": "redis:alpine"}}},
    }
    _patch_module(monkeypatch, params)

    instances = []

    class FakeClient:
        def __init__(self):
            instances.append(self)
            self.created_args = None

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def find_application(self, name):
            return None

        def create_custom_app(self, name, compose_config):
            self.created_args = (name, compose_config)
            return SimpleNamespace(name=name, state="DEPLOYING")

        def update_custom_app(self, *args, **kwargs):
            self.updated_args = (args, kwargs)

        def delete_custom_app(self, *args, **kwargs):
            self.deleted_args = (args, kwargs)

    monkeypatch.setattr(custom_app, "TruenasClient", FakeClient)

    with pytest.raises(ModuleExit) as captured:
        custom_app.main()

    result = captured.value.kwargs
    assert result["changed"] is True
    assert result["diff"]["before"] is None
    assert result["diff"]["after"] == params["compose_config"]
    assert result["state"] == "present"
    assert instances[0].created_args == ("redis", params["compose_config"])


def test_custom_app_detects_matching_config(monkeypatch, tmp_path):
    compose = {"services": {"redis": {"image": "redis:alpine"}}}
    params = {"name": "redis", "compose_config": compose}
    _patch_module(monkeypatch, params)

    dump = textwrap.dedent(
        """
        services:
          redis:
            image: redis:alpine
        """
    )
    _write_user_config(tmp_path, "redis", "1.0.0", dump)
    monkeypatch.setenv("TRUENAS_APP_CONFIG_ROOT", str(tmp_path))

    class FakeClient:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def find_application(self, name):
            return {"name": name, "version": "1.0.0", "custom_app": True}

        def update_custom_app(self, *args, **kwargs):
            self.updated_args = (args, kwargs)

        def delete_custom_app(self, *args, **kwargs):
            self.deleted_args = (args, kwargs)

    monkeypatch.setattr(custom_app, "TruenasClient", FakeClient)

    with pytest.raises(ModuleExit) as captured:
        custom_app.main()

    result = captured.value.kwargs
    assert result["changed"] is False
    assert result["diff"]["before"] == compose
    assert result["diff"]["after"] == compose
    assert result["state"] == "present"
    assert result["application"]["name"] == "redis"


def test_custom_app_detects_different_config(monkeypatch, tmp_path):
    current_yaml = textwrap.dedent(
        """
        services:
          redis:
            image: redis:alpine
        """
    )
    desired = {"services": {"redis": {"image": "redis:7"}}}
    params = {"name": "redis", "compose_config": desired}
    _patch_module(monkeypatch, params)
    _write_user_config(tmp_path, "redis", "1.0", current_yaml)
    monkeypatch.setenv("TRUENAS_APP_CONFIG_ROOT", str(tmp_path))

    class FakeClient:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def find_application(self, name):
            return {"name": name, "version": "1.0", "custom_app": True}

        def update_custom_app(self, name, compose_config):
            self.updated_args = (name, compose_config)

        def delete_custom_app(self, *args, **kwargs):
            self.deleted_args = (args, kwargs)

    monkeypatch.setattr(custom_app, "TruenasClient", FakeClient)

    with pytest.raises(ModuleExit) as captured:
        custom_app.main()

    result = captured.value.kwargs
    assert result["changed"] is True
    assert result["diff"]["before"]["services"]["redis"]["image"] == "redis:alpine"
    assert result["diff"]["after"]["services"]["redis"]["image"] == "redis:7"
    assert "compose config differs" in result["message"]
    assert result["state"] == "present"


def test_custom_app_absent_when_missing(monkeypatch):
    params = {"name": "redis", "state": "absent"}
    _patch_module(monkeypatch, params)

    class FakeClient:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def find_application(self, name):
            return None

    monkeypatch.setattr(custom_app, "TruenasClient", FakeClient)

    with pytest.raises(ModuleExit) as captured:
        custom_app.main()

    result = captured.value.kwargs
    assert result["changed"] is False
    assert result["state"] == "absent"
    assert "already absent" in result["message"]


def test_custom_app_absent_deletes_application(monkeypatch):
    params = {"name": "redis", "state": "absent"}
    _patch_module(monkeypatch, params)
    instances = []

    class FakeClient:
        def __init__(self):
            instances.append(self)
            self.deleted = None

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def find_application(self, name):
            return {"name": name, "version": "1.0", "custom_app": True}

        def delete_custom_app(self, name):
            self.deleted = name

        def update_custom_app(self, *args, **kwargs):
            self.updated_args = (args, kwargs)

    monkeypatch.setattr(custom_app, "TruenasClient", FakeClient)

    with pytest.raises(ModuleExit) as captured:
        custom_app.main()

    result = captured.value.kwargs
    assert result["changed"] is True
    assert result["state"] == "absent"
    assert "was removed" in result["message"]
    assert instances[0].deleted == "redis"
