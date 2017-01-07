#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mylinux.core.utils import Path
import binascii


@pytest.fixture
def dhcp_msg():
	from mylinux.core.net.pxe import DHCP
	return DHCP.Message()


class Test_DHCP_msg:
	def test_deserialize(self, dhcp_msg):
		with open(Path.join(__file__, '../../resources/DHCDISCOVER.bin'), 'rb') as file:
			dhcp_msg.deserialize(file)
			assert dhcp_msg.op.data == 1
			assert dhcp_msg.htype.data == 1
			assert dhcp_msg.hlen.data == 6
			assert dhcp_msg.hops.data == 0
			assert dhcp_msg.xid.data == binascii.unhexlify('82c14d4b')
			assert dhcp_msg.secs.data == 4
			# assert dhcp_msg.flags.BROADCAST.data == True
			# assert dhcp_msg.flags.other.data == '000000000000000'
			# assert dhcp_msg.ciaddr.data == [00, 00, 00, 00]
			# assert dhcp_msg.yiaddr.data == [00, 00, 00, 00]
			# assert dhcp_msg.siaddr.data == [00, 00, 00, 00]
			# assert dhcp_msg.giaddr.data == [00, 00, 00, 00]
			# assert dhcp_msg.getMAC().data == ['00', '24', '81', 'c1', '4d', '4b']
			# assert dhcp_msg.sname.data == b'00' * 64
			# assert dhcp_msg.file.data == b'\x00' * 128
			# assert dhcp_msg.magic_cookie.data == [99, 130, 83, 99]
