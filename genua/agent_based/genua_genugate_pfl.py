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


MAP_PF_STATES = {
    "0": (State.CRIT, "not OK"),
    "1": (State.OK, "OK"),
}


Section = list[str]

def parse_genua_genugate_pfl(string_table: StringTable) -> Section:
    return string_table[0]

snmp_section_genua_genugate_pfl = SimpleSNMPSection(
    name="genua_genugate_pfl",
    detect=all_of(
       DETECT_GENUA_GENUGATE,
       exists(".1.3.6.1.4.1.3717.8.8.*")
    ),
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.3717.8.8", # GENUA-GENUGATE-MIB::pfl
        oids=[
            "1", # pflRunningVersion
            "2", # pflRunningConfig
            "3", # pflLocalVersion
            "4", # pflLocalConfig
            "5", # pflConfigUpToDate
            "6", # pflLogfileUpToDate
        ],
    ),
    parse_function=parse_genua_genugate_pfl,
)

def discover_genua_genugate_pfl(section: Section) -> DiscoveryResult:
    yield Service()

def check_genua_genugate_pfl(section: Section) -> CheckResult:
    pflRunningVersion, pflRunningConfig, pflLocalVersion, pflLocalConfig, pflConfigUpToDate, pflLogfileUpToDate = section
    
    yield Result(
        state=MAP_PF_STATES.get(pflConfigUpToDate)[0],
        summary=f"State of Config: {MAP_PF_STATES.get(pflConfigUpToDate)[1]}",
    )

    yield Result(
        state=MAP_PF_STATES.get(pflLogfileUpToDate)[0],
        summary=f"State of Logfile: {MAP_PF_STATES.get(pflLogfileUpToDate)[1]}",
    )

    if pflRunningConfig == pflLocalConfig:
        summary = f"Running and local config are the same"
        details = f"Running and local config are the same: {pflRunningConfig}"
    else:
        summary = f"Running and local config differ"
        details = f"Running config: {pflRunningConfig}\nLocal config: {pflLocalConfig}"
    yield Result(
        state=State.OK,
        summary=summary,
        details=details,
    )

    if pflRunningVersion == pflLocalVersion:
        summary = f"Running and local version are the same"
        details = f"Running and local version are the same: {pflRunningVersion}"
    else:
        summary = f"Running and local version differ"
        details = f"Running version: {pflRunningVersion}\nLocal version: {pflLocalVersion}"
    yield Result(
        state=State.OK,
        summary=summary,
        details=details,
    )


check_plugin_genua_genugate_pfl = CheckPlugin(
    name="genua_genugate_pfl",
    service_name="PFL",
    discovery_function=discover_genua_genugate_pfl,
    check_function=check_genua_genugate_pfl,
)
