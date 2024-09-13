# local imports:
from ..utils import FontDescription, PathDescription
from ..models import TransparentMisc

# standard libraries:
from typing import Any, TypeAlias, Optional, Final
from tkinter import Toplevel, Event, Misc, Wm, Tk
from ctypes import windll, WinDLL
from os.path import exists


class WindowIndexes:
    WINDOW_STYLE: Final[int] = -16
    EXTENDED_WINDOW_STYLE: Final[int] = -20


class WindowStyles:
    BORDER: Final[int] = 0x00800000
    MAXIMIZE: Final[int] = 0x00010000
    MINIMIZE: Final[int] = 0x00020000
    RESIZE: Final[int] = 0x00040000


class ExtendedWindowStyles:
    TASKBAR: Final[int] = 0x00040000


class WindowStates:
    SHOWN: Final[int] = 5


class WindowUtils:
    def __init__(self, master: "EnhancedWindow") -> None:
        assert isinstance(master, EnhancedWindow), "This object must be an instance of EnhancedWindow."
        self.graphics_api: WinDLL = windll.gdi32
        self.windows_api: WinDLL = windll.user32
        self.master: EnhancedWindow = master

    def retrieve_window_handle(self) -> int:
        self.master.update_idletasks()
        window_id: int = self.master.winfo_id()
        window_handle: int = self.windows_api.GetParent(window_id)
        return window_handle

    def center_window(self, width: int, height: int) -> None:
        screen_width: int = self.master.winfo_screenwidth()
        screen_height: int = self.master.winfo_screenheight()
        center_x: int = (screen_width - width)//2
        center_y: int = (screen_height - height)//2
        new_geometry: str = "{}x{}+{}+{}".format(width, height, center_x, center_y)
        self.master.wm_geometry(newGeometry=new_geometry)

    def hide_titlebar(self) -> None:
        self.master.wm_overrideredirect(boolean=True)
        window_handle: int = self.retrieve_window_handle()
        self.windows_api.SetWindowLongPtrW(
            window_handle,
            WindowIndexes.WINDOW_STYLE,
            WindowStyles.MAXIMIZE | WindowStyles.MINIMIZE | WindowStyles.BORDER | WindowStyles.RESIZE)
        self.windows_api.SetWindowLongPtrW(
            window_handle,
            WindowIndexes.EXTENDED_WINDOW_STYLE,
            ExtendedWindowStyles.TASKBAR)
        is_window_hidden: bool = self.master.wm_state() == "withdrawn"
        if is_window_hidden:
            return None
        self.windows_api.ShowWindow(window_handle, WindowStates.SHOWN)

    def show_titlebar(self) -> None:
        self.master.wm_overrideredirect(boolean=False)


IcoPath: TypeAlias = Optional[PathDescription]


class EnhancedWindow(Misc, Wm):
    def __init__(
            self,
            *,
            centerwindow: bool = True,
            cornerradius: int = 10,
            font: Optional[FontDescription] = None,
            height: int = 400,
            hidetitlebar: bool = True,
            icopath: IcoPath = None,
            title: str = "Enhanced Window",
            width: int = 500,
            **options: Any) -> None:
        """
        Valid option names:
        centerwindow, cornerradius, font, height, hidetitlebar, icopath, title, width.
        """
        super().__init__(**options)
        self._corner_radius = 0
        self._last_size: tuple[int, int] = width, height
        self.utils: WindowUtils = WindowUtils(self)
        self.wm_title(string=title)
        if icopath and exists(path=icopath):
            self.wm_iconbitmap(default=icopath)
        if font is not None:
            self.option_add(pattern="*font", value=font)
        self.utils.hide_titlebar()
        if not hidetitlebar:
            self.utils.show_titlebar()
        self.wm_minsize(width, height)
        if centerwindow:
            self.utils.center_window(width, height)
        self.configure(cornerradius=cornerradius)
        self.bind(sequence="<Configure>", func=self.on_configure, add=True)

    def on_configure(self, event: Event) -> None:
        if event.widget != self:
            return None
        if self._last_size == (event.width, event.height):
            return None
        self._last_size = event.width, event.height
        window_id: int = self.utils.retrieve_window_handle()
        start_x: int = 6
        start_y: int = 6
        end_x: int = event.width+11
        end_y: int = event.height+(11 if self.wm_overrideredirect() else 34)
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

    def configure(self, **options: Any) -> Any:
        corner_radius: Optional[Any] = options.pop("cornerradius", None)
        if corner_radius is not None and not isinstance(corner_radius, int):
            raise ValueError("The \"cornerradius\" must be an integer.")
        result: Any = super().configure(**options)
        background_color: Optional[str] = options.get("background", None)
        background_color = options.get("bg", background_color)
        if background_color is not None:
            def update_children() -> None: return TransparentMisc.update_children(self)
            self.after(ms=0, func=update_children)
        if corner_radius is not None:
            self._corner_radius = corner_radius
        return result
    config = configure

    def cget(self, key: str) -> Any:
        return self._corner_radius if key == "cornerradius" else super().cget(key)

    def keys(self) -> list[str]:
        keys: list[str] = super().keys()
        keys.append("cornerradius")
        return sorted(keys)


class EnhancedTk(EnhancedWindow, Tk):
    def __init__(
            self,
            *,
            background: Optional[str] = "#f0f0f0",
            title: str = "Enhanced Tk",
            **options: Any) -> None:
        super().__init__(className="TkEnhanced", title=title, **options)
        if background is not None:
            self.tk_setPalette(background=background)


class EnhancedToplevel(EnhancedWindow, Toplevel):
    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            modal: bool = False,
            title: str = "Enhanced Toplevel",
            **options: Any) -> None:
        super().__init__(master=master, title=title, **options)
        if modal:
            self.grab_set()
            self.master.wait_window(self)
            self.grab_release()
