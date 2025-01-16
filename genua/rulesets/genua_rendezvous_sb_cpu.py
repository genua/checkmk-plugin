#!/usr/bin/env python3

from cmk.rulesets.v1 import (
    Title,
)

from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    DefaultValue,
    SimpleLevels,
    LevelDirection,
    Percentage,
)

from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    Topic,
    HostAndItemCondition,
)


def _form_genua_rendezvous_sb_cpu() -> Dictionary:
    return Dictionary(
        elements={
            "cpu_util": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("CPU Utilization"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_fixed_levels=DefaultValue((80.0, 90.0))
                ),
            ),
        },
    )

rule_spec_genua_rendezvous_sb_cpu = CheckParameters(
    name="genua_rendezvous_sb_cpu",
    title=Title("genua ServiceBox CPU"),
    condition=HostAndItemCondition(
        item_title=Title("ServiceBox"),
    ),
    topic=Topic.NETWORKING,
    parameter_form=_form_genua_rendezvous_sb_cpu,
)
