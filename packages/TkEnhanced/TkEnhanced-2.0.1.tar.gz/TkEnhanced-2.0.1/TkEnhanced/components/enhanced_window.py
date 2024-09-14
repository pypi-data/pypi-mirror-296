# local imports:
from ..models import TransparentMisc
from ..utils import Constants

# standard libraries:
from tkinter import Toplevel, Event, Misc, Wm, Tk
from ctypes import windll, WinDLL
from typing import Any, Optional
from enum import IntEnum


class WindowIndexes(IntEnum):
    WINDOW_STYLE: int = -16
    EXTENDED_WINDOW_STYLE: int = -20


class WindowStyles(IntEnum):
    MAXIMIZE: int = 0x00010000
    MINIMIZE: int = 0x00020000
    RESIZE: int = 0x00040000


class ExtendedWindowStyles(IntEnum):
    TASKBAR: int = 0x00040000


class WindowUtils:
    _graphics_api: WinDLL = windll.gdi32
    _windows_api: WinDLL = windll.user32

    def __init__(self, master: "EnhancedWindow") -> None:
        assert isinstance(master, EnhancedWindow), "This object must be an instance of EnhancedWindow."
        self.master: EnhancedWindow = master
        self._updated_size: tuple[int, int] = 0, 0
        self._updated_styles: dict[int, int] = {}

    def _on_update_size(self, event: Event) -> None:
        if self._updated_size == (event.width, event.height):
            return None
        self._updated_size = event.width, event.height
        if event.widget != self.master or not self.master.wm_overrideredirect():
            return None
        window_id: int = self.retrieve_window_handle()
        is_width_resizable, is_height_resizable = self.master.wm_resizable()
        start_x: int = 6 if is_width_resizable else 7
        start_y: int = 6 if is_height_resizable else 7
        end_x: int = event.width + (8 if is_width_resizable else 7)
        end_y: int = event.height + (8 if is_height_resizable else 7)
        new_region: int = self._graphics_api.CreateRectRgn(start_x, start_y, end_x, end_y)
        self._windows_api.SetWindowRgn(window_id, new_region, True)

    def retrieve_window_handle(self) -> int:
        self.master.update_idletasks()
        window_id: int = self.master.winfo_id()
        window_handle: int = self._windows_api.GetParent(window_id)
        return window_handle

    def center_window(self, width: int, height: int) -> None:
        screen_width: int = self.master.winfo_screenwidth()
        screen_height: int = self.master.winfo_screenheight()
        center_x: int = (screen_width - width)//2
        center_y: int = (screen_height - height)//2
        new_geometry: str = "{}x{}+{}+{}".format(width, height, center_x, center_y)
        self.master.wm_geometry(newGeometry=new_geometry)

    def hide_titlebar(self) -> None:
        if self.master.wm_overrideredirect():
            return None
        self.master.wm_overrideredirect(boolean=True)
        window_handle: int = self.retrieve_window_handle()
        self._updated_styles[WindowIndexes.WINDOW_STYLE] = self._windows_api.GetWindowLongPtrW(
            window_handle,
            WindowIndexes.WINDOW_STYLE)
        self._updated_styles[WindowIndexes.EXTENDED_WINDOW_STYLE] = self._windows_api.GetWindowLongPtrW(
            window_handle,
            WindowIndexes.EXTENDED_WINDOW_STYLE)
        new_styles: dict[int, int] = {
            WindowIndexes.WINDOW_STYLE: WindowStyles.MAXIMIZE | WindowStyles.MINIMIZE | WindowStyles.RESIZE,
            WindowIndexes.EXTENDED_WINDOW_STYLE: ExtendedWindowStyles.TASKBAR}
        for index, style in new_styles.items():
            self._windows_api.SetWindowLongPtrW(window_handle, index, style)
        is_window_shown: bool = self.master.wm_state() != "withdrawn"
        if is_window_shown:
            self.master.wm_deiconify()

    def show_titlebar(self) -> None:
        if not self.master.wm_overrideredirect():
            return None
        window_handle: int = self.retrieve_window_handle()
        for index, style in self._updated_styles.items():
            self._windows_api.SetWindowLongPtrW(window_handle, index, style)
        self._updated_styles.clear()
        self.master.wm_overrideredirect(boolean=False)


class EnhancedWindow(Misc, Wm):
    def __init__(self, **options: Any) -> None:
        super().__init__(**options)
        self.utils: WindowUtils = WindowUtils(self)
        self.bind(sequence="<Configure>", func=self.utils._on_update_size, add=True)

    def configure(self, **options: Any) -> Any:
        result: Any = super().configure(**options)
        if Constants.BACKGROUND_KEYS & options.keys():
            def update_children() -> None: TransparentMisc.update_children(self)
            self.after(ms=0, func=update_children)
        return result
    config = configure


class EnhancedTk(EnhancedWindow, Tk):
    def __init__(self, *, className: str = "TkEnhanced", **options: Any) -> None:
        super().__init__(className=className, **options)


class EnhancedToplevel(EnhancedWindow, Toplevel):
    def __init__(self, master: Optional[Misc] = None, *, modal: bool = False, **options: Any) -> None:
        super().__init__(master=master, **options)
        if modal:
            self.grab_set()
            self.master.wait_window(self)
            self.grab_release()
