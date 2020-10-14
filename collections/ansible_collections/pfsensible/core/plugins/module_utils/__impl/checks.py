# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Orion Poplawski <orion@nwra.com>
# Copyright: (c) 2019, Frederic Bor <frederic.bor@wanadoo.fr>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
import re
import socket


def check_name(self, name, objtype):
    """ check name validy """

    msg = None
    if len(name) >= 32 or len(re.findall(r'(^_*$|^\d*$|[^a-zA-Z0-9_])', name)) > 0:
        msg = "The {0} name must be less than 32 characters long, may not consist of only numbers, may not consist of only underscores, ".format(objtype)
        msg += "and may only contain the following characters: a-z, A-Z, 0-9, _"
    elif name in ["port", "pass"]:
        msg = "The {0} name must not be either of the reserved words 'port' or 'pass'".format(objtype)
    else:
        try:
            socket.getprotobyname(name)
            msg = 'The {0} name must not be an IP protocol name such as TCP, UDP, ICMP etc.'.format(objtype)
        except socket.error:
            pass

        try:
            socket.getservbyname(name)
            msg = 'The {0} name must not be a well-known or registered TCP or UDP port name such as ssh, smtp, pop3, tftp, http, openvpn etc.'.format(objtype)
        except socket.error:
            pass

    if msg is not None:
        self.module.fail_json(msg=msg)


def check_ip_address(self, address, ipprotocol, objtype, allow_networks=False, fail_ifnotip=False):
    """ check address according to ipprotocol """
    if address is None:
        return
    if allow_networks:
        ipv4 = self.is_ipv4_network(address, False)
        ipv6 = self.is_ipv6_network(address, False)
    else:
        ipv4 = self.is_ipv4_address(address)
        ipv6 = self.is_ipv6_address(address)

    if ipprotocol == 'inet':
        if ipv6 or not ipv4 and fail_ifnotip:
            self.module.fail_json(msg='{0} must use an IPv4 address'.format(objtype))
    elif ipprotocol == 'inet6':
        if ipv4 or not ipv6 and fail_ifnotip:
            self.module.fail_json(msg='{0} must use an IPv6 address'.format(objtype))
    elif ipprotocol == 'inet46':
        if ipv4 or ipv6:
            self.module.fail_json(msg='IPv4 and IPv6 addresses can not be used in objects that apply to both IPv4 and IPv6 (except within an alias).')
