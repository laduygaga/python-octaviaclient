#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

"""Load Balancer v2 API Library Tests"""

from keystoneauth1 import session
from oslo_utils import uuidutils
from requests_mock.contrib import fixture

from osc_lib.tests import utils

from octaviaclient.api.v2 import octavia

FAKE_ACCOUNT = 'q12we34r'
FAKE_AUTH = '11223344556677889900'
FAKE_URL = 'http://example.com/v2.0/'
FAKE_LBAAS_URL = FAKE_URL + 'lbaas/'

FAKE_LB = uuidutils.generate_uuid()
FAKE_LI = uuidutils.generate_uuid()
FAKE_PO = uuidutils.generate_uuid()
FAKE_ME = uuidutils.generate_uuid()
FAKE_L7PO = uuidutils.generate_uuid()
FAKE_L7RU = uuidutils.generate_uuid()
FAKE_HM = uuidutils.generate_uuid()
FAKE_PRJ = uuidutils.generate_uuid()


LIST_LB_RESP = {
    'loadbalancers':
        [{'name': 'lb1'},
         {'name': 'lb2'}]
}

LIST_LI_RESP = {
    'listeners':
        [{'name': 'lb1'},
         {'name': 'lb2'}]
}

LIST_PO_RESP = {
    'pools':
        [{'name': 'po1'},
         {'name': 'po2'}]
}

LIST_ME_RESP = {
    'members':
        [{'name': 'mem1'},
         {'name': 'mem2'}]
}

LIST_L7PO_RESP = [
    {'name': 'l71'},
    {'name': 'l72'},
]

LIST_L7RU_RESP = {
    'rules':
        [{'id': uuidutils.generate_uuid()},
         {'id': uuidutils.generate_uuid()}]
}

LIST_HM_RESP = {
    'healthmonitors':
        [{'id': uuidutils.generate_uuid()},
         {'id': uuidutils.generate_uuid()}]
}

LIST_QT_RESP = {
    'quotas':
        [{'health_monitor': -1},
         {'listener': -1},
         {'load_balancer': 5},
         {'member': 10},
         {'pool': 20},
         {'project': uuidutils.generate_uuid()}]
}

SINGLE_LB_RESP = {'loadbalancer': {'id': FAKE_LB, 'name': 'lb1'}}
SINGLE_LB_UPDATE = {"loadbalancer": {"admin_state_up": False}}
SINGLE_LB_STATS_RESP = {'bytes_in': '0'}

SINGLE_LI_RESP = {'listener': {'id': FAKE_LI, 'name': 'li1'}}
SINGLE_LI_UPDATE = {"listener": {"admin_state_up": False}}

SINGLE_PO_RESP = {'pool': {'id': FAKE_PO, 'name': 'li1'}}
SINGLE_PO_UPDATE = {'pool': {'admin_state_up': False}}

SINGLE_L7PO_RESP = {'l7policy': {'id': FAKE_L7PO, 'name': 'l71'}}
SINGLE_L7PO_UPDATE = {'l7policy': {'admin_state_up': False}}

SINGLE_ME_RESP = {'member': {'id': FAKE_ME, 'name': 'mem1'}}
SINGLE_ME_UPDATE = {"member": {"admin_state_up": False}}

SINGLE_L7RU_RESP = {'rule': {'id': FAKE_L7RU}}
SINGLE_L7RU_UPDATE = {'rule': {'admin_state_up': False}}

SINGLE_HM_RESP = {'healthmonitor': {'id': FAKE_ME}}
SINGLE_HM_UPDATE = {'healthmonitor': {'admin_state_up': False}}

SINGLE_QT_RESP = {'quota': {'pool': -1}}
SINGLE_QT_UPDATE = {'quota': {'pool': -1}}


class TestOctaviaClient(utils.TestCase):

    def setUp(self):
        super(TestOctaviaClient, self).setUp()
        sess = session.Session()
        self.api = octavia.OctaviaAPI(session=sess, endpoint=FAKE_URL)
        self.requests_mock = self.useFixture(fixture.Fixture())


class TestLoadBalancer(TestOctaviaClient):

    _error_message = ("Validation failure: Test message.")

    def test_list_load_balancer_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_LBAAS_URL + 'loadbalancers',
            json=LIST_LB_RESP,
            status_code=200,
        )
        ret = self.api.load_balancer_list()
        self.assertEqual(LIST_LB_RESP, ret)

    def test_show_load_balancer(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_LBAAS_URL + 'loadbalancers/' + FAKE_LB,
            json=SINGLE_LB_RESP,
            status_code=200
        )
        ret = self.api.load_balancer_show(FAKE_LB)
        self.assertEqual(SINGLE_LB_RESP['loadbalancer'], ret)

    def test_create_load_balancer(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_LBAAS_URL + 'loadbalancers',
            json=SINGLE_LB_RESP,
            status_code=200
        )
        ret = self.api.load_balancer_create(json=SINGLE_LB_RESP)
        self.assertEqual(SINGLE_LB_RESP, ret)

    def test_create_load_balancer_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_LBAAS_URL + 'loadbalancers',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.load_balancer_create,
                               json=SINGLE_LB_RESP)

    def test_set_load_balancer(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_LBAAS_URL + 'loadbalancers/' + FAKE_LB,
            json=SINGLE_LB_UPDATE,
            status_code=200
        )
        ret = self.api.load_balancer_set(FAKE_LB, json=SINGLE_LB_UPDATE)
        self.assertEqual(SINGLE_LB_UPDATE, ret)

    def test_set_load_balancer_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_LBAAS_URL + 'loadbalancers/' + FAKE_LB,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.load_balancer_set,
                               FAKE_LB,
                               json=SINGLE_LB_UPDATE)

    def test_failover_load_balancer(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_LBAAS_URL + 'loadbalancers/' + FAKE_LB + '/failover',
            status_code=202,
        )
        ret = self.api.load_balancer_failover(FAKE_LB)
        self.assertEqual(202, ret.status_code)

    def test_failover_load_balancer_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_LBAAS_URL + 'loadbalancers/' + FAKE_LB + '/failover',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=409,
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.load_balancer_failover,
                               FAKE_LB)

    def test_delete_load_balancer(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_LBAAS_URL + 'loadbalancers/' + FAKE_LB,
            status_code=200
        )
        ret = self.api.load_balancer_delete(FAKE_LB)
        self.assertEqual(200, ret.status_code)

    def test_delete_load_balancer_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_LBAAS_URL + 'loadbalancers/' + FAKE_LB,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.load_balancer_delete,
                               FAKE_LB)

    def test_stats_show_load_balancer(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_LBAAS_URL + 'loadbalancers/' + FAKE_LB + '/stats',
            json=SINGLE_LB_STATS_RESP,
            status_code=200,
        )
        ret = self.api.load_balancer_stats_show(FAKE_LB)
        self.assertEqual(SINGLE_LB_STATS_RESP, ret)

    def test_list_listeners_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_LBAAS_URL + 'listeners',
            json=LIST_LI_RESP,
            status_code=200,
        )
        ret = self.api.listener_list()
        self.assertEqual(LIST_LI_RESP, ret)

    def test_show_listener(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_LBAAS_URL + 'listeners/' + FAKE_LI,
            json=SINGLE_LI_RESP,
            status_code=200
        )
        ret = self.api.listener_show(FAKE_LI)
        self.assertEqual(SINGLE_LI_RESP['listener'], ret)

    def test_create_listener(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_LBAAS_URL + 'listeners',
            json=SINGLE_LI_RESP,
            status_code=200
        )
        ret = self.api.listener_create(json=SINGLE_LI_RESP)
        self.assertEqual(SINGLE_LI_RESP, ret)

    def test_create_listener_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_LBAAS_URL + 'listeners',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.listener_create,
                               json=SINGLE_LI_RESP)

    def test_set_listeners(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_LBAAS_URL + 'listeners/' + FAKE_LI,
            json=SINGLE_LI_UPDATE,
            status_code=200
        )
        ret = self.api.listener_set(FAKE_LI, json=SINGLE_LI_UPDATE)
        self.assertEqual(SINGLE_LI_UPDATE, ret)

    def test_set_listeners_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_LBAAS_URL + 'listeners/' + FAKE_LI,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.listener_set,
                               FAKE_LI, json=SINGLE_LI_UPDATE)

    def test_delete_listener(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_LBAAS_URL + 'listeners/' + FAKE_LI,
            status_code=200
        )
        ret = self.api.listener_delete(FAKE_LI)
        self.assertEqual(200, ret.status_code)

    def test_delete_listener_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_LBAAS_URL + 'listeners/' + FAKE_LI,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.listener_delete,
                               FAKE_LI)

    def test_stats_show_listener(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_LBAAS_URL + 'listeners/' + FAKE_LI + '/stats',
            json=SINGLE_LB_STATS_RESP,
            status_code=200,
        )
        ret = self.api.listener_stats_show(FAKE_LI)
        self.assertEqual(SINGLE_LB_STATS_RESP, ret)

    def test_list_pool_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_LBAAS_URL + 'pools',
            json=LIST_PO_RESP,
            status_code=200,
        )
        ret = self.api.pool_list()
        self.assertEqual(LIST_PO_RESP, ret)

    def test_show_pool(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_LBAAS_URL + 'pools/' + FAKE_PO,
            json=SINGLE_PO_RESP,
            status_code=200
        )
        ret = self.api.pool_show(FAKE_PO)
        self.assertEqual(SINGLE_PO_RESP['pool'], ret)

    def test_create_pool(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_LBAAS_URL + 'pools',
            json=SINGLE_PO_RESP,
            status_code=200
        )
        ret = self.api.pool_create(json=SINGLE_PO_RESP)
        self.assertEqual(SINGLE_PO_RESP, ret)

    def test_create_pool_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_LBAAS_URL + 'pools',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.pool_create,
                               json=SINGLE_PO_RESP)

    def test_set_pool(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_LBAAS_URL + 'pools/' + FAKE_PO,
            json=SINGLE_PO_UPDATE,
            status_code=200
        )
        ret = self.api.pool_set(FAKE_PO, json=SINGLE_PO_UPDATE)
        self.assertEqual(SINGLE_PO_UPDATE, ret)

    def test_set_pool_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_LBAAS_URL + 'pools/' + FAKE_PO,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.pool_set,
                               FAKE_PO, json=SINGLE_PO_UPDATE)

    def test_delete_pool(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_LBAAS_URL + 'pools/' + FAKE_PO,
            status_code=200
        )
        ret = self.api.pool_delete(FAKE_PO)
        self.assertEqual(200, ret.status_code)

    def test_delete_pool_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_LBAAS_URL + 'pools/' + FAKE_PO,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.pool_delete,
                               FAKE_PO)

    def test_list_member_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_LBAAS_URL + 'pools/' + FAKE_PO + '/members',
            json=LIST_ME_RESP,
            status_code=200,
        )
        ret = self.api.member_list(FAKE_PO)
        self.assertEqual(LIST_ME_RESP, ret)

    def test_show_member(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_LBAAS_URL + 'pools/' + FAKE_PO + '/members/' + FAKE_ME,
            json=SINGLE_ME_RESP,
            status_code=200
        )
        ret = self.api.member_show(pool_id=FAKE_PO, member_id=FAKE_ME)
        self.assertEqual(SINGLE_ME_RESP['member'], ret)

    def test_create_member(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_LBAAS_URL + 'pools/' + FAKE_PO + '/members',
            json=SINGLE_ME_RESP,
            status_code=200
        )
        ret = self.api.member_create(json=SINGLE_ME_RESP, pool_id=FAKE_PO)
        self.assertEqual(SINGLE_ME_RESP, ret)

    def test_create_member_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_LBAAS_URL + 'pools/' + FAKE_PO + '/members',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.member_create,
                               json=SINGLE_ME_RESP, pool_id=FAKE_PO)

    def test_set_member(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_LBAAS_URL + 'pools/' + FAKE_PO + '/members/' + FAKE_ME,
            json=SINGLE_ME_UPDATE,
            status_code=200
        )
        ret = self.api.member_set(pool_id=FAKE_PO, member_id=FAKE_ME,
                                  json=SINGLE_ME_UPDATE)
        self.assertEqual(SINGLE_ME_UPDATE, ret)

    def test_set_member_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_LBAAS_URL + 'pools/' + FAKE_PO + '/members/' + FAKE_ME,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.member_set,
                               pool_id=FAKE_PO, member_id=FAKE_ME,
                               json=SINGLE_ME_UPDATE)

    def test_delete_member(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_LBAAS_URL + 'pools/' + FAKE_PO + '/members/' + FAKE_ME,
            status_code=200
        )
        ret = self.api.member_delete(pool_id=FAKE_PO, member_id=FAKE_ME)
        self.assertEqual(200, ret.status_code)

    def test_delete_member_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_LBAAS_URL + 'pools/' + FAKE_PO + '/members/' + FAKE_ME,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.member_delete,
                               pool_id=FAKE_PO, member_id=FAKE_ME)

    def test_list_l7policy_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_LBAAS_URL + 'l7policies',
            json=LIST_L7PO_RESP,
            status_code=200,
        )
        ret = self.api.l7policy_list()
        self.assertEqual(LIST_L7PO_RESP, ret)

    def test_show_l7policy(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_LBAAS_URL + 'l7policies/' + FAKE_L7PO,
            json=SINGLE_L7PO_RESP,
            status_code=200
        )
        ret = self.api.l7policy_show(FAKE_L7PO)
        self.assertEqual(SINGLE_L7PO_RESP['l7policy'], ret)

    def test_create_l7policy(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_LBAAS_URL + 'l7policies',
            json=SINGLE_L7PO_RESP,
            status_code=200
        )
        ret = self.api.l7policy_create(json=SINGLE_L7PO_RESP)
        self.assertEqual(SINGLE_L7PO_RESP, ret)

    def test_create_l7policy_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_LBAAS_URL + 'l7policies',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.l7policy_create,
                               json=SINGLE_L7PO_RESP)

    def test_set_l7policy(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_LBAAS_URL + 'l7policies/' + FAKE_L7PO,
            json=SINGLE_L7PO_UPDATE,
            status_code=200
        )
        ret = self.api.l7policy_set(FAKE_L7PO, json=SINGLE_L7PO_UPDATE)
        self.assertEqual(SINGLE_L7PO_UPDATE, ret)

    def test_set_l7policy_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_LBAAS_URL + 'l7policies/' + FAKE_L7PO,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.l7policy_set,
                               FAKE_L7PO, json=SINGLE_L7PO_UPDATE)

    def test_delete_l7policy(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_LBAAS_URL + 'l7policies/' + FAKE_L7PO,
            status_code=200
        )
        ret = self.api.l7policy_delete(FAKE_L7PO)
        self.assertEqual(200, ret.status_code)

    def test_delete_l7policy_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_LBAAS_URL + 'l7policies/' + FAKE_L7PO,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.l7policy_delete,
                               FAKE_L7PO)

    def test_list_l7rule_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_LBAAS_URL + 'l7policies/' + FAKE_L7PO + '/rules',
            json=LIST_L7RU_RESP,
            status_code=200,
        )
        ret = self.api.l7rule_list(FAKE_L7PO)
        self.assertEqual(LIST_L7RU_RESP, ret)

    def test_show_l7rule(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_LBAAS_URL + 'l7policies/' + FAKE_L7PO + '/rules/' + FAKE_L7RU,
            json=SINGLE_L7RU_RESP,
            status_code=200
        )
        ret = self.api.l7rule_show(FAKE_L7RU, FAKE_L7PO)
        self.assertEqual(SINGLE_L7RU_RESP['rule'], ret)

    def test_create_l7rule(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_LBAAS_URL + 'l7policies/' + FAKE_L7PO + '/rules',
            json=SINGLE_L7RU_RESP,
            status_code=200
        )
        ret = self.api.l7rule_create(FAKE_L7PO, json=SINGLE_L7RU_RESP)
        self.assertEqual(SINGLE_L7RU_RESP, ret)

    def test_create_l7rule_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_LBAAS_URL + 'l7policies/' + FAKE_L7PO + '/rules',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.l7rule_create,
                               FAKE_L7PO, json=SINGLE_L7RU_RESP)

    def test_set_l7rule(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_LBAAS_URL + 'l7policies/' + FAKE_L7PO + '/rules/' + FAKE_L7RU,
            json=SINGLE_L7RU_UPDATE,
            status_code=200
        )
        ret = self.api.l7rule_set(
            l7rule_id=FAKE_L7RU,
            l7policy_id=FAKE_L7PO,
            json=SINGLE_L7RU_UPDATE
        )
        self.assertEqual(SINGLE_L7RU_UPDATE, ret)

    def test_set_l7rule_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_LBAAS_URL + 'l7policies/' + FAKE_L7PO + '/rules/' + FAKE_L7RU,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.l7rule_set,
                               l7rule_id=FAKE_L7RU,
                               l7policy_id=FAKE_L7PO,
                               json=SINGLE_L7RU_UPDATE)

    def test_delete_l7rule(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_LBAAS_URL + 'l7policies/' + FAKE_L7PO + '/rules/' + FAKE_L7RU,
            status_code=200
        )
        ret = self.api.l7rule_delete(
            l7rule_id=FAKE_L7RU,
            l7policy_id=FAKE_L7PO
        )
        self.assertEqual(200, ret.status_code)

    def test_delete_l7rule_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_LBAAS_URL + 'l7policies/' + FAKE_L7PO + '/rules/' + FAKE_L7RU,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.l7rule_delete,
                               l7rule_id=FAKE_L7RU,
                               l7policy_id=FAKE_L7PO)

    def test_list_health_monitor_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_LBAAS_URL + 'healthmonitors',
            json=LIST_HM_RESP,
            status_code=200,
        )
        ret = self.api.health_monitor_list()
        self.assertEqual(LIST_HM_RESP, ret)

    def test_show_health_monitor(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_LBAAS_URL + 'healthmonitors/' + FAKE_HM,
            json=SINGLE_HM_RESP,
            status_code=200
        )
        ret = self.api.health_monitor_show(FAKE_HM)
        self.assertEqual(SINGLE_HM_RESP['healthmonitor'], ret)

    def test_create_health_monitor(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_LBAAS_URL + 'healthmonitors',
            json=SINGLE_HM_RESP,
            status_code=200
        )
        ret = self.api.health_monitor_create(json=SINGLE_HM_RESP)
        self.assertEqual(SINGLE_HM_RESP, ret)

    def test_create_health_monitor_error(self):
        self.requests_mock.register_uri(
            'POST',
            FAKE_LBAAS_URL + 'healthmonitors',
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.health_monitor_create,
                               json=SINGLE_HM_RESP)

    def test_set_health_monitor(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_LBAAS_URL + 'healthmonitors/' + FAKE_HM,
            json=SINGLE_HM_UPDATE,
            status_code=200
        )
        ret = self.api.health_monitor_set(FAKE_HM, json=SINGLE_HM_UPDATE)
        self.assertEqual(SINGLE_HM_UPDATE, ret)

    def test_set_health_monitor_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_LBAAS_URL + 'healthmonitors/' + FAKE_HM,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.health_monitor_set,
                               FAKE_HM, json=SINGLE_HM_UPDATE)

    def test_delete_health_monitor(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_LBAAS_URL + 'healthmonitors/' + FAKE_HM,
            status_code=200
        )
        ret = self.api.health_monitor_delete(FAKE_HM)
        self.assertEqual(200, ret.status_code)

    def test_delete_health_monitor_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_LBAAS_URL + 'healthmonitors/' + FAKE_HM,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.health_monitor_delete,
                               FAKE_HM)

    def test_list_quota_no_options(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_LBAAS_URL + 'quotas',
            json=LIST_QT_RESP,
            status_code=200,
        )
        ret = self.api.quota_list()
        self.assertEqual(LIST_QT_RESP, ret)

    def test_show_quota(self):
        self.requests_mock.register_uri(
            'GET',
            FAKE_LBAAS_URL + 'quotas/' + FAKE_PRJ,
            json=SINGLE_QT_RESP,
            status_code=200
        )
        ret = self.api.quota_show(FAKE_PRJ)
        self.assertEqual(SINGLE_QT_RESP['quota'], ret)

    def test_set_quota(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_LBAAS_URL + 'quotas/' + FAKE_PRJ,
            json=SINGLE_QT_UPDATE,
            status_code=200
        )
        ret = self.api.quota_set(FAKE_PRJ, json=SINGLE_QT_UPDATE)
        self.assertEqual(SINGLE_QT_UPDATE, ret)

    def test_set_quota_error(self):
        self.requests_mock.register_uri(
            'PUT',
            FAKE_LBAAS_URL + 'quotas/' + FAKE_PRJ,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.quota_set,
                               FAKE_PRJ, json=SINGLE_QT_UPDATE)

    def test_reset_quota(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_LBAAS_URL + 'quotas/' + FAKE_PRJ,
            status_code=200
        )
        ret = self.api.quota_reset(FAKE_PRJ)
        self.assertEqual(200, ret.status_code)

    def test_reset_quota_error(self):
        self.requests_mock.register_uri(
            'DELETE',
            FAKE_LBAAS_URL + 'quotas/' + FAKE_PRJ,
            text='{"faultstring": "%s"}' % self._error_message,
            status_code=400
        )
        self.assertRaisesRegex(octavia.OctaviaClientException,
                               self._error_message,
                               self.api.quota_reset,
                               FAKE_PRJ)
