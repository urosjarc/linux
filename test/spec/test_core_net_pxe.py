#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mylinux.core.utils import Path
import binascii
from bitstring import ConstBitStream


@pytest.fixture
def dhcp_msg():
	from mylinux.core.net.pxe import DHCP
	return DHCP.Message()


class Test_DHCP_msg:
	def test_deserialize(self, dhcp_msg):
		with open(Path.join(__file__, '../../resources/DHCDISCOVER.bin'), 'rb') as file:
			dhcp_msg.deserialize(file)
			assert dhcp_msg.op() == 1
			assert dhcp_msg.htype() == 1
			assert dhcp_msg.hlen() == 6
			assert dhcp_msg.hops() == 0
			assert dhcp_msg.xid() == binascii.unhexlify('82c14d4b')
			assert dhcp_msg.secs() == 4
			assert dhcp_msg.flag_BROADCAST() == True
			assert dhcp_msg.flag_NULL() == 0
			assert dhcp_msg.ciaddr() == [00, 00, 00, 00]
			assert dhcp_msg.yiaddr() == [00, 00, 00, 00]
			assert dhcp_msg.siaddr() == [00, 00, 00, 00]
			assert dhcp_msg.giaddr() == [00, 00, 00, 00]
			assert dhcp_msg.chaddr() == ['00', '24', '81', 'c1', '4d', '4b'] + ['00' for i in range(10)]
			assert dhcp_msg.MAC() == ['00', '24', '81', 'c1', '4d', '4b']
			assert dhcp_msg.sname() == b'\x00' * 64
			assert dhcp_msg.file() == b'\x00' * 128
			assert dhcp_msg.magic_cookie() == [99, 130, 83, 99]

			assert dhcp_msg.options[53].data == ConstBitStream('0x01')
			assert dhcp_msg.options[57].data == ConstBitStream('0x04ec')
			assert 255 not in dhcp_msg.options
