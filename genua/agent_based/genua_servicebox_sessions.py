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
    all_of,
    exists,
)

from cmk.plugins.lib.genua import DETECT_GENUA_GENUBOX


Section = list[str]

def parse_genua_servicebox_sessions(string_table: StringTable) -> Section:
    parsed = []
    for element in string_table:
        parsed.append(element[0])
    return parsed

snmp_section_genua_servicebox_sessions = SimpleSNMPSection(
    name="genua_servicebox_sessions",
    detect=all_of(
        DETECT_GENUA_GENUBOX,
        exists(".1.3.6.1.4.1.3717.65.4.1.2.*"),
    ),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.3717.65.4.1",
        oids=[
            "2",
        ],
    ),
    parse_function=parse_genua_servicebox_sessions,
)


def discover_genua_servicebox_sessions(section: Section) -> DiscoveryResult:
    yield Service()

def check_genua_servicebox_sessions(section: Section) -> CheckResult:
    yield from check_levels(
        value=len(section),
        label="Number of sessions",
        metric_name="genua_servicebox_sessions",
        render_func=int,
    )

    yield Result(
        state=State.OK,
        summary="See long output for details",
        details=f"Sessions: {', '.join(section)}"
    )

check_plugin_genua_servicebox_sessions = CheckPlugin(
    name="genua_servicebox_sessions",
    service_name="ServiceBox Sessions",
    discovery_function=discover_genua_servicebox_sessions,
    check_function=check_genua_servicebox_sessions,
)
