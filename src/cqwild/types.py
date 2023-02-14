import cadquery as cq
import typing


from typing import Callable, Concatenate, ParamSpec, TypeVar


X = TypeVar("X")


P = ParamSpec('P')


class Sketch(cq.Sketch):
    @classmethod
    def _fromCQ(cls, w: cq.Sketch) -> 'Sketch':
        w.__class__ = cls
        return typing.cast(cls, w)
    def apply(self: 'Sketch', fn: Callable[Concatenate['Sketch', P], X], *args: P.args, **kwargs: P.kwargs) -> X:
        return fn(self, *args, **kwargs)


class Workplane(cq.Workplane):
    @classmethod
    def _fromCQ(cls, w: cq.Workplane) -> 'Workplane':
        w.__class__ = cls
        return typing.cast(cls, w)
    def apply(self: 'Workplane', fn: Callable[Concatenate['Workplane', P], X], *args: P.args, **kwargs: P.kwargs) -> X:
        return fn(self, *args, **kwargs)
    def workplaneFromTagged(self: 'Workplane', workplaneName: str) -> 'Workplane':
        return self._fromCQ(super().workplaneFromTagged(workplaneName))
    def end(self: 'Workplane') -> 'Workplane':
        return self._fromCQ(super().end())
    def sketch(self: 'Workplane') -> Sketch:
        x = super().sketch()
        x.__class__ = Sketch
        return typing.cast(Sketch, x)
