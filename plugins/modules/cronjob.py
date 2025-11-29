#!/usr/bin/python
# Copyright: (c) 2024, Marek Marecki (@mareckii)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
module: cronjob
short_description: Manage TrueNAS SCALE cron jobs
description:
  - Create, update, or remove cron jobs on TrueNAS SCALE systems.
  - The module focuses on idempotent management of the cron job metadata exposed through the API.
options:
  name:
    description:
      - Description of the cron job. This value must be unique on the TrueNAS node.
    type: str
    required: true
  command:
    description:
      - Shell command executed by the cron job.
      - Required when C(state=present).
    type: str
  user:
    description:
      - Account that should run the cron job.
    type: str
    default: root
  enabled:
    description:
      - Whether the cron job should be enabled.
    type: bool
    default: true
  schedule:
    description:
      - Cron schedule definition. Any omitted value defaults to C(*).
    type: dict
    suboptions:
      minute:
        description:
          - Minute component of the cron schedule.
        type: str
      hour:
        description:
          - Hour component of the cron schedule.
        type: str
      dom:
        description:
          - Day of month component of the cron schedule.
        type: str
      month:
        description:
          - Month component of the cron schedule.
        type: str
      dow:
        description:
          - Day of week component of the cron schedule.
        type: str
  state:
    description:
      - Whether the cron job should exist.
    type: str
    choices:
      - present
      - absent
    default: present
author:
  - Marek Marecki (@mareckii)
extends_documentation_fragment:
  - ansible.builtin.action_common_attributes
attributes:
  check_mode:
    support: full
  diff_mode:
    support: full
  platform:
    platforms:
      - Linux
"""

EXAMPLES = r"""
- name: Ensure database backup job exists
  mareckii.truenas_scale.cronjob:
    name: nightly backup
    command: /usr/local/bin/backup.sh
    user: root
    schedule:
      minute: "0"
      hour: "2"

- name: Disable a cron job
  mareckii.truenas_scale.cronjob:
    name: nightly backup
    enabled: false

- name: Remove an obsolete cron job
  mareckii.truenas_scale.cronjob:
    name: old job
    state: absent
"""

RETURN = r"""
cronjob:
  description: The cron job record returned by the TrueNAS API.
  returned: always
  type: dict
changed:
  description: Indicates whether the cron job definition was modified.
  returned: always
  type: bool
diff:
  description:
    - Structured diff showing the before and after state of the cron job metadata.
  returned: when state=present
  type: dict
state:
  description: Final state that was ensured.
  returned: always
  type: str
message:
  description: Human readable summary of the action taken.
  returned: always
  type: str
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mareckii.truenas_scale.plugins.module_utils.cronjobs import (
    CronJobSpec,
)
from ansible_collections.mareckii.truenas_scale.plugins.module_utils.truenas_client import (
    TruenasClient,
)


def _build_module():
    return AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=True),
            command=dict(type="str"),
            user=dict(type="str", default="root"),
            enabled=dict(type="bool", default=True),
            schedule=dict(
                type="dict",
                options=dict(
                    minute=dict(type="str"),
                    hour=dict(type="str"),
                    dom=dict(type="str"),
                    month=dict(type="str"),
                    dow=dict(type="str"),
                ),
            ),
            state=dict(type="str", default="present", choices=["present", "absent"]),
        ),
        required_if=[("state", "present", ["command"])],
        supports_check_mode=True,
    )


def main():
    module = _build_module()
    name = module.params["name"]
    state = module.params["state"]

    with TruenasClient() as client:
        job = client.find_cronjob(name)

        if state == "absent":
            if not job:
                module.exit_json(
                    changed=False,
                    state="absent",
                    message="Cron job '{}' is already absent".format(name),
                    cronjob=None,
                )

            if module.check_mode:
                module.exit_json(
                    changed=True,
                    state="absent",
                    message="Cron job '{}' would be removed".format(name),
                    cronjob=job,
                )

            client.delete_cronjob(job["id"])
            module.exit_json(
                changed=True,
                state="absent",
                message="Cron job '{}' was removed".format(name),
                cronjob=job,
            )

        spec = CronJobSpec.from_module_params(module.params)
        diff = spec.diff(job)

        if not job:
            if module.check_mode:
                module.exit_json(
                    changed=True,
                    state="present",
                    message="Cron job '{}' would be created".format(name),
                    cronjob=None,
                    diff=diff,
                )
            created = client.create_cronjob(spec.to_payload())
            module.exit_json(
                changed=True,
                state="present",
                message="Cron job '{}' was created".format(name),
                cronjob=created,
                diff=diff,
            )

        if spec.matches(job):
            module.exit_json(
                changed=False,
                state="present",
                message="Cron job '{}' is up to date".format(name),
                cronjob=job,
                diff=diff,
            )

        if module.check_mode:
            module.exit_json(
                changed=True,
                state="present",
                message="Cron job '{}' would be updated".format(name),
                cronjob=job,
                diff=diff,
            )

        updated = client.update_cronjob(job["id"], spec.to_payload())
        module.exit_json(
            changed=True,
            state="present",
            message="Cron job '{}' was updated".format(name),
            cronjob=updated,
            diff=diff,
        )


if __name__ == "__main__":
    main()
