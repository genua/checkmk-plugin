#!/usr/bin/env python3

from cmk.agent_based.v2 import (
    SimpleSNMPSection,
    SNMPTree,
    StringTable,
    State,
    CheckPlugin,
    DiscoveryResult,
    CheckResult,
    Service,
    Result,
    all_of,
    exists,
)

from cmk.plugins.lib.genua import DETECT_GENUA_GENUGATE


MAP_NTP_STATES = {
    "0": (State.UNKNOWN, "unknown"),
    "1": (State.CRIT, "not reachable"),
    "2": (State.CRIT, "not synchronized"),
    "3": (State.OK, "synchronized"),
}

def parse_genua_genugate_ntp(string_table: StringTable) -> str:
    return string_table[0][0]

snmp_section_genua_genugate_ntp = SimpleSNMPSection(
    name="genua_genugate_ntp",
    detect=all_of(
       DETECT_GENUA_GENUGATE,
       exists(".1.3.6.1.4.1.3717.8.7")
    ),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.3717.8", # GENUA-GENUGATE-MIB
        oids=[
            "7", # ntpStatus
        ],
    ),
    parse_function=parse_genua_genugate_ntp,
)


def discover_genua_genugate_ntp(section: str) -> DiscoveryResult:
    yield Service()

def check_genua_genugate_ntp(section: str) -> CheckResult:
    yield Result(
        state=MAP_NTP_STATES.get(section, (State.UNKNOWN, section))[0],
        summary=f"State: {MAP_NTP_STATES.get(section, (State.UNKNOWN, section))[1]}",
    )

check_plugin_genua_genugate_ntp = CheckPlugin(
    name="genua_genugate_ntp",
    service_name="NTP Synchronization",
    discovery_function=discover_genua_genugate_ntp,
    check_function=check_genua_genugate_ntp,
)
