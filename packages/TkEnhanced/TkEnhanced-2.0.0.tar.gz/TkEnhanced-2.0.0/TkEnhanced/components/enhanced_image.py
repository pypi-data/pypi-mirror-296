# local imports:
from ..utils import PathDescription, SizeDescription, ResizeMode, Constants

# standard libraries:
from tkinter import TclError, Event, Label, Misc
from typing import Any, Optional
from threading import Thread
from os.path import exists

# third-party libraries:
from PIL.Image import Image, open as open_image
from PIL.ImageTk import PhotoImage


class EnhancedImage(Label):
    UPDATE_MILLISECONDS: int = 20

    @staticmethod
    def check_options(**options: Any) -> None:
        unknown_options: tuple[str, ...] = "activeforeground", "bitmap", "disabledforeground", "font", "foreground", "takefocus", "text", "textvariable", "underline", "wraplength"
        for option in unknown_options:
            if option not in options:
                continue
            error_message: str = "unknown option \"{}\"".format(option)
            raise TclError(error_message)

    @staticmethod
    def get_image_size(enhanced_image: "EnhancedImage", image: Image) -> tuple[int, int]:
        container_width: int = enhanced_image.winfo_width()
        container_height: int = enhanced_image.winfo_height()
        image_width, image_height = image.size
        if enhanced_image._width != Constants.AUTO:
            image_width = enhanced_image._width
        if enhanced_image._height != Constants.AUTO:
            image_height = enhanced_image._height
        if enhanced_image._resize_mode == Constants.CONTAIN:
            scaling_factor: int = min(container_width / image_width, container_height / image_height)
        elif enhanced_image._resize_mode == Constants.COVER:
            scaling_factor: int = max(container_width / image_width, container_height / image_height)
        new_image_width: int = int(image_width * scaling_factor)
        new_image_height: int = int(image_height * scaling_factor) - 4
        return 1 if new_image_width <= 0 else new_image_width, 1 if new_image_height <= 0 else new_image_height

    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            height: Optional[SizeDescription] = Constants.AUTO,
            image: Optional[PathDescription] = None,
            resizemode: ResizeMode = Constants.CONTAIN,
            width: Optional[SizeDescription] = Constants.AUTO,
            **options: Any) -> None:
        """
        Valid option names:
        activebackground, anchor, background, borderwidth, cursor, height, highlightbackground, highlightcolor,
        highlightthickness, image, justify, padx, pady, relief, resizemode, state, width.
        """
        self.check_options(**options)
        super().__init__(master, **options)
        self._height: SizeDescription = Constants.AUTO
        self._image: Optional[Image] = None
        self._image_path: Optional[PathDescription] = None
        self._photo_image: Optional[PhotoImage] = None
        self._resize_mode: ResizeMode = Constants.CONTAIN
        self._scheduled_update: Optional[str] = None
        self._width: SizeDescription = Constants.AUTO
        self.configure(height=height, image=image, resizemode=resizemode, width=width)
        self.bind(sequence="<Configure>", func=self.schedule_update, add=True)

    def schedule_update(self, event: Optional[Event] = None, milliseconds: int = UPDATE_MILLISECONDS) -> None:
        if self._scheduled_update is not None:
            self.after_cancel(id=self._scheduled_update)
            self._scheduled_update = None
        resize_thread: Thread = Thread(target=self.resize_image, daemon=True)
        self._scheduled_update = self.after(ms=milliseconds, func=resize_thread.start)

    def resize_image(self) -> None:
        if self._image is not None:
            new_image: Image = self._image.copy()
            new_size: tuple[int, int] = self.get_image_size(self, image=new_image)
            resized_image: Image = new_image.resize(size=new_size)
            self.update_image(image=resized_image)
        self._scheduled_update = None

    def update_image(self, image: Image) -> None:
        photo_image: PhotoImage = PhotoImage(image)
        if photo_image == self._photo_image:
            return None
        Misc.configure(self, image=photo_image)
        self._photo_image = photo_image

    def configure(self, **options: Any) -> Any:
        self.check_options(**options)
        resize_mode: Optional[ResizeMode] = options.pop("resizemode", None)
        if resize_mode is not None and resize_mode not in Constants.RESIZE_VALUES:
            error_message: str = "Invalid resize mode: \"{}\"".format(resize_mode)
            raise TclError(error_message)
        image: Optional[Image] = None
        image_path: Optional[PathDescription] = options.pop("image", None)
        if image_path:
            if not exists(path=image_path):
                error_message: str = "Image not found: \"{}\"".format(image_path)
                raise TclError(error_message)
            image = open_image(fp=image_path)
        height: Optional[SizeDescription] = options.get("height", None)
        if height == Constants.AUTO:
            options["height"] = 0 if image is None else image.height
        width: Optional[SizeDescription] = options.get("width", None)
        if width == Constants.AUTO:
            options["width"] = 0 if image is None else image.width
        result: Any = super().configure(**options)
        if width is not None:
            self._width = width
        if height is not None:
            self._height = height
        if image_path == "":
            self._image = self._image_path = self._photo_image = None
        elif image_path is not None:
            self._image = image
            self._image_path = image_path
            self.schedule_update(milliseconds=0)
        if resize_mode is not None:
            self._resize_mode = resize_mode
        return result
    config = configure

    def cget(self, key: str) -> Any:
        self.check_options(key=None)
        options: dict[str, Any] = {
            "height": self._height,
            "image": self._image_path,
            "resizemode": self._resize_mode,
            "width": self._width}
        return options.get(key) if key in options else super().cget(key)
    __getitem__ = cget
