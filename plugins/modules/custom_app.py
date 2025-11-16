#!/usr/bin/python
# Copyright: (c) 2024, Marecki (@mareckii)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: custom_app
short_description: Manage TrueNAS SCALE custom applications
description:
  - Create a new TrueNAS SCALE custom application or report the difference between
    an existing application's current compose configuration and the desired state.
options:
  name:
    description:
      - Name of the TrueNAS application instance to manage.
    type: str
    required: true
  compose_config:
    description:
      - Desired docker compose configuration that should be applied to the custom application.
      - This must follow the same structure that TrueNAS expects for custom compose deployments.
      - Required when C(state=present).
    type: dict
    required: false
  state:
    description:
      - Whether the custom application should exist.
    type: str
    choices:
      - present
      - absent
      - restarted
    default: present
author:
  - Marecki (@mareckii)
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
- name: Ensure a Redis custom application exists (playbook task)
  mareckii.truenas_scale.custom_app:
    name: redis
    compose_config:
      services:
        redis:
          image: redis:alpine

- name: Remove a custom application
  mareckii.truenas_scale.custom_app:
    name: redis
    state: absent

- name: Restart a custom application
  mareckii.truenas_scale.custom_app:
    name: redis
    state: restarted

# Equivalent ad-hoc invocation
# ansible -i inventory.local.yml truenas_test \
#   -m mareckii.truenas_scale.custom_app \
#   -a '{"name": "redis", "compose_config": {"services": {"redis": {"image": "redis:alpine"}}}}'
"""

RETURN = r"""
changed:
  description: Whether the current compose configuration differs from the requested specification.
  returned: always
  type: bool
diff:
  description:
    - Structured diff containing the current on-device compose configuration and the desired configuration.
    - The C(before) value is parsed from C(user_config.yaml); the C(after) value is the provided compose_config.
  returned: when state=present
  type: dict
state:
  description: Final state that was ensured.
  returned: always
  type: str
application:
  description: The metadata returned by the TrueNAS API for the matching application.
  returned: when the application already exists
  type: dict
"""

import os
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - import guard for sanity tests
    yaml = None
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mareckii.truenas_scale.plugins.module_utils.truenas_client import (
    TruenasClient,
)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            compose_config=dict(type='dict', required=False),
            state=dict(default='present', choices=['present', 'absent', 'restarted'], type='str'),
        ),
        required_if=[('state', 'present', ['compose_config'])],
        supports_check_mode=True,
    )
    name = module.params['name']
    compose_config = module.params.get('compose_config')
    state = module.params['state']

    with TruenasClient() as client:
        application = client.find_application(name)
        if application and not application.get('custom_app'):
            module.fail_json(
                msg="Application with name '{}' is not custom_app".format(name)
            )

        if state == 'absent':
            if not application:
                module.exit_json(
                    changed=False,
                    state='absent',
                    message="Application '{}' is already absent".format(name),
                )

            if module.check_mode:
                module.exit_json(
                    changed=True,
                    state='absent',
                    message="Application '{}' would be removed".format(name),
                    application=application,
                )

            client.delete_custom_app(application["name"])
            module.exit_json(
                changed=True,
                state='absent',
                message="Application '{}' was removed".format(name),
                application=application,
            )

        if state == 'restarted':
            if not application:
                module.fail_json(
                    msg="Application '{}' is absent; cannot restart".format(name)
                )

            if module.check_mode:
                module.exit_json(
                    changed=True,
                    state='restarted',
                    message="Application '{}' would be restarted".format(name),
                    application=application,
                )

            client.stop_custom_app(application["name"])
            client.start_custom_app(application["name"])
            module.exit_json(
                changed=True,
                state='restarted',
                message="Application '{}' was restarted".format(name),
                application=application,
            )

        if not application:
            if module.check_mode:
                module.exit_json(
                    changed=True,
                    state='present',
                    message="Application '{}' would be created".format(name),
                    diff={'before': None, 'after': compose_config},
                )

            app = client.create_custom_app(name, compose_config)
            app_name = getattr(app, 'name', None)
            app_state = getattr(app, 'state', None)
            module.exit_json(
                changed=True,
                message='Application with name {} was created with state: {}'.format(
                    app_name or name,
                    app_state or 'unknown',
                ),
                state='present',
                application=app,
                diff={'before': None, 'after': compose_config},
            )

        app_config_root = os.environ.get(
            "TRUENAS_APP_CONFIG_ROOT", "/mnt/.ix-apps/app_configs"
        )
        user_config = (
            Path(app_config_root)
            / application["name"]
            / "versions"
            / application["version"]
            / "user_config.yaml"
        )
        try:
            user_config_text = user_config.read_text()
        except OSError as exc:
            module.fail_json(
                msg="Unable to read {}: {}".format(user_config, exc)
            )

        if yaml is None:
            module.fail_json(msg="The PyYAML python package is required to parse compose configuration.")

        try:
            current_compose = yaml.safe_load(user_config_text) or {}
        except yaml.YAMLError as exc:
            module.fail_json(
                msg="Invalid YAML in {}: {}".format(user_config, exc)
            )

        changed = current_compose != compose_config
        if changed:
            if module.check_mode:
                message = "Application {} would be updated".format(name)
            else:
                client.update_custom_app(application["name"], compose_config)
                message = "Application '{}' compose config differs from desired state".format(
                    application["name"]
                )
        else:
            message = "Application {} is up to date".format(name)

        module.exit_json(
            changed=changed,
            message=message,
            diff={'before': current_compose, 'after': compose_config},
            application=application,
            state='present'
        )


if __name__ == '__main__':
    main()
