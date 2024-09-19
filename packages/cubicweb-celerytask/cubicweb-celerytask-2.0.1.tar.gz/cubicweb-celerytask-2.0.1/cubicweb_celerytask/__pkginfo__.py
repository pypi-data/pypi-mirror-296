# pylint: disable=W0622
"""cubicweb-celerytask application packaging information"""


modname = "cubicweb_celerytask"
distname = "cubicweb-celerytask"

numversion = (2, 0, 1)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "Run and monitor celery tasks"
web = f"https://forge.extranet.logilab.fr/cubicweb/cubes/{distname}"

__depends__ = {
    "celery": "~= 5.0",
    "cubicweb": ">= 3.38.16, < 5.0.0",
    "cw-celerytask-helpers": ">= 0.11.0",
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: JavaScript",
]
