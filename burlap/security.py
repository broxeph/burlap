"""
General tweaks and services to enhance system security.
"""
from __future__ import print_function

from burlap import Satchel
from burlap.constants import *
from burlap.decorators import task

class UnattendedUpgradesSatchel(Satchel):
    """
    Enables various degrees of automatic package download and installation.
    """
    
    name = 'unattendedupgrades'
    
    @property
    def packager_system_packages(self):
        return {
            UBUNTU: ['unattended-upgrades'],
            (UBUNTU, '12.04'): ['unattended-upgrades'],
            (UBUNTU, '14.04'): ['unattended-upgrades'],
        }
    
    def set_defaults(self):
        
        self.env.mail_to = 'root@localhost'
        self.env.reboot = 'true'
        self.env.reboot_time = '02:00'
        self.env.mailonlyonerror = "true"
        
        self.env.update_package_lists = 1
        self.env.download_upgradeable_packages = 1
        self.env.autoclean_interval = 7
        self.env.unattended_upgrade = 1

    @task
    def configure(self):
        
        #TODO:generalize for other distros?
        assert not self.genv.host_os_distro or self.genv.host_os_distro == UBUNTU, \
            'Only Ubuntu is supported.'
        
        r = self.local_renderer
        
        if self.env.enabled:
            
            # Enable automatic package updates for Ubuntu.
            # Taken from the guide at https://help.ubuntu.com/lts/serverguide/automatic-updates.html.
            r.sudo('apt-get install --yes unattended-upgrades')
            fn = self.render_to_file('unattended_upgrades/etc_apt_aptconfd_50unattended_upgrades')
            r.put(local_path=fn, remote_path='/etc/apt/apt.conf.d/50unattended-upgrades', use_sudo=True)
            fn = self.render_to_file('unattended_upgrades/etc_apt_aptconfd_10periodic')
            r.put(local_path=fn, remote_path='/etc/apt/apt.conf.d/10periodic', use_sudo=True)
            
        else:
            #TODO:disable
            pass
    
    
    configure.deploy_before = ['packager', 'user']
        
UnattendedUpgradesSatchel()
