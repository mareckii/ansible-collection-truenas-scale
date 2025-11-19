# Testing

This collection provides `Makefile` helpers and raw commands for both unit and integration coverage. All tasks manage the virtual environment automatically.

## Unit tests

Use the Makefile convenience target for day-to-day work:

```bash
make unit
```

This runs `ansible-test units --python 3.11 -v` inside `.venv`. To invoke pytest directly (useful when iterating on a single file):

```bash
  .venv/bin/python -m pytest tests/unit/plugins/modules/test_app.py
```


## Integration tests

Integration coverage talks to an actual TrueNAS SCALE VM over SSH. Before running anything:

1. Create a `.vm_target` file at the repo root containing `user@host` for your lab box (for example `truenas_admin@192.168.1.110`). That user must have sudo access because the module reads compose files directly from `/mnt/.ix-apps/...`.
2. Ensure the VM allows SSH with the key/credentials configured on your workstation.

Then run:

```bash
make integration            # run the entire suite
make integration app # run a single target
```

Under the hood this issues:

```
ansible-test integration [target] \
  --allow-unsupported \
  --target "ssh:$(cat .vm_target),python=3.11"
```

Every integration run is against the real VM; there are no Docker substitutes. Use `TRUENAS_LIVE_APP_NAME` if you need to override the application name created during tests.
