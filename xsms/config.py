import xsms.util as util
import os

config_file = '.xsms.cfg'
home = os.path.expanduser('~')
config_file_with_path = os.path.join(home, config_file)

util.check_if_not_create(config_file_with_path, 'config/xsms.cfg')

config = util.parse_config(config_file_with_path)

conf = {
    'xsms_config_root': os.path.expanduser('~/.xsms'),
    'xsms_generated_root': os.path.expanduser('~/.xsms/generated'),
    'xsms_templates_root': os.path.expanduser('~/.xsms/templates'),
    'xsms_generated_servers_root': os.path.expanduser('~/.xsms/generated/servers'),
    'xsms_templates_servers_root': os.path.expanduser('~/.xsms/templates/servers'),
    'xonotic_root': os.path.expanduser(config['xonotic_root']),
    'smb_init_script': os.path.expanduser(config['smb_init_script']),
    'smb_update_script': os.path.expanduser(config['smb_update_script']),
    'smb_build_script': os.path.expanduser(config['smb_build_script']),
    'smb_cache_path': os.path.expanduser(config['smb_cache_path']),
    'data_csprogs': os.path.expanduser(config['data_csprogs']),
    'servers_manifest': os.path.expanduser(config['servers']),
    'xonotic_server_template': os.path.expanduser(config['xonotic_server_template']),
    'supervisor_server_template': os.path.expanduser(config['supervisor_server_template']),
    'supervisor_conf': os.path.expanduser(config['supervisor_conf']),
}

# Setup templates in ~/.xsms
util.check_if_not_create(conf['servers_manifest'], 'config/servers.yml')
util.check_if_not_create(conf['xonotic_server_template'], 'config/templates/xonotic.server.cfg.tpl')
util.check_if_not_create(conf['supervisor_server_template'], 'config/templates/supervisor.server.conf.tpl')

# Make sure needed dirs exist
os.makedirs(conf['xsms_generated_servers_root'], exist_ok=True)
os.makedirs(conf['xsms_templates_servers_root'], exist_ok=True)

# Setup symlinks
if not os.path.exists(os.path.expanduser('~/.xonotic/servers.pk3dir')):
    os.symlink(conf['xsms_generated_servers_root'], os.path.expanduser('~/.xonotic/servers.pk3dir'))
