from . import Location, Shape, WP

from math import cos, pi
from typing import NamedTuple, Optional


__all__ = [
    "PrintSettings",
    "steppedHoleDownwards",
]


class PrintSettings(NamedTuple):
    layerHeight: float = 0.2
    nozzleDiameter: float = 0.6
    comfortableOverhang: float = 45
    smallesHorizontalGap: float = 0.1


def steppedHoleDownwards(
        w: WP,
        dOuter: float,
        depthOuter: float,
        dInner: float,
        depthInner: Optional[float] = None,
        pSettings: PrintSettings = PrintSettings(),
        ) -> WP:
    w = (
        w
        .tag("steppedHolePos")

        .vertices(tag="steppedHolePos")
        .cboreHole(dInner, dOuter, depthOuter, depthInner)
    )
    def coneShell(p: Location) -> Shape:
        gap = pSettings.smallesHorizontalGap
        angle = pSettings.comfortableOverhang
        diam = dOuter + 0.5*pSettings.nozzleDiameter
        diam2 = dInner + 1.5*pSettings.nozzleDiameter
        height = cos(angle/180*pi) * (diam-diam2)
        return (
            WP("XY")
            .workplane(offset=-depthOuter)
            .circle(diam/2+gap/2)
            .extrude(-height, taper=angle)
            .faces(">Z")
            .circle(diam/2-gap/2)
            .extrude(-height, taper=angle, combine="cut")
            .findSolid()
            .moved(p)
            )
    w = w.vertices(tag="steppedHolePos").eachpoint(coneShell, combine="cut")
    return w

