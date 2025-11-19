.. Created with antsibull-docs 2.22.0

mareckii.truenas_scale.app module -- Manage TrueNAS SCALE applications
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `mareckii.truenas_scale collection <https://galaxy.ansible.com/ui/repo/published/mareckii/truenas_scale/>`_ (version 0.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible\-galaxy collection install mareckii.truenas\_scale`.

To use it in a playbook, specify: ``mareckii.truenas_scale.app``.


.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Create or reconcile TrueNAS SCALE applications backed by custom compose deployments.
- Catalog\-driven applications are not supported because the underlying API does not expose the methods required to manage marketplace apps yet.








Parameters
----------

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th><p>Parameter</p></th>
    <th><p>Comments</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-compose_config"></div>
      <p style="display: inline;"><strong>compose_config</strong></p>
      <a class="ansibleOptionLink" href="#parameter-compose_config" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>Desired docker compose configuration that should be applied to the custom application.</p>
      <p>This must follow the same structure that TrueNAS expects for custom compose deployments.</p>
      <p>Required when <code class='docutils literal notranslate'>state=present</code>.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-name"></div>
      <p style="display: inline;"><strong>name</strong></p>
      <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>
    </td>
    <td valign="top">
      <p>Name of the TrueNAS application instance to manage.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-state"></div>
      <p style="display: inline;"><strong>state</strong></p>
      <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Whether the custom application should exist.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>&#34;present&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>&#34;absent&#34;</code></p></li>
        <li><p><code>&#34;restarted&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  </tbody>
  </table>




Attributes
----------

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Attribute
    - Support
    - Description

  * - .. _ansible_collections.mareckii.truenas_scale.app_module__attribute-check_mode:

      **check_mode**

    - Support: full



    -
      Can run in check\_mode and return changed status prediction without modifying target, if not supported the action will be skipped.



  * - .. _ansible_collections.mareckii.truenas_scale.app_module__attribute-diff_mode:

      **diff_mode**

    - Support: full



    -
      Will return details on what has changed (or possibly needs changing in check\_mode), when in diff mode



  * - .. _ansible_collections.mareckii.truenas_scale.app_module__attribute-platform:

      **platform**

    - Platform:Linux


    -
      Target OS/families that can be operated against






Examples
--------

.. code-block:: yaml

    - name: Ensure a Redis custom application exists (playbook task)
      mareckii.truenas_scale.app:
        name: redis
        compose_config:
          services:
            redis:
              image: redis:alpine

    - name: Remove a custom application
      mareckii.truenas_scale.app:
        name: redis
        state: absent

    - name: Restart a custom application
      mareckii.truenas_scale.app:
        name: redis
        state: restarted

    # Equivalent ad-hoc invocation
    # ansible -i inventory.local.yml truenas_test \
    #   -m mareckii.truenas_scale.app \
    #   -a '{"name": "redis", "compose_config": {"services": {"redis": {"image": "redis:alpine"}}}}'




Return Values
-------------
The following are the fields unique to this module:

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th><p>Key</p></th>
    <th><p>Description</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-application"></div>
      <p style="display: inline;"><strong>application</strong></p>
      <a class="ansibleOptionLink" href="#return-application" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>The metadata returned by the TrueNAS API for the matching application.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when the application already exists</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-changed"></div>
      <p style="display: inline;"><strong>changed</strong></p>
      <a class="ansibleOptionLink" href="#return-changed" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>Whether the current compose configuration differs from the requested specification.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> always</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-diff"></div>
      <p style="display: inline;"><strong>diff</strong></p>
      <a class="ansibleOptionLink" href="#return-diff" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>Structured diff containing the current on-device compose configuration and the desired configuration.</p>
      <p>The <code class='docutils literal notranslate'>before</code> value is parsed from <code class='docutils literal notranslate'>user_config.yaml</code>; the <code class='docutils literal notranslate'>after</code> value is the provided compose_config.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when state=present</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-state"></div>
      <p style="display: inline;"><strong>state</strong></p>
      <a class="ansibleOptionLink" href="#return-state" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Final state that was ensured.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> always</p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Marecki (@mareckii)


Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/mareckii/ansible\-collection\-truenas\-scale/issues>`__
* `Repository (Sources) <https://github.com/mareckii/ansible\-collection\-truenas\-scale.git>`__
