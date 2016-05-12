# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from unittest.mock import patch, Mock, ANY
from gns3.modules.qemu.qemu_vm import QemuVM
from gns3.ports.port import Port
from gns3.nios.nio_udp import NIOUDP
from gns3.base_node import BaseNode


def test_qemu_vm_init(local_server, project):

    vm = QemuVM(None, local_server, project)


def test_qemu_vm_setup(qemu_vm, project):

    with patch('gns3.project.Project.post') as mock:
        qemu_vm.setup("/bin/fake", name="VMNAME")
        mock.assert_called_with(ANY,
                                "/nodes",
                                qemu_vm._setupNodeCallback,
                                body={
                                    'name': 'VMNAME',
                                    'properties': {
                                        'linked_clone': True,
                                        'qemu_path': '/bin/fake'
                                    },
                                    'console_type': 'telnet',
                                    'compute_id': 'local',
                                    'node_type': 'qemu'
                                },
                                context={},
                                timeout=120)

        # Callback
        params = {
            "name": "QEMU1",
            "vmname": "VMNAME",
            "project_id": "f91bd115-3b5c-402e-b411-e5919723cf4b",
            "node_id": "aec7a00c-e71c-45a6-8c04-29e40732883c",
            "vm_directory": "/tmp/test",
            "hda_disk_image": "0cc175b9c0f1b6a831c399e269772661"
        }
        qemu_vm._setupNodeCallback(params)
        assert qemu_vm.node_id() == "aec7a00c-e71c-45a6-8c04-29e40732883c"
        assert qemu_vm.nodeDir() == "/tmp/test"


def test_qemu_vm_setup_command_line(qemu_vm, project):

    with patch('gns3.project.Project.post') as mock:
        qemu_vm.setup("/bin/fake", name="VMNAME")
        mock.assert_called_with(ANY,
                                "/nodes",
                                qemu_vm._setupNodeCallback,
                                body={
                                    'name': 'VMNAME',
                                    'properties': {
                                        'linked_clone': True,
                                        'qemu_path': '/bin/fake'
                                    },
                                    'console_type': 'telnet',
                                    'compute_id': 'local',
                                    'node_type': 'qemu'
                                },
                                context={},
                                timeout=120)

        # Callback
        params = {
            "name": "QEMU1",
            "vmname": "VMNAME",
            "project_id": "f91bd115-3b5c-402e-b411-e5919723cf4b",
            "node_id": "aec7a00c-e71c-45a6-8c04-29e40732883c",
            "vm_directory": "/tmp/test",
            "hda_disk_image": "0cc175b9c0f1b6a831c399e269772661",
            "command_line": "/bin/fake"
        }
        qemu_vm._setupNodeCallback(params)
        assert qemu_vm.node_id() == "aec7a00c-e71c-45a6-8c04-29e40732883c"
        assert qemu_vm.commandLine() == "/bin/fake"


def test_qemu_vm_setup_md5_missing(qemu_vm, project):

    with patch('gns3.project.Project.post') as mock:
        qemu_vm.setup("/bin/fake", name="VMNAME")
        mock.assert_called_with(ANY,
                                "/nodes",
                                qemu_vm._setupNodeCallback,
                                body={
                                    'name': 'VMNAME',
                                    'properties': {
                                        'linked_clone': True,
                                        'qemu_path': '/bin/fake'
                                    },
                                    'compute_id': 'local',
                                    'node_type': 'qemu',
                                    'console_type': 'telnet'
                                },
                                context={},
                                timeout=120)

        # Callback
        params = {
            "name": "QEMU1",
            "vmname": "VMNAME",
            "project_id": "f91bd115-3b5c-402e-b411-e5919723cf4b",
            "node_id": "aec7a00c-e71c-45a6-8c04-29e40732883c",
            "hda_disk_image": "0cc175b9c0f1b6a831c399e269772661"
        }
        with patch("gns3.image_manager.ImageManager.addMissingImage") as mock:
            qemu_vm._setupNodeCallback(params)
            assert mock.called

        assert qemu_vm.node_id() == "aec7a00c-e71c-45a6-8c04-29e40732883c"


def test_update(qemu_vm):

    new_settings = {
        "name": "QEMU2",
    }

    with patch('gns3.base_node.BaseNode.controllerHttpPut') as mock:
        qemu_vm.update(new_settings)

        assert mock.called
        args, kwargs = mock.call_args
        assert args[0] == "/nodes/{node_id}".format(node_id=qemu_vm.node_id())
        assert kwargs["body"] == new_settings

        # Callback
        args[1]({"name": "QEMU2"})
