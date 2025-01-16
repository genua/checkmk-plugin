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

from cmk.plugins.lib.genua import DETECT_GENUA_GENUBOX

import time

Section = dict[str, dict[str, str]]


def parse_genua_rendezvous_sb(string_table: StringTable) -> Section:
    parsed = {}
    for line in string_table:
        sboxAppId, sboxName, sboxLastUpdate, sboxSerialNumber, sboxCpuUsage, sboxMemUsage = line
        sub_parsed = {
            "sboxAppId": sboxAppId,
            "sboxLastUpdate": int(sboxLastUpdate),
            "sboxSerialNumber": sboxSerialNumber,
            "sboxCpuUsage": float(sboxCpuUsage),
            "sboxMemUsage": float(sboxMemUsage),
        }
        parsed[sboxName] = sub_parsed
    return parsed

snmp_section_genua_rendezvous_sb = SimpleSNMPSection(
    name="genua_rendezvous_sb",
    detect=all_of(
        DETECT_GENUA_GENUBOX,
        exists(".1.3.6.1.4.1.3717.65.1.1.*"),
    ),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.3717.65.1.1", # GENUA-SERVICEBOX-MIB::sboxTable
        oids=[
            "2",  # sboxAppId
            "3",  # sboxName
            "4",  # sboxLastUpdate
            "10", # sboxSerialNumber
            "11", # sboxCpuusage
            "12", # sboxMemusage
        ],
    ),
    parse_function=parse_genua_rendezvous_sb,
)


def discover_genua_rendezvous_sb(section: Section) -> DiscoveryResult:
    for sb in section.keys():
        yield Service(
            item=sb,
        )


########
# INFO #
########

def check_genua_rendezvous_sb_info(item: str, params: dict, section: Section) -> CheckResult:
    sb = section.get(item)
    now = int(time.time())
    time_since_last_update = now - sb.get("sboxLastUpdate")
    
    yield Result(
        state=State.OK,
        summary=f"{item} ({sb.get('sboxAppId')})"
    )
    yield Result(
        state=State.OK,
        summary=f"Serialnumber: {sb.get('sboxSerialNumber')}",
    )
    yield from check_levels(
        value=time_since_last_update,
        label="Time since last update",
        levels_upper=params.get("last_update"),
        render_func=render.timespan,
    )

check_plugin_genua_rendezvous_sb_info = CheckPlugin(
    name="genua_rendezvous_sb_info",
    service_name="ServiceBox %s",
    sections=["genua_rendezvous_sb"],
    discovery_function=discover_genua_rendezvous_sb,
    check_function=check_genua_rendezvous_sb_info,
    check_ruleset_name="genua_rendezvous_sb_info",
    check_default_parameters={
        "last_update": ("fixed", (60 * 5, 60 * 15)),
    }
)


#######
# CPU #
#######

def check_genua_rendezvous_sb_cpu(item: str, params: dict, section: Section) -> CheckResult:
    sb = section.get(item)
    yield from check_levels(
        value=sb.get("sboxCpuUsage"),
        label="Total CPU Utilization",
        levels_upper=params.get("cpu_util"),
        render_func=render.percent,
        metric_name="genua_rendezvous_sb_cpu",
        boundaries=(0.0, 100.0),
    )

check_plugin_genua_rendezvous_sb_cpu = CheckPlugin(
    name="genua_rendezvous_sb_cpu",
    service_name="ServiceBox %s CPU",
    sections=["genua_rendezvous_sb"],
    discovery_function=discover_genua_rendezvous_sb,
    check_function=check_genua_rendezvous_sb_cpu,
    check_ruleset_name="genua_rendezvous_sb_cpu",
    check_default_parameters={
        "cpu_util": ("fixed", (80, 90)),
    },
)


##########
# Memory #
##########

def check_genua_rendezvous_sb_mem(item: str, params: dict, section: Section) -> CheckResult:
    sb = section.get(item)
    yield from check_levels(
        value=sb.get("sboxMemUsage"),
        label="Total Memory",
        levels_upper=params.get("mem_usage"),
        render_func=render.percent,
        metric_name="genua_rendezvous_sb_mem",
        boundaries=(0.0, 100.0),
    )

check_plugin_genua_rendezvous_sb_mem = CheckPlugin(
    name="genua_rendezvous_sb_mem",
    service_name="ServiceBox %s Memory",
    sections=["genua_rendezvous_sb"],
    discovery_function=discover_genua_rendezvous_sb,
    check_function=check_genua_rendezvous_sb_mem,
    check_ruleset_name="genua_rendezvous_sb_mem",
    check_default_parameters={
        "mem_usage": ("fixed", (80, 90)),
    }
)
