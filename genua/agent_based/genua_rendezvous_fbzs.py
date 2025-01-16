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
    Metric
)

from cmk.plugins.lib.genua import DETECT_GENUA_GENUBOX


STATE_MAP = {
    "0": "stopped",
    "1": "started",
}

Section = dict[str, dict[str, str]]

def parse_genua_rendezvous_fbzs(string_table: StringTable) -> Section:
    parsed = {}
    for entry in string_table:
        parsed_entry = {
            "fbzsIndex": entry[0],
            "fbzsId": entry[1],
            "fbzsDescription": entry[3],
            "fbzsState": entry[4],
            "fbzsTimeleft": entry[5],
        }
        parsed[entry[2]] = parsed_entry
    return parsed

snmp_section_genua_rendezvous_fbzs = SimpleSNMPSection(
    name="genua_rendezvous_fbzs",
    detect=all_of(
        DETECT_GENUA_GENUBOX,
        exists(".1.3.6.1.4.1.3717.64.3.*"),
    ),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.3717.64.3.1", # GENUA-RENDEZVOUS-MIB::fbzsTable:fbzsEntry
        oids=[
            "1", # fbzsIndex
            "2", # fbzsId
            "3", # fbzsName
            "4", # fbzsDescription
            "5", # fbzsState
            "6", # fbzsTimeleft
        ],
    ),
    parse_function=parse_genua_rendezvous_fbzs,
)

def discover_genua_rendezvous_fbzs(section: Section) -> DiscoveryResult:
    yield Service()

def check_genua_rendezvous_fbzs(section: Section) -> CheckResult:
    open_connections = []
    all_connections = []
    for name, connection in section.items():
        all_connections.append(name)
        if connection.get("fbzsState") == "1":
            open_connections.append(name)

    yield Result(
        state=State.OK,
        summary=f"{len(open_connections)} open connections: {', '.join(open_connections)}",
        details=f"All connections: {', '.join(all_connections)}",
    )
    yield Metric(
        name="genua_rendezvous_fbzs_all_connections",
        value=len(all_connections),
    )
    yield Metric(
        name="genua_rendezvous_fbzs_open_connections",
        value=len(open_connections),
    )

check_plugin_genua_rendezvous_fbzs = CheckPlugin(
    name="genua_rendezvous_fbzs",
    discovery_function=discover_genua_rendezvous_fbzs,
    check_function=check_genua_rendezvous_fbzs,
    service_name="Open Fzbs",
)
