# Configures a web server for deployment of web_static using puppet

# Install Nginx
package { 'nginx':
  ensure   => 'present',
  provider => 'apt',
} 

# Ensure directories and files exist
file { '/data':
  ensure  => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

file { '/data/web_static/releases':
  ensure => 'directory',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Holberton School Puppet\n",
}

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

# Set ownership
exec { 'chown -R ubuntu:ubuntu /data/':
  path    => ['/usr/bin', '/usr/local/bin', '/bin'],
  require => [
    File['/data'],
    File['/data/web_static'],
    File['/data/web_static/releases'],
    File['/data/web_static/releases/test'],
    File['/data/web_static/shared'],
    File['/data/web_static/releases/test/index.html'],
    File['/data/web_static/current'],
  ],
}

# Ensure Nginx directories and files exist
file { '/etc/nginx':
  ensure => 'directory',
}

file { '/etc/nginx/html':
  ensure => 'directory',
}

file { '/etc/nginx/html/index.html':
  ensure  => 'present',
  content => "Holberton School Nginx\n",
}

file { '/etc/nginx/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page\n",
}

# Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => template('module/nginx_config.erb'),
} 

# Restart Nginx service
service { 'nginx':
  ensure     => 'running',
  enable     => true,
  subscribe  => File['/etc/nginx/sites-available/default'],
}
