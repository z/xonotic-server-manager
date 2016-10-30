import yaml
import os
from datetime import datetime
from xsms.engines import screen
from xsms.engines import tmux
from xsms.engines import supervisor
"""
Created on Oct 30, 2016
@author: Tyler Mulligan
"""


class ServersCommand:
    """This class handles the `xsms servers` subcommand

    :param conf:
        The conf dictionary from `config.py`
    :type conf: ``dictionary``

    .. note::
        This file is subject to change with the addition of new
        engines until and API has been established.

    """

    def __init__(self, conf):
        self.conf = conf

    def generate_engine_configs(self):
        """
        This method generates **engine** configs
        """
        with open(self.conf['supervisor_conf_template']) as f:
            conf_template = f.read()
            conf_template = '{0}\n\n'.format(conf_template)

        with open(self.conf['supervisor_server_template']) as f:
            server_template = f.read()
            server_template = '{0}\n\n'.format(server_template)

        with open(self.conf['servers_manifest']) as f:
            servers = yaml.load(f)

        current_date = datetime.now()

        supervisor_data = '# Last Generated: {}\n' \
                          '{}'.format(current_date, conf_template)

        for server in servers['servers']:
            supervisor_data += server_template.format(
                gs_name=server,
                gs_command=servers['servers'][server]['exec'],
                xonotic_root=self.conf['xonotic_root'],
            )

        with open(self.conf['supervisor_conf'], 'w') as f:
            f.write(supervisor_data)

    def generate_server_configs(self):
        """
        This method generates `cfg` **server** configs from `YAML`
        """
        with open(self.conf['xonotic_server_template']) as f:
            xonotic_server_template = f.read()
            xonotic_server_template = '{0}\n\n'.format(xonotic_server_template)

        with open(self.conf['xonotic_smbmod_server_template']) as f:
            smbmod_server_template = f.read()
            smbmod_server_template = '{0}\n\n'.format(smbmod_server_template)

        with open(self.conf['servers_manifest']) as f:
            servers = yaml.load(f)

        current_date = datetime.now()

        for server in servers['servers']:

            server_data = '// Last Generated: {}\n'.format(current_date)

            if servers['servers'][server]['use_smbmod']:
                server_data += smbmod_server_template.format(
                    servername=server,
                    title=servers['servers'][server]['title'],
                    motd=servers['servers'][server]['motd'],
                    port=servers['servers'][server]['port'],
                    maxplayers=servers['servers'][server]['maxplayers'],
                    net_address=servers['servers'][server]['net_address'],
                )
            else:
                server_data += xonotic_server_template.format(
                    servername=server,
                    title=servers['servers'][server]['title'],
                    motd=servers['servers'][server]['motd'],
                    port=servers['servers'][server]['port'],
                    maxplayers=servers['servers'][server]['maxplayers'],
                    net_address=servers['servers'][server]['net_address'],
                )



            custom_server_template = '{}/{}.cfg.tpl'.format(self.conf['xsms_templates_servers_root'], server)

            if os.path.exists(custom_server_template):
                with open(custom_server_template) as f:
                    custom_server_data = f.read()
                    server_data += '// Custom Server Config\n\n' \
                                   '{0}\n'.format(custom_server_data)

            with open('{}/{}.cfg'.format(self.conf['xsms_generated_servers_root'], server), 'w') as f:
                f.write(server_data)

    def start(self, engine='screen'):
        """
        This method starts servers with an **engine**

        Available engines:

          * screen
          * tmux
          * supervisor

        :Example:

        >>> from xsms.servers import ServersCommand
        >>> from xsms.config import conf
        >>> server_cmd = ServersCommand(conf=conf)
        >>> server_cmd.start(engine='tmux')

        """
        with open(self.conf['servers_manifest']) as f:
            servers = yaml.load(f)

        # using screen
        if engine == 'screen':
            screen.start(servers=servers, xonotic_root=self.conf['xonotic_root'])

        # using supervisor
        if engine == 'tmux':
            tmux.start(servers=servers, xonotic_root=self.conf['xonotic_root'])

        # using supervisor
        if engine == 'supervisor':
            supervisor.start(servers=servers, xonotic_root=self.conf['xonotic_root'])
