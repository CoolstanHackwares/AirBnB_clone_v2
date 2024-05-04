#!/usr/bin/python3
#A Fabfile that generates a .tgz archive from the contents of web_static.
import os.path
from datetime import datetime
from fabric.api import local


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    try:
        dt = datetime.utcnow()
        timestamp = dt.strftime("%Y%m%d%H%M%S")
        archive_name = "versions/web_static_{}.tgz".format(timestamp)

        # Create the versions folder if it doesn't exist
        local("mkdir -p versions")

        # Create the .tgz archive
        local("tar -cvzf {} web_static".format(archive_name))

        # Check if the archive file exists
        if os.path.isfile(archive_name):
            print("web_static packed: {} -> {}Bytes".format(
                archive_name,
                os.path.getsize(archive_name)
            ))
            return archive_name
        else:
            return None
    except Exception as e:
        print(e)
        return None
