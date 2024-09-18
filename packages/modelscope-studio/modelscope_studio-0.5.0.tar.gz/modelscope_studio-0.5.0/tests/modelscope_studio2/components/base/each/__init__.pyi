from __future__ import annotations

from typing import Any

from gradio.component_meta import ComponentMeta
from gradio.components.base import BlockContext
from gradio.events import Dependency

from ....utils.dev.resolve_frontend_dir import resolve_frontend_dir

class AntdEach(AntdDataLayoutComponent):
    """
    """
    EVENTS = []
    data_model = AntdEachData

    def __init__(
            self,
            value: list | Callable = None,
            *,
            as_item: str | None = None,
            _internal: None = None,

            # gradio properties
            visible: bool = True,
            elem_id: str | None = None,
            elem_classes: list[str] | str | None = None,
            elem_style: dict | None = None,
            key: int | str | None = None,
            every: Timer | float | None = None,
            inputs: Component | list[Component] | set[Component] | None = None,
            render: bool = True,
            **kwargs):
        super().__init__(visible=visible,
                         render=render,
                         value=value,
                         as_item=as_item,
                         elem_id=elem_id,
                         elem_classes=elem_classes,
                         key=key,
                         elem_style=elem_style,
                         every=every,
                         inputs=inputs,
                         **kwargs)

    FRONTEND_DIR = resolve_frontend_dir("each", type='base')

    @property
    def skip_api(self):
        return False

    def preprocess(self, payload: list | AntdEachData) -> list:
        if isinstance(payload, AntdEachData):
            return payload.root
        return payload

    def postprocess(self, value: list) -> list:
        return value

    def example_payload(self) -> list:
        return []

    def example_value(self) -> list:
        return []
    from typing import TYPE_CHECKING, Any, Callable, Literal, Sequence

    from gradio.blocks import Block
    if TYPE_CHECKING:
        from gradio.components import Timer