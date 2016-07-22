########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

# Built-in Imports
import os
import tempfile
from subprocess import Popen, PIPE

# Third-party Imports

# Cloudify imports
from cloudify import ctx
from cloudify import exceptions


def get_playbook_path(playbook):
    try:
        path_to_file = ctx.download_resource(playbook)
    except exceptions.HttpException as e:
        raise exceptions.NonRecoverableError(
            'Could not get playbook file: {}.'.format(str(e)))
    return path_to_file


def get_inventory_path(inventory):
    if not inventory:
        inventory.append(ctx.instance.host_ip)
    _, path_to_file = tempfile.mkstemp()
    with open(path_to_file, 'w') as f:
        for host in inventory:
            f.write('{0}\n'.format(host))
    return path_to_file


def run_command(command):
    try:
        run = Popen(command, stdout=PIPE)
    except Exception as e:
        raise exceptions.NonRecoverableError(
            'Unable to run command. Error {}'.format(str(e)))
    try:
        output = run.communicate()
    except Exception as e:
        raise exceptions.NonRecoverableError(
            'Unable to run command. Error {}'.format(str(e)))
    if run.returncode != 0:
        raise exceptions.NonRecoverableError(
            'Non-zero returncode. Output {}.'.format(output))
    return output
