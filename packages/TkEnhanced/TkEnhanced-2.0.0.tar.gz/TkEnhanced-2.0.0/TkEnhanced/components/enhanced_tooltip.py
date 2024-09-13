# local imports:
from . import EnhancedToplevel, EnhancedLabel

# standard libraries:
from tkinter import TclError, Event, Misc
from typing import Any, Optional


class EnhancedTooltip(EnhancedToplevel):
    @staticmethod
    def check_options(**options: Any) -> None:
        unknown_options: tuple[str, ...] = "centerwindow", "height", "hidetitlebar", "icopath", "menu", "screen", "title", "width"
        for option in unknown_options:
            if option not in options:
                continue
            error_message: str = "unknown option \"{}\"".format(option)
            raise TclError(error_message)

    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            text: Optional[str] = "Enhanced Tooltip",
            **options: Any) -> None:
        """
        Valid option names:
        background, bd, bg, borderwidth, class, colormap, container, cornerradius, cursor,
        font, height, highlightbackground, highlightcolor, highlightthickness, relief,
        takefocus, text, use, visual, width.
        """
        self.check_options(**options)
        super().__init__(master, centerwindow=False, height=0, title=text, width=0, **options)
        self.setup_tooltip(text)
        self.master.bind(sequence="<Enter>", func=self.show_tooltip, add=True)
        self.master.bind(sequence="<Motion>", func=self.update_position, add=True)
        self.master.bind(sequence="<Leave>", func=self.hide_tooltip, add=True)

    def on_configure(self, event: Event) -> None:
        if self._last_size == (event.width, event.height):
            return None
        self._last_size = event.width, event.height
        window_id: int = self.utils.retrieve_window_handle()
        start_x: int = 8
        start_y: int = 8
        end_x: int = event.width+9
        end_y: int = event.height+(9 if self.wm_overrideredirect() else 32)
        radius: int = self._corner_radius
        new_region: Optional[int] = self.utils.graphics_api.CreateRoundRectRgn(
            start_x,
            start_y,
            end_x,
            end_y,
            radius,
            radius)
        if new_region is None:
            return None
        self.utils.windows_api.SetWindowRgn(window_id, new_region, True)

    def setup_tooltip(self, text: Optional[str] = None) -> None:
        self.configure(padx=2, pady=2)
        self.hide_tooltip()
        self._label: EnhancedLabel = EnhancedLabel(self, text=text)
        self._label.pack_configure(expand=True, fill="both")

    def show_tooltip(self, event: Event) -> None:
        self.update_position(event)
        self.wm_deiconify()

    def update_position(self, event: Event) -> None:
        x_position: int = event.x_root + 6
        y_position: int = event.y_root + 6
        new_position: str = "+{}+{}".format(x_position, y_position)
        self.wm_geometry(newGeometry=new_position)

    def hide_tooltip(self, event: Optional[Event] = None) -> None:
        self.wm_withdraw()

    def configure(self, **options: Any) -> None:
        text: Optional[str] = options.pop("text", None)
        if text is not None:
            self._label.configure(text=text)
        super().configure(**options)
    config = configure

    def cget(self, key: str) -> Any:
        return self._label.cget(key="text") if key == "text" else super().cget(key)
    __getitem__ = cget
