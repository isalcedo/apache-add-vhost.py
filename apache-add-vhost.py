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


def start_bs(domain, path, remove=False):
    if remove is True:
        os.remove("/etc/httpd/conf/vhosts/" + domain)

        httpdfile = open("/etc/httpd/conf/httpd.conf", "r")
        lines = httpdfile.readlines()
        httpdfile.close()

        httpdfile = open("/etc/httpd/conf/httpd.conf", "w")
        for i in lines:
            if i != "Include conf/vhosts/" + domain + "\n":
                httpdfile.write(i)
        httpdfile.close()

        hostsfile = open("/etc/hosts", "r")
        lines = hostsfile.readlines()
        hostsfile.close()

        hostsfile = open("/etc/hosts", "w")
        for i in lines:
            if i != "127.0.0.1       " + domain + "\n":
                hostsfile.write(i)
        hostsfile.close()

        os.system(
            'systemctl restart httpd'
        )

    else:
        data = {"path": path,
                "domain": domain}

        with open("/etc/httpd/conf/vhosts/" + domain, "w+") as vhostfile:
            vhostfile.write(template.format(**data))

        with open("/etc/httpd/conf/httpd.conf", "a") as httpdfile:
            httpdfile.write("{}\n".format("Include conf/vhosts/" + domain))

        with open("/etc/hosts", "a") as hostsfile:
            hostsfile.write("{}\n".format("127.0.0.1       " + domain))

        os.system(
            'systemctl restart httpd'
        )


# Dealing with arguments.
parser = argparse.ArgumentParser(
    description=("""Create a virtualhost in Apache for local
                    serving (Archlinux and variants)""")
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

parser.add_argument(
    '-remove',
    action='store_true',
    help='(optional) For removing the domain from local machine'
)

arguments = parser.parse_args()

# Main Script
start_bs(arguments.domain, arguments.path, arguments.remove)
