#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers."""

import os
from fabric.api import env, run, put
from datetime import datetime

# Set the user and SSH key
env.user = 'ubuntu'
env.key_filename = ['/path/to/your/ssh/private/key']

# Set the web servers
env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers.

    Args:
        archive_path (str): Path to the archive to be deployed.

    Returns:
        bool: True if all operations have been done correctly, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp')

        # Extract archive filename without extension
        filename = os.path.basename(archive_path).split('.')[0]

        # Uncompress the archive to the folder /data/web_static/releases/<filename>
        run('mkdir -p /data/web_static/releases/{}/'.format(filename))
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'
            .format(filename, filename))

        # Delete the archive from the web server
        run('rm /tmp/{}.tgz'.format(filename))

        # Move contents to proper location
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'
            .format(filename, filename))

        # Remove the now-empty folder
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(filename))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the new version
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(filename))

        print("New version deployed!")

        return True
    except Exception as e:
        print(e)
        return False
