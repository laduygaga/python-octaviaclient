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

import copy
import mock

from osc_lib import exceptions

from octaviaclient.osc.v2 import constants
from octaviaclient.osc.v2 import listener
from octaviaclient.tests.unit.osc.v2 import constants as attr_consts
from octaviaclient.tests.unit.osc.v2 import fakes


class TestListener(fakes.TestOctaviaClient):

    def setUp(self):
        super(TestListener, self).setUp()

        self._listener = fakes.createFakeResource('listener')
        self.listener_info = copy.deepcopy(attr_consts.LISTENER_ATTRS)
        self.columns = copy.deepcopy(constants.LISTENER_COLUMNS)

        self.api_mock = mock.Mock()
        self.api_mock.listener_list.return_value = copy.deepcopy(
            {'listeners': [attr_consts.LISTENER_ATTRS]})
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock


class TestListenerList(TestListener):

    def setUp(self):
        super(TestListenerList, self).setUp()
        self.datalist = (tuple(
            attr_consts.LISTENER_ATTRS[k] for k in self.columns),)
        self.cmd = listener.ListListener(self.app, None)

    def test_listener_list_no_options(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.api_mock.listener_list.assert_called_with()
        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))

    def test_listener_list_with_options(self):
        arglist = ['--name', 'rainbarrel']
        verifylist = [('name', 'rainbarrel')]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)
        self.api_mock.listener_list.assert_called_with(name='rainbarrel')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist, tuple(data))


class TestListenerDelete(TestListener):

    def setUp(self):
        super(TestListenerDelete, self).setUp()
        self.cmd = listener.DeleteListener(self.app, None)

    def test_listener_delete(self):
        arglist = [self._listener.id]
        verifylist = [
            ('listener', self._listener.id)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_delete.assert_called_with(
            listener_id=self._listener.id)

    def test_listener_delete_failure(self):
        arglist = ['unknown_lb']
        verifylist = [
            ('listener', 'unknown_lb')
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.assertRaises(exceptions.CommandError, self.cmd.take_action,
                          parsed_args)
        self.assertNotCalled(self.api_mock.listener_delete)


class TestListenerCreate(TestListener):

    def setUp(self):
        super(TestListenerCreate, self).setUp()
        self.api_mock.listener_create.return_value = {
            'listener': self.listener_info}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = listener.CreateListener(self.app, None)

    @mock.patch('octaviaclient.osc.v2.utils.get_listener_attrs')
    def test_listener_create(self, mock_client):
        mock_client.return_value = self.listener_info
        arglist = ['mock_lb_id',
                   '--name', self._listener.name,
                   '--protocol', 'HTTP',
                   '--protocol-port', '80']
        verifylist = [
            ('loadbalancer', 'mock_lb_id'),
            ('name', self._listener.name),
            ('protocol', 'HTTP'),
            ('protocol_port', '80')
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_create.assert_called_with(
            json={'listener': self.listener_info})

    @mock.patch('octaviaclient.osc.v2.utils.get_listener_attrs')
    def test_tls_listener_create(self, mock_client):
        mock_client.return_value = self.listener_info
        arglist = ['mock_lb_id',
                   '--name', self._listener.name,
                   '--protocol', 'TERMINATED_HTTPS'.lower(),
                   '--protocol-port', '443',
                   '--sni-container-refs',
                   self._listener.sni_container_refs[0],
                   self._listener.sni_container_refs[1],
                   '--default-tls-container-ref',
                   self._listener.default_tls_container_ref]
        verifylist = [
            ('loadbalancer', 'mock_lb_id'),
            ('name', self._listener.name),
            ('protocol', 'TERMINATED_HTTPS'),
            ('protocol_port', '443'),
            ('sni_container_refs', self._listener.sni_container_refs),
            ('default_tls_container_ref',
             self._listener.default_tls_container_ref)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_create.assert_called_with(
            json={'listener': self.listener_info})


class TestListenerShow(TestListener):

    def setUp(self):
        super(TestListenerShow, self).setUp()
        self.api_mock.listener_show.return_value = self.listener_info
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock

        self.cmd = listener.ShowListener(self.app, None)

    def test_listener_show(self):
        arglist = [self._listener.id]
        verifylist = [
            ('listener', self._listener.id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_show.assert_called_with(
            listener_id=self._listener.id)


class TestListenerSet(TestListener):

    def setUp(self):
        super(TestListenerSet, self).setUp()
        self.cmd = listener.SetListener(self.app, None)

    def test_listener_set(self):
        arglist = [self._listener.id, '--name', 'new_name',
                   '--sni-container-refs',
                   self._listener.sni_container_refs[0],
                   self._listener.sni_container_refs[1],
                   '--default-tls-container-ref',
                   self._listener.default_tls_container_ref]
        verifylist = [
            ('listener', self._listener.id),
            ('name', 'new_name'),
            ('sni_container_refs', self._listener.sni_container_refs),
            ('default_tls_container_ref',
                self._listener.default_tls_container_ref)
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_set.assert_called_with(
            self._listener.id, json={
                'listener': {
                    'name': 'new_name',
                    'sni_container_refs': self._listener.sni_container_refs,
                    'default_tls_container_ref':
                        self._listener.default_tls_container_ref
                }})


class TestListenerStatsShow(TestListener):

    def setUp(self):
        super(TestListenerStatsShow, self).setUp()
        listener_stats_info = {'stats': {'bytes_in': '0'}}
        self.api_mock.listener_stats_show.return_value = {
            'stats': listener_stats_info['stats']}
        lb_client = self.app.client_manager
        lb_client.load_balancer = self.api_mock
        self.cmd = listener.ShowListenerStats(self.app, None)

    def test_listener_stats_show(self):
        arglist = [self._listener.id]
        verifylist = [
            ('listener', self._listener.id),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        self.cmd.take_action(parsed_args)
        self.api_mock.listener_stats_show.assert_called_with(
            listener_id=self._listener.id)
