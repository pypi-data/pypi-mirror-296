from __future__ import annotations

from typing import Any

from gradio.component_meta import ComponentMeta
from gradio.components.base import BlockContext
from gradio.events import Dependency

from ....utils.dev import resolve_frontend_dir

class AntdFragment(BlockContext, metaclass=ComponentMeta):
    """
    """
    EVENTS = []

    def __init__(self,
                 slot: str,
                 *,
                 visible: bool = True,
                 render: bool = True):
        super().__init__(visible=visible, render=render)
        self._internal = dict()
        if isinstance(self.parent, AntdFragment):
            self.slot = f"{self.parent.slot}.{slot}"
        else:
            self.slot = slot

    FRONTEND_DIR = resolve_frontend_dir("fragment", type='atom')

    @property
    def skip_api(self):
        return True

    def preprocess(self, payload: None) -> None:
        return payload

    def postprocess(self, value: None) -> None:

        return value

    def example_payload(self) -> Any:
        return None

    def example_value(self) -> Any:
        return None
class AntdSlot(AntdLayoutComponent):
    """
    """
    EVENTS = []

    def __init__(self,
                 value: str = '',
                 params_mapping: str | None = None,
                 *,
                 skip_context_value: bool = True,
                 as_item: str | None = None,
                 _internal: None = None,
                 visible: bool = True,
                 render: bool = True,
                 **kwargs):
        super().__init__(visible=visible,
                         render=render,
                         as_item=as_item,
                         **kwargs)
        self.params_mapping = params_mapping
        self.skip_context_value = skip_context_value
        if isinstance(self.parent, AntdSlot):
            self.value = f"{self.parent.value}.{value}"
        else:
            self.value = value

    FRONTEND_DIR = resolve_frontend_dir("slot", type='base')

    @property
    def skip_api(self):
        return True

    def preprocess(self, payload: str) -> str:
        return payload

    def postprocess(self, value: str) -> str:

        return value

    def example_payload(self) -> Any:
        return None

    def example_value(self) -> Any:
        return None
    from typing import TYPE_CHECKING, Any, Callable, Literal, Sequence

    from gradio.blocks import Block
    if TYPE_CHECKING:
        from gradio.components import Timer

    