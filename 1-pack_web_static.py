#!/usr/bin/python3
#A Fabfile that generates a .tgz archive from the contents of web_static

from fabric.api import local
from datetime import datetime

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        # Get the current date and time
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")

        # Create the versions folder if it doesn't exist
        local("mkdir -p versions")

        # Generate the archive filename
        archive_name = "versions/web_static_{}.tgz".format(timestamp)

        # Create the .tgz archive
        local("tar -cvzf {} web_static".format(archive_name))

        print("web_static packed: {} -> {}Bytes".format(
            archive_name,
            local("du -b {}".format(archive_name), capture=True)
        ))
        return archive_name
    except Exception as e:
        print(e)
        return None

