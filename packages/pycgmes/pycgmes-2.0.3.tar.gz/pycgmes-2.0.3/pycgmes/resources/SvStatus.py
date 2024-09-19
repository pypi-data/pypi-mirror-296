# SPDX-FileCopyrightText: 2023 Alliander
#
# SPDX-License-Identifier: Apache-2.0

"""
Generated from the CGMES 3 files via cimgen: https://github.com/sogno-platform/cimgen
"""

from functools import cached_property
from typing import Optional

from pydantic import Field
from pydantic.dataclasses import dataclass

from ..utils.base import Base
from ..utils.profile import BaseProfile, Profile


@dataclass
class SvStatus(Base):
    """
    State variable for status.

    ConductingEquipment: The conducting equipment associated with the status state variable.
    inService: The in service status as a result of topology processing.  It indicates if the equipment is considered as
      energized by the power flow. It reflects if the equipment is connected within a solvable island.
      It does not necessarily reflect whether or not the island was solved by the power flow.
    """

    ConductingEquipment: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "in_profiles": [
                Profile.SV,
            ]
        },
    )

    inService: bool = Field(
        default=False,
        json_schema_extra={
            "in_profiles": [
                Profile.SV,
            ]
        },
    )

    @cached_property
    def possible_profiles(self) -> set[BaseProfile]:
        """
        A resource can be used by multiple profiles. This is the set of profiles
        where this element can be found.
        """
        return {
            Profile.SV,
        }
