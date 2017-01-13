#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mylinux.core.utils import Path
from bitstring import ConstBitStream, Bits
from mylinux.core.net import ICMP
import binascii


@pytest.fixture
def dhcp_msg():
	from mylinux.core.net.PXE import DHCP
	return DHCP.Message()


class Test_DHCP_msg:
	def test_deserialize(self, dhcp_msg):
		with open(Path.join(__file__, '../../resources/net/DHCDISCOVER.bin'), 'rb') as file:
			dhcp_msg.deserialize(file)
			assert dhcp_msg.op.value == 1
			assert dhcp_msg.htype.value == 1
			assert dhcp_msg.hlen.value == 6
			assert dhcp_msg.hops.value == 0
			assert dhcp_msg.xid.value == binascii.unhexlify('82c14d4b')
			assert dhcp_msg.secs.value == 4
			assert dhcp_msg.flag_BROADCAST.value == True
			assert dhcp_msg.flag_NULL.value == 0
			assert dhcp_msg.ciaddr.value == [00, 00, 00, 00]
			assert dhcp_msg.yiaddr.value == [00, 00, 00, 00]
			assert dhcp_msg.siaddr.value == [00, 00, 00, 00]
			assert dhcp_msg.giaddr.value == [00, 00, 00, 00]
			assert dhcp_msg.chaddr.value == ['00', '24', '81', 'c1', '4d', '4b'] + ['00' for i in range(10)]
			assert dhcp_msg.mac == ['00', '24', '81', 'c1', '4d', '4b']
			assert dhcp_msg.sname.value == b'\x00' * 64
			assert dhcp_msg.file.value == b'\x00' * 128
			assert dhcp_msg.magic_cookie.value == [99, 130, 83, 99]

			assert dhcp_msg.options[53].data == ConstBitStream('0x01')
			assert dhcp_msg.options[57].data == ConstBitStream('0x04ec')
			assert 255 not in dhcp_msg.options

	def test_checksum(self):
		echo = ICMP.Echo()
		assert echo.checksum.value == b'\xde\xf8'

	def test_echo(self):
		echo = ICMP.Echo()
		echo.request()
