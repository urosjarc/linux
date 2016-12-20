# -*- coding: utf-8 -*-

def html(module_name, docfilter=None, allsubmodules=False,
		 external_links=False, link_prefix='', source=True):
	"""
    Returns the documentation for the module `module_name` in HTML
    format. The module must be importable.
    `docfilter` is an optional predicate that controls which
    documentation objects are shown in the output. It is a single
    argument function that takes a documentation object and returns
    `True` or `False`. If `False`, that object will not be included in
    the output.
    If `allsubmodules` is `True`, then every submodule of this module
    that can be found will be included in the documentation, regardless
    of whether `__all__` contains it.
    If `external_links` is `True`, then identifiers to external modules
    are always turned into links.
    If `link_prefix` is `True`, then all links will have that prefix.
    Otherwise, links are always relative.
    If `source` is `True`, then source code will be retrieved for
    every Python object whenever possible. This can dramatically
    decrease performance when documenting large modules.
    """
	mod = Module(import_module(module_name),
				 docfilter=docfilter,
				 allsubmodules=allsubmodules)
	return mod.html(external_links=external_links,
					link_prefix=link_prefix, source=source)
