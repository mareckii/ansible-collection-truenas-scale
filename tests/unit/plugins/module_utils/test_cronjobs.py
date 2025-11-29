from ansible_collections.mareckii.truenas_scale.plugins.module_utils import cronjobs


def test_schedule_defaults_to_wildcards():
    schedule = cronjobs.CronSchedule.from_mapping({})
    assert schedule.to_api() == {
        "minute": "*",
        "hour": "*",
        "dom": "*",
        "month": "*",
        "dow": "*",
    }


def test_spec_matches_existing_job():
    spec = cronjobs.CronJobSpec.from_module_params(
        {
            "name": "nightly",
            "command": "/bin/true",
            "user": "root",
            "enabled": True,
            "schedule": {"minute": 0, "hour": 2},
        }
    )
    job = {
        "id": 7,
        "description": "nightly",
        "command": "/bin/true",
        "user": "root",
        "enabled": True,
        "schedule": {
            "minute": "0",
            "hour": "2",
            "dom": "*",
            "month": "*",
            "dow": "*",
        },
    }
    assert spec.matches(job)


def test_spec_diff_includes_before_and_after():
    spec = cronjobs.CronJobSpec.from_module_params(
        {"name": "nightly", "command": "/bin/true"}
    )
    diff = spec.diff(None)
    assert diff["before"] is None
    assert diff["after"]["description"] == "nightly"
    assert diff["after"]["schedule"]["minute"] == "*"
