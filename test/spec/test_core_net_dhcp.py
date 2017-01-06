#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mylinux.core.utils import pathJoin
import binascii


@pytest.fixture
def dhcp_msg():
	from mylinux.core.net.dhcp import DHCP_msg
	return DHCP_msg()


class Test_DHCP_msg:
	def test_deserialize(self, dhcp_msg):
		with open(pathJoin(__file__, '../../resources/DHCDISCOVER.bin'), 'rb') as file:
			dhcp_msg.deserialize(file)
			assert dhcp_msg.op == 1
			assert dhcp_msg.htype == 1
			assert dhcp_msg.hlen == 6
			assert dhcp_msg.hops == 0
			assert dhcp_msg.xid == binascii.unhexlify('82c14d4b')
			# assert dhcp_msg.secs == 4
			# assert dhcp_msg.flags.BROADCAST == True
			# assert dhcp_msg.flags.other == '000000000000000'
			# assert dhcp_msg.ciaddr == (0, 0, 0, 0)
			# assert dhcp_msg.yiaddr == (0, 0, 0, 0)
			# assert dhcp_msg.siaddr == (0, 0, 0, 0)
			# assert dhcp_msg.giaddr == (0, 0, 0, 0)
			# assert dhcp_msg.chaddr == (b'00', b'24', b'81', b'c1', b'4d', b'4b')
			# assert dhcp_msg.sname == b'00' * 64
			# assert dhcp_msg.file == b'\x00' * 128
			# assert dhcp_msg.magic_cookie == (63, 82, 53, 63)
