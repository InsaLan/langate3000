def to_decimal_mac(mac):
	"""
	Convert a MAC address to decimal.
	
	:param mac: MAC address to convert, in the format "3e:a1:f8:d7:5b:c2".
	:return: Decimal MAC address, in the format "62.161.248.215.91.194".
	"""
	
	octets = mac.split(':')
	decimal_mac = '.'.join(str(int(octet, 16)) for octet in octets)
	return decimal_mac