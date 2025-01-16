#!/usr/bin/env python3

from cmk.agent_based.v2 import (
    SimpleSNMPSection,
    SNMPTree,
    StringTable,
    InventoryPlugin,
    InventoryResult,
    Attributes,
    HostLabelGenerator,
    HostLabel,
)

from cmk.plugins.lib.genua import DETECT_GENUA

import re

Section = dict[str, str]


def _is_hw(hw_version: str, product_type: str) -> bool:
    if product_type == "genugate" and re.match(r"ALG_(\d{3}_\d{3}$|[SML]_\d{3})", hw_version):
        return True
    elif product_type == "genugate":
        return False
    elif "Standard PC" in hw_version:
        return False
    else:
        return True

def parse_genua_info(string_table: StringTable) -> Section:
    parsed = {
        "infoProduct": string_table[0][0],
        "infoSoftwareversion":string_table[0][1],
        "infoRelease": string_table[0][2],
        "infoPatchlevel": string_table[0][3],
        "infoHardwareversion": string_table[0][4],
        "infoSerialnumber": string_table[0][5],
        "infoLicense": string_table[0][6],
    }
    if parsed.get("infoProduct") in ["genugate", "genuscreen", "genubox", "genucenter"]:
        if _is_hw(hw_version=parsed.get("infoHardwareversion"), product_type=parsed.get("infoProduct")):
            parsed["infoType"] = "Hardware"
        else:
            parsed["infoType"] = "Virtual"

    return parsed

def host_label_genua_info(section: Section) -> HostLabelGenerator:
    yield HostLabel("cmk/genua_product", section.get("infoProduct"))
    yield HostLabel("cmk/genua_sw_version", section.get("infoSoftwareversion"))
    yield HostLabel("cmk/genua_hw_version", section.get("infoHardwareversion"))
    yield HostLabel("cmk/genua_type", section.get("infoType"))


snmp_section_genua_info = SimpleSNMPSection(
    name="genua_info",
    detect=DETECT_GENUA,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.3717.2.3", # GENUA-MIB::os::info
        oids=[
            "1", # infoProduct
            "2", # infoSoftwareversion
            "3", # infoRelease
            "4", # infoPatchlevel
            "5", # infoHardwareversion
            "6", # infoSerialnumber
            "7", # infoLicense
        ],
    ),
    parse_function=parse_genua_info,
    host_label_function=host_label_genua_info,
)


def inventory_genua_info(section: Section) -> InventoryResult:
    yield Attributes(
        path=["software", "applications", "genua"],
        inventory_attributes=section,
    )

inventory_plugin_genua_info = InventoryPlugin(
    name="genua_info",
    inventory_function=inventory_genua_info,
)
