.. ...........................................................................
.. © Copyright IBM Corporation 2020                                          .
.. ...........................................................................

Requirements of managed nodes
=============================

The CMCI tasks in the **IBM® z/OS® CICS® collection** interact with the managed node over an HTTP connection by leveraging the `CMCI REST API`_. Therefore, an SSH connection is not necessary. Instead, you can delegate Ansible tasks to run on the control node, for example, by specifying ``delegate_to: 'localhost'`` for the task in the playbook. For more ways of delegating tasks, see `Controlling where tasks run`_.

Delegating tasks to run on the control node saves you the complexity of configuring an unnecessary SSH connection and installing module dependencies on the remote host.

The requirements of the managed node are as follows:

* IBM CICS V4.2 or later
* A `CMCI connection`_ must be set up in either a CICSplex or a stand-alone CICS region
* Python module dependencies:

  * `requests`_
  * `xmltodict`_

  If you delegate the tasks to run on your localhost, the Python module dependencies need to be installed on your localhost instead. You can install them from CLI:

  .. code-block:: sh

     pip install requests xmltodict

  You can also install them using the playbook. See this sample (link to be added) for an example.

.. _requests:
   https://pypi.org/project/requests/

.. _xmltodict:
   https://pypi.org/project/xmltodict/


If you use the CICS collection in conjunction with other IBM z/OS collections, you won't be able to delegate all tasks to your localhost. In that case, your managed node must also follow the requirements of those collections, for example, `IBM z/OS core managed node requirements`_.

If you use the CICS collection alone but don't delegate the CICS tasks to your localhost, your managed node must also follow the `IBM z/OS core managed node requirements`_ except that IBM Z Open Automation Utilities (ZOAU) is not required.

.. _z/OS OpenSSH:
   https://www.ibm.com/support/knowledgecenter/SSLTBW_2.2.0/com.ibm.zos.v2r2.e0za100/ch1openssh.htm

.. _CMCI connection:
   https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/configuring/cmci/clientapi_setup.html

.. _CMCI REST API:
   https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/fundamentals/cpsm/cpsm-cmci-restfulapi-overview.html

.. _IBM z/OS core managed node requirements:
   https://ibm.github.io/z_ansible_collections_doc/ibm_zos_core/docs/source/requirements_managed.html
.. _Controlling where tasks run:
   https://docs.ansible.com/ansible/latest/user_guide/playbooks_delegation.html#delegating-tasks
