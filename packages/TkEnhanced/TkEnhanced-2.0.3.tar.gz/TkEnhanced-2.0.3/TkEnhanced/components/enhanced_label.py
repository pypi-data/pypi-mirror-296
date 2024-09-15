# local imports:
from ..models import TransparentMisc, ReadableMisc
from ..utils import FontDescription, Constants

# standard libraries:
from tkinter import Event, Label, Misc
from typing import Any, Optional
from tkinter.font import Font


class EnhancedLabel(TransparentMisc, ReadableMisc, Label):
    MINIMUM_PADDING_X: int = 3

    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            background: Optional[str] = Constants.TRANSPARENT,
            foreground: Optional[str] = Constants.READABLE,
            padx: Optional[int] = MINIMUM_PADDING_X,
            text: Optional[str] = "Enhanced Label",
            truncatetext: bool = True,
            **options: Any) -> None:
        super().__init__(master, background=background, foreground=foreground, **options)
        self._text: str = ""
        self._truncate_text: bool = False
        self.configure(padx=padx, text=text, truncatetext=truncatetext)
        self.bind(sequence="<Configure>", func=self.on_configure, add=True)

    def on_configure(self, event: Optional[Event] = None) -> None:
        if not self._truncate_text:
            Misc.configure(self, text=self._text)
            return None
        font: FontDescription = self.cget(key="font")
        font = Font(font=font)
        label_width: int = self.winfo_width()
        minimum_width: int = font.measure(text=Constants.ELLIPSIS)
        if minimum_width > label_width:
            Misc.configure(self, text=Constants.ELLIPSIS)
            return None
        text: str = self._text
        text_width: int = font.measure(text)
        if text_width > label_width:
            text_width += minimum_width
            while text_width > label_width:
                text = text[:-1]
                text_width = font.measure(text=text + Constants.ELLIPSIS)
            text += Constants.ELLIPSIS
        Misc.configure(self, text=text)

    def configure(self, **options: Any) -> Any:
        padding_x: Optional[int] = options.get("padx", None)
        if isinstance(padding_x, int) and padding_x < self.MINIMUM_PADDING_X:
            error_message: str = "Number of \"padx\" must be at least {}.".format(self.MINIMUM_PADDING_X)
            raise ValueError(error_message)
        truncate_text: Optional[bool] = options.pop("truncatetext", None)
        result: Any = super().configure(**options)
        if truncate_text is not None:
            self._truncate_text = bool(truncate_text)
        if "text" in options:
            self._text = Misc.cget(self, key="text")
            self.after(ms=0, func=self.on_configure)
        return result
    config = configure

    def cget(self, key: str) -> Any:
        options: dict[str, Any] = {"text": self._text, "truncatetext": self._truncate_text}
        return options.get(key) if key in options else super().cget(key)
    __getitem__ = cget
