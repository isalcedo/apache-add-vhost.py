#!/usr/bin/python

"""Tool to add a new project into apache

This is a simple tool for lazy developers.
This is for Arch Linux environments.

Example:
    $ python apache-add-vhost.py project.dev /home/joe-doe/project-folder

Attributes:
    domain (string): Local domain name of your application
    path   (string): Absolute path to project folder

Dev:     Ignacio Salcedo
WebSite: https://isalcedo.com
Email:   ignacio@isalcedo.com

"""

# Imports.
import os
import argparse


template = """
<VirtualHost *:80>
    DocumentRoot "{path}"
    ServerAdmin ignacio@isalcedo.com
    ServerName {domain}
    ServerAlias *.{domain}
    <Directory "{path}/">
        AllowOverride All
        Require all granted
        Options Indexes SymLinksIfOwnerMatch FollowSymLinks
    </Directory>
    ErrorLog "/var/log/httpd/{domain}-error_log"
    CustomLog "/var/log/httpd/{domain}-access_log" common
</VirtualHost>
"""


def start_bs(domain, path):
    data = {"path": path,
            "domain": domain}

    with open("/etc/httpd/conf/vhosts/" + domain, "w+") as vhostfile:
        vhostfile.write(template.format(**data))

    with open("/etc/httpd/conf/httpd.conf", "a") as httpdfile:
        httpdfile.write("Include conf/vhosts/" + domain)

    with open("/etc/hosts", "a") as hostsfile:
        hostsfile.write("127.0.0.1       " + domain)

    os.system(
        'systemctl restart httpd'
    )


# Dealing with arguments.
parser = argparse.ArgumentParser(
    description=("""Start BrowserSync for Joomla 3 site development,
                    or Advanced Yii2 Development""")
)

parser.add_argument(
    'domain',
    action='store',
    help='Define the local domain'
)

parser.add_argument(
    'path',
    action='store',
    help='Define the absolute path to the project folder'
)

arguments = parser.parse_args()

# Main Script
start_bs(arguments.domain, arguments.path)
