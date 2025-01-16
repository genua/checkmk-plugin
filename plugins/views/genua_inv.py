#!/usr/bin/env python3

from cmk.gui.i18n import _
from cmk.gui.views.inventory.registry import inventory_displayhints

inventory_displayhints.update(
    {
        ".software.applications.genua.": {
            "title": _("genua"),
            "keyorder": [
                "infoProduct",
                "infoSoftwareversion",
                "infoRelease",
                "infoPatchlevel",
                "infoType",
                "infoHardwareversion",
                "infoSerialnumber",
                "infoLicense",
            ],
        },
        ".software.applications.genua.infoProduct": {
            "title": _("Product type"),
        },
        ".software.applications.genua.infoSoftwareversion": {
            "title": _("Software version"),
        },
        ".software.applications.genua.infoRelease": {
            "title": _("Release"),
        },
        ".software.applications.genua.infoPatchlevel": {
            "title": _("Patchlevel"),
        },
        ".software.applications.genua.infoHardwareversion": {
            "title": _("Hardware version"),
        },
        ".software.applications.genua.infoSerialnumber": {
            "title": _("Serialnumber"),
        },
        ".software.applications.genua.infoLicense": {
            "title": _("License Key"),
        },
        ".software.applications.genua.infoType": {
            "title": _("Type"),
        },
    },
)
