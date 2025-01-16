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
    TimeSpan,
    TimeMagnitude,
)

from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    Topic,
    HostAndItemCondition,
)


def _form_genua_rendezvous_sb_info() -> Dictionary:
    return Dictionary(
        elements={
            "last_update": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Time since last update"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[
                            TimeMagnitude.SECOND,
                            TimeMagnitude.MINUTE,
                            TimeMagnitude.HOUR,
                            TimeMagnitude.DAY,
                        ],
                    ),
                    prefill_fixed_levels=DefaultValue((5 * 60, 15 * 60)),
                ),
            ),
        },
    )

rule_spec_genua_rendezvous_sb_info = CheckParameters(
    name="genua_rendezvous_sb_info",
    title=Title("genua ServiceBox"),
    condition=HostAndItemCondition(
        item_title=Title("ServiceBox"),
    ),
    topic=Topic.NETWORKING,
    parameter_form=_form_genua_rendezvous_sb_info,
)
