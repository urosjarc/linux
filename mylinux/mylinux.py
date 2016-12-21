# -*- coding: utf-8 -*-

"""
alsjfkd
"""


def html(module_name, docfilter=None, allsubmodules=False,
		 external_links=False, link_prefix='', source=True):
	mod = Module(import_module(module_name),
				 docfilter=docfilter,
				 allsubmodules=allsubmodules)
	return mod.html(external_links=external_links,
					link_prefix=link_prefix, source=source)
