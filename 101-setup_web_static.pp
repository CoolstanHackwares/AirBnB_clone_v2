# Web server setup using puppet

# Install nginx
package { 'nginx':
  ensure => installed,
}

# Create directories
file { '/data/web_static/releases/test':
  ensure => directory,
}

file { '/data/web_static/shared':
  ensure => directory,
}

# Create index.html
file { '/data/web_static/releases/test/index.html':
  content => '<html><head></head><body>Holberton School</body></html>',
}

# Symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  force  => true,
}

# Set ownership
exec { 'set_ownership':
  command => 'chown -R ubuntu:ubuntu /data/',
  path    => '/usr/bin',
  onlyif  => 'test "$(stat -c %U:%G /data/)" != "ubuntu:ubuntu"',
}

# Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => '
server {
    listen 80;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /etc/nginx/html;
    index  index.html index.htm;

    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }

    error_page 404 /404.html;
    location /404 {
        root /etc/nginx/html;
        internal;
    }
}',
}

# Restart nginx
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
