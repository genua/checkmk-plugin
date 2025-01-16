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
    check_levels,
    render,
    all_of,
    exists,
)

from cmk.plugins.lib.genua import DETECT_GENUA


Section = dict[str, str]

MAP_SWAP_STATES = {
    0: (State.CRIT, "not ok"),
    1: (State.OK, "ok"),
    2: (State.UNKNOWN, "unknown"),
}

def parse_genua_swap(string_table: StringTable) -> Section:
    parsed = {
        "swapMax": int(string_table[0][0]),
        "swapUsed": int(string_table[0][1]),
        "swapStatus": int(string_table[0][2]),
    }
    return parsed

snmp_section_genua_swap = SimpleSNMPSection(
    name="genua_swap",
    detect=all_of(
        DETECT_GENUA,
        exists(".1.3.6.1.4.1.3717.2.1.1.4.*")
    ),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.3717.2.1.1.4", # GENUA-MIB::os::sensor::system::swap
        oids=[
            "1", # swapMax
            "2", # swapUsed
            "3", # swapStatus
        ],
    ),
    parse_function=parse_genua_swap,
)


def discover_genua_swap(section: Section) -> DiscoveryResult:
    if section.get("swapMax") != 0:
        yield Service()

def check_genua_swap(section: Section) -> CheckResult:
    yield Result(
        state=MAP_SWAP_STATES.get(section.get("swapStatus"))[0],
        summary=f"State: {MAP_SWAP_STATES.get(section.get('swapStatus'))[1]}",
    )
    yield from check_levels(
        value=section.get("swapMax") * 1024 ** 2,
        label="Available Swap",
        render_func=render.bytes,
        metric_name="genua_swap_max",
        boundaries=(0, section.get("swapMax") * 1024 ** 2),
    )
    yield from check_levels(
        value=section.get("swapUsed") * 1024 ** 2,
        label="Used Swap",
        render_func=render.bytes,
        metric_name="genua_swap_used",
        boundaries=(0, section.get("swapMax") * 1024 ** 2),
    )

check_plugin_genua_swap = CheckPlugin(
    name="genua_swap",
    service_name="Swap",
    discovery_function=discover_genua_swap,
    check_function=check_genua_swap,

)
