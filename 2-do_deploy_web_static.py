#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers."""

import os.path
from fabric.api import env, put, run

env.hosts = ["100.25.104.113", "100.25.31.234"]


def do_deploy(archive_path):
    """
    Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.

    Returns:
        bool: True if the deployment succeeds, False otherwise.
    """
    if not os.path.isfile(archive_path):
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is False:
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed is False:
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed is False:
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)).failed is False:
    if run("rm /tmp/{}".format(file)).failed is False:
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is False:
    if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed is False:
    if run("rm -rf /data/web_static/current").failed is False:
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed is False:
        return True
    return False
