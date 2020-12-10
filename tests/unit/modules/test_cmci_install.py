# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.modules import cmci_install
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.cmci_helper import (
    HOST, PORT, CONTEXT, SCOPE, od, create_records_response, body_matcher, cmci_module, CMCITestHelper
)


def test_csd_install(cmci_module):  # type: (CMCITestHelper) -> None
    record = dict(
        name='bar',
        bundledir='/u/bundles/bloop',
        csdgroup='bat'
    )
    cmci_module.stub_records(
        'PUT',
        'cicsdefinitionbundle',
        records=[record],
        scope='IYCWEMW2',
        parameters='?PARAMETER=CSDGROUP%28%2A%29',
        additional_matcher=body_matcher(od(
            ('request', od(
                ('action', od(
                    ('@name', 'CSDINSTALL')
                ))
            ))
        ))
    )

    cmci_module.expect({
        'changed': True,
        'request': {
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
                   'cicsdefinitionbundle/CICSEX56/IYCWEMW2',
            'method': 'PUT',
            'params': {'PARAMETER': 'CSDGROUP(*)'},
            'body': '<request><action name="CSDINSTALL"></action></request>'
        },
        'response': {
            'body': create_records_response('cicsdefinitionbundle', [record]),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run(cmci_install, dict(
        cmci_host=HOST,
        cmci_port=PORT,
        context=CONTEXT,
        scope='IYCWEMW2',
        resource=dict(
            type='cicsdefinitionbundle',
            location='CSD'
        ),
        parameter='CSDGROUP(*)'
    ))


def test_bas_install(cmci_module):  # type: (CMCITestHelper) -> None
    record = dict(
        name='bar',
        bundledir='/u/bundles/bloop',
        csdgroup='bat'
    )
    cmci_module.stub_records(
        'PUT',
        'cicsdefinitionbundle',
        [record],
        additional_matcher=body_matcher(od(
            ('request', od(
                ('action', od(
                    ('@name', 'INSTALL')
                ))
            ))
        ))
    )

    cmci_module.expect({
        'changed': True,
        'request': {
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
                   'cicsdefinitionbundle/CICSEX56/',
            'method': 'PUT',
            'body': '<request><action name="INSTALL"></action></request>'
        },
        'response': {
            'body':
                create_records_response('cicsdefinitionbundle', [record]),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run(cmci_install, dict(
        cmci_host=HOST,
        cmci_port=PORT,
        context=CONTEXT,
        resource=dict(
            type='cicsdefinitionbundle',
            location='BAS'
        )
    ))


def test_install_csd_criteria_parameter(cmci_module):  # type: (CMCITestHelper) -> None
    # TODO: The parameters field for criteria is intentionally stubbing a bad request here. The "+'s" will be
    # removed in a future fix
    record = dict(
        changeagent='CSDAPI',
        changeagrel='0730',
        csdgroup='DUMMY',
        name='DUMMY'
    )
    cmci_module.stub_records(
        'PUT',
        'cicsdefinitionprogram',
        [record],
        scope=SCOPE,
        parameters='?CRITERIA=%28%28NAME%3DDUMMY%29+AND+%28DEFVER%3D0%29+AND+'
                   '%28CSDGROUP%3DDUMMY%29%29&PARAMETER=CSDGROUP%28DUMMY%29',
        additional_matcher=body_matcher(od(
            ('request', od(
                ('action', od(
                    ('@name', 'CSDINSTALL')
                ))
            ))
        ))
    )

    cmci_module.expect({
        'changed': True,
        'request': {
            'body':
                '<request>'
                '<action name="CSDINSTALL"></action>'
                '</request>',
            'method': 'PUT',
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicsdefinitionprogram/CICSEX56/IYCWEMW2',
            'params': {
                'PARAMETER': 'CSDGROUP(DUMMY)',
                'CRITERIA': '((NAME=DUMMY) AND (DEFVER=0) AND (CSDGROUP=DUMMY))'
            }
        },
        'response': {
            'body': create_records_response('cicsdefinitionprogram', [record]),
            'reason': 'OK',
            'status_code': 200}
    })

    cmci_module.run(cmci_install, dict(
        cmci_host=HOST,
        cmci_port=PORT,
        context=CONTEXT,
        scope=SCOPE,
        security_type='none',
        resource=dict(
            type='cicsdefinitionprogram',
            location='CSD',
        ),
        criteria="((NAME=DUMMY) AND (DEFVER=0) AND (CSDGROUP=DUMMY))",
        parameter='CSDGROUP(DUMMY)'
    ))