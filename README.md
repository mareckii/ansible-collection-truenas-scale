# ansible-collection-truenas-scale

Ansible collection that automates management of TrueNAS SCALE resources. The initial release focuses on applications, providing the `mareckii.truenas_scale.app` module to create, update, and remove custom compose deployments via the SCALE API. Catalog applications are not supported yet because the upstream API does not expose those operations. The collection is structured to grow with additional modules, roles, and documentation as more SCALE features are automated.

## Features

- **Custom applications** – declaratively ensure custom compose deployments exist with the desired configuration, view diffs, and remove apps when they are no longer needed.
- **Reusable client utilities** – shared module utils encapsulate API access patterns so new modules can be added quickly.
- **Integration-first design** – modules follow Ansible best practices (idempotent, check mode aware) so they drop cleanly into existing playbooks.
- **Direct middleware access** – modules connect to the TrueNAS SCALE middleware over SSH and require sudo privileges. Compose content is still fetched from on-box files (`user_config.yaml`) because the API does not expose it yet.

## Documentation

- [Module docs](docs/) contain rendered documentation for each plugin once published.
- [Testing guide](TESTING.md) explains how to run unit and live integration suites, including the `.vm_target` workflow.

## Getting started

Until the collection is published to Galaxy you can install it straight from GitHub:

```bash
ansible-galaxy collection install git@github.com:mareckii/ansible-collection-truenas-scale.git
```

Once installed, call the modules directly from your playbooks:

```yaml
- name: Deploy redis custom application
  mareckii.truenas_scale.app:
    name: redis
    compose_config:
      services:
        redis:
          image: redis:alpine
```

## Development quickstart

Use the provided `Makefile` when hacking on the collection:

- `make unit` runs all unit tests locally with the configured Python version (defaults to 3.11).
- `make integration [target_name]` executes the real TrueNAS SCALE integration suite against the host defined in `.vm_target` (format: `user@host`). If you omit the target name the entire suite runs; otherwise pass the integration alias you want to focus on. Every run talks to a live VM—no Docker-only stubs remain.
