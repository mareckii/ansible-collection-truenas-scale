.. Created with antsibull-docs 2.22.0

mareckii.truenas_scale.cronjob module -- Manage TrueNAS SCALE cron jobs
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `mareckii.truenas_scale collection <https://galaxy.ansible.com/ui/repo/published/mareckii/truenas_scale/>`_ (version 0.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible\-galaxy collection install mareckii.truenas\_scale`.

To use it in a playbook, specify: ``mareckii.truenas_scale.cronjob``.


.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Create, update, or remove cron jobs on TrueNAS SCALE systems.
- The module focuses on idempotent management of the cron job metadata exposed through the API.








Parameters
----------

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th colspan="2"><p>Parameter</p></th>
    <th><p>Comments</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-command"></div>
      <p style="display: inline;"><strong>command</strong></p>
      <a class="ansibleOptionLink" href="#parameter-command" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Shell command executed by the cron job.</p>
      <p>Required when <code class='docutils literal notranslate'>state=present</code>.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-enabled"></div>
      <p style="display: inline;"><strong>enabled</strong></p>
      <a class="ansibleOptionLink" href="#parameter-enabled" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>Whether the cron job should be enabled.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code style="color: blue;"><b>true</b></code> <span style="color: blue;">← (default)</span></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-name"></div>
      <p style="display: inline;"><strong>name</strong></p>
      <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>
    </td>
    <td valign="top">
      <p>Description of the cron job. This value must be unique on the TrueNAS node.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-schedule"></div>
      <p style="display: inline;"><strong>schedule</strong></p>
      <a class="ansibleOptionLink" href="#parameter-schedule" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>Cron schedule definition. Any omitted value defaults to <code class='docutils literal notranslate'>*</code>.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-schedule/dom"></div>
      <p style="display: inline;"><strong>dom</strong></p>
      <a class="ansibleOptionLink" href="#parameter-schedule/dom" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Day of month component of the cron schedule.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-schedule/dow"></div>
      <p style="display: inline;"><strong>dow</strong></p>
      <a class="ansibleOptionLink" href="#parameter-schedule/dow" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Day of week component of the cron schedule.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-schedule/hour"></div>
      <p style="display: inline;"><strong>hour</strong></p>
      <a class="ansibleOptionLink" href="#parameter-schedule/hour" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Hour component of the cron schedule.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-schedule/minute"></div>
      <p style="display: inline;"><strong>minute</strong></p>
      <a class="ansibleOptionLink" href="#parameter-schedule/minute" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Minute component of the cron schedule.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-schedule/month"></div>
      <p style="display: inline;"><strong>month</strong></p>
      <a class="ansibleOptionLink" href="#parameter-schedule/month" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Month component of the cron schedule.</p>
    </td>
  </tr>

  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-state"></div>
      <p style="display: inline;"><strong>state</strong></p>
      <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Whether the cron job should exist.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>&#34;present&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>&#34;absent&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-user"></div>
      <p style="display: inline;"><strong>user</strong></p>
      <a class="ansibleOptionLink" href="#parameter-user" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Account that should run the cron job.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">&#34;root&#34;</code></p>
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

  * - .. _ansible_collections.mareckii.truenas_scale.cronjob_module__attribute-check_mode:

      **check_mode**

    - Support: full



    -
      Can run in check\_mode and return changed status prediction without modifying target, if not supported the action will be skipped.



  * - .. _ansible_collections.mareckii.truenas_scale.cronjob_module__attribute-diff_mode:

      **diff_mode**

    - Support: full



    -
      Will return details on what has changed (or possibly needs changing in check\_mode), when in diff mode



  * - .. _ansible_collections.mareckii.truenas_scale.cronjob_module__attribute-platform:

      **platform**

    - Platform:Linux


    -
      Target OS/families that can be operated against






Examples
--------

.. code-block:: yaml

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
      <div class="ansibleOptionAnchor" id="return-changed"></div>
      <p style="display: inline;"><strong>changed</strong></p>
      <a class="ansibleOptionLink" href="#return-changed" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>Indicates whether the cron job definition was modified.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> always</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-cronjob"></div>
      <p style="display: inline;"><strong>cronjob</strong></p>
      <a class="ansibleOptionLink" href="#return-cronjob" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>The cron job record returned by the TrueNAS API.</p>
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
      <p>Structured diff showing the before and after state of the cron job metadata.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when state=present</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-message"></div>
      <p style="display: inline;"><strong>message</strong></p>
      <a class="ansibleOptionLink" href="#return-message" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Human readable summary of the action taken.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> always</p>
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

- Marek Marecki (@mareckii)


Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/mareckii/ansible\-collection\-truenas\-scale/issues>`__
* `Repository (Sources) <https://github.com/mareckii/ansible\-collection\-truenas\-scale.git>`__
