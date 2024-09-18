from __future__ import annotations

from .canvasapi import HI


from ntucool.requestor import Requestor


class NTUCoolBase[Async: bool]:
    parent: NTUCoolBase | None
    requestor: Requestor

    _is_async: Async

    def __init__(
        self,
        *,
        parent: NTUCoolBase | None = None,
        requestor: Requestor | None = None,
    ) -> None:
        self.parent = parent
        if self.requestor is None:
            assert parent is not None
            self.requestor = parent.requestor
