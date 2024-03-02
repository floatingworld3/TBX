import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from .styles import *
from copy import deepcopy
from PIL import Image, ImageTk


class TypedEntry(tk.Entry):
    def __init__(self, master=None, default=None, entry_type=None, value_min=None,
                 value_max=None, callback=None, index=None, **kwargs):
        self.content = tk.StringVar()
        if callback:
            self.content.trace_add('write', callback=callback)
        self.entry_type = entry_type if entry_type is not None else str
        tk.Entry.__init__(self, master, textvariable=self.content, **kwargs)
        self.kwargs = kwargs
        self.get = self.content.get
        self.value_min = value_min
        self.value_max = value_max

        default = default if default is not None else str
        self.default = self.apply_range(default)
        self.old = default
        self.content.set(self.default)

        self.bind("<FocusOut>", self.handle_empty)
        self.bind("<Return>", self.handle_empty)
        self.configure_entry()

    def add_callback(self, callback):
        self.content.trace_add('write', callback=callback)

    def configure_entry(self):
        config = deepcopy(entry)
        config.update(self.kwargs)
        self.configure(**config)

    def handle_empty(self, *args):
        if not self.get():
            self.set(self.default)
        else:
            try:
                self.set(self.get())
            except:
                self.set(self.default)

    def apply_range(self, value):
        value = max(value, self.value_min) if self.value_min is not None else value
        value = min(value, self.value_max) if self.value_max is not None else value
        return value

    def set(self, value):
        self.content.set(self.apply_range(self.entry_type(value)))


class PlaceHolderEntry(tk.Entry):
    def __init__(
            self, master,
            placeholder="",
            on_edit_callback=None,
            on_finish_callback=None,
            **kwargs):
        tk.Entry.__init__(self, master, **kwargs)
        self.kwargs = kwargs
        self.placeholder = placeholder
        self.insert(0, self.placeholder)
        self._is_empty = True
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<KeyRelease>", self.on_key_press)
        self.bind("<Return>", self.on_key_press)
        self.bind("<Return>", self.on_edit_finished)
        self.on_finish_callback = on_finish_callback
        self.on_edit_callback = on_edit_callback
        self.configure_entry()

    def configure_entry(self):
        config = deepcopy(placeholder_entry)
        config.update(self.kwargs)
        self.configure(**config)

    def on_focus_in(self, event):
        if self._is_empty:
            self.delete(0, tk.END)
            self._is_empty = False

    def on_focus_out(self, event):
        if self.get() == '':
            self.insert(0, self.placeholder)
            self.config(fg=COLOR_TEXT_PASSIVE)
            self._is_empty = True
        self.on_edit_finished(event)

    def on_key_press(self, event):
        if self.get() == '':
            self._is_empty = True
        else:
            self._is_empty = False
        self.config(fg=COLOR_TEXT)
        if self.on_edit_callback:
            self.on_edit_callback()

    def set_text(self, text):
        self.delete(0, tk.END)
        self.insert(0, text)
        self.config(fg=COLOR_TEXT)
        self._is_empty = False

    def get_text(self):
        text = "" if self._is_empty else self.get()
        return text

    def on_edit_finished(self, event=None, callback=None):
        if self.get_text():
            if self.on_finish_callback:
                self.on_finish_callback()


class Button(tk.Button):
    def __init__(self, master, **kwargs):
        tk.Button.__init__(self, master, **kwargs)
        self.kwargs = kwargs
        self.pixel = tk.PhotoImage()
        config = deepcopy(button)
        config.update(kwargs)
        self.configure(image=self.pixel, **config)

    def disable(self):
        config = deepcopy(button_disabled)
        config.update(self.kwargs)
        self.configure(state="disabled", **config)

    def enable(self):
        config = deepcopy(button)
        config.update(self.kwargs)
        self.configure(state="normal", **config)


class LabeledCheckbutton(tk.Frame):
    def __init__(self, master, text="", **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.on = tk.PhotoImage(width=14, height=14)
        self.on.put(("#5680C2",), to=(0, 0, 12, 12))
        self.off = tk.PhotoImage(width=14, height=14)
        self.off.put((), to=(0, 0, 14, 14))
        self.checkbutton = tk.Checkbutton(self,
                                          bd=0,
                                          background="#FFFFFF",
                                          activebackground="#FFFFFF",
                                          indicatoron=False,
                                          image=self.off,
                                          selectimage=self.on,
                                          onvalue=1, offvalue=0,
                                          **kwargs)
        self.label = tk.Label(self, text=text)
        self.label.grid(row=0, column=0)
        self.checkbutton.grid(row=0, column=1)


class PathExplorerFrame(tk.Frame):
    def __init__(self, master,
                 on_finish_callback=None,
                 on_edit_callback=None,
                 **kwargs):
        tk.Frame.__init__(self, master)
        self.kwargs = kwargs
        self.configure(bg=COLOR_DEPRESSED)

        placeholder = self.kwargs.get("placeholder", "")
        self.mode = self.kwargs.get("mode", "open")
        self.entry = PlaceHolderEntry(
            self, placeholder=placeholder,
            on_edit_callback=on_edit_callback,
            on_finish_callback=on_finish_callback
        )
        self.entry.grid(row=0, column=1, columnspan=3, padx=0, pady=0)

        self.button = Button(self, width=64, text="Open", command=self.set_file_name)
        self.button.grid(row=0, column=4, columnspan=1, padx=0, pady=0)

    def set_file_name(self):
        file_types = self.kwargs.get("file_types")
        if self.mode == "save":
            file_name = filedialog.asksaveasfilename(filetypes=file_types)
        else:
            file_name = filedialog.askopenfilename(filetypes=file_types)

        if file_name:
            self.entry.set_text(file_name)
            self.entry.on_edit_finished()

    def get_filename(self):
        return self.entry.get_text()


class LabelledWidget(tk.Frame):
    def __init__(self, master, text="", label_pad=(0, 0), widget=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.label = tk.Label(self, text=text)
        self.init_label(label_pad)
        self.widget = widget
        self.config(**frame)

    def init_label(self, padx):
        self.label.configure(**label)
        self.label.grid(row=0, column=0, padx=padx)


class SceneFrame(tk.LabelFrame):
    def __init__(self, master, **kwargs):
        tk.LabelFrame.__init__(self, master, **kwargs)
        self.configure(text="Scene", **label_frame)

        self.fps = TypedEntry(self, entry_type=float, default=30.0, value_min=1.0, bd=0)
        self.fps.grid(row=0, column=1)
        self.fps_frame = LabelledWidget(
            self, text="Frame Rate",
            label_pad=(0, 16),
            widget=self.fps,
        )
        self.fps_frame.grid(row=0, column=0, sticky="e")

        self.up_vector_var = tk.StringVar(value="Y")
        self.up_vector_combo = tk.OptionMenu(self, self.up_vector_var, 'Y','Z')
        self.arrow = tk.PhotoImage(file='./assets/arrow.gif')
        self.up_vector_combo.configure(image=self.arrow, **combo)

        self.up_vector_combo.grid(row=1, column=1)
        self.up_vector_frame = LabelledWidget(
            self, text="Up Vector",
            label_pad=(0, 16),
            widget=self.up_vector_combo,
        )
        self.up_vector_frame.grid(row=1, column=0, sticky="e")

    def get_state(self):
        fps = float(self.fps.get())
        up_vector = self.up_vector_var.get()
        state = dict(up_vector=up_vector, fps=fps)
        return state


class ClipFrame(tk.LabelFrame):
    def __init__(self, master, **kwargs):
        tk.LabelFrame.__init__(self, master, **kwargs)
        self.configure(text="Clip Range", **label_frame)

        self.start_frame = TypedEntry(self, entry_type=int, default=1, value_min=1, bd=0)
        self.start_frame.grid(row=0, column=1)
        self.start_frame_frame = LabelledWidget(
            self, text="Start Frame",
            label_pad=(0, 16),
            widget=self.start_frame,
        )
        self.start_frame_frame.grid(row=0, column=0, sticky="e")

        self.end_frame = TypedEntry(self, entry_type=int, default=99999, value_min=1, bd=0)
        self.end_frame.grid(row=1, column=1)
        self.end_frame_frame = LabelledWidget(
            self, text="End Frame",
            label_pad=(0, 16),
            widget=self.end_frame,
        )
        self.end_frame_frame.grid(row=1, column=0, sticky="e")

    def get_state(self):
        start_frame = int(self.start_frame.get())
        end_frame = int(self.end_frame.get())
        state = dict(start_frame=start_frame, end_frame=end_frame)
        return state


class MaskFrame(tk.LabelFrame):
    def __init__(self, master, **kwargs):
        tk.LabelFrame.__init__(self, master, **kwargs)
        self.configure(text="Mask", **label_frame)

        self.rotation_x = TypedEntry(self, entry_type=float, default=0.0, bd=0)
        self.rotation_x.grid(row=0, column=1)
        self.rotation_x_frame = LabelledWidget(
            self, text="Rotation X",
            label_pad=(0, 16),
            widget=self.rotation_x,
        )
        self.rotation_x_frame.grid(row=0, column=0, sticky="e")

        self.rotation_y = TypedEntry(self, entry_type=float, default=180.0, bd=0)
        self.rotation_y.grid(row=1, column=1)
        self.rotation_y_frame = LabelledWidget(
            self, text="Y",
            label_pad=(0, 16),
            widget=self.rotation_y,
        )
        self.rotation_y_frame.grid(row=1, column=0, sticky="e")

        self.rotation_z = TypedEntry(self, entry_type=float, default=180.0, bd=0)
        self.rotation_z.grid(row=2, column=1)
        self.rotation_z_frame = LabelledWidget(
            self, text="Z",
            label_pad=(0, 16),
            widget=self.rotation_z,
        )
        self.rotation_z_frame.grid(row=2, column=0, sticky="e")

        self.apply_position_var = tk.BooleanVar()
        self.on_check = tk.PhotoImage(width=7, height=7)
        self.on_check.put((COLOR_TEXT), to=(0, 0, 6, 6))
        self.on_uncheck = tk.PhotoImage(width=7, height=7)
        self.on_uncheck.put((), to=(0, 0, 6, 6))
        self.apply_position = tk.Checkbutton(
            self, image=self.on_uncheck,
            selectimage=self.on_check,
            variable=self.apply_position_var
        )
        self.apply_position.configure(**checkbox)

        self.apply_position.grid(row=3, column=1)
        self.apply_position_frame = LabelledWidget(
            self, text="Apply Position",
            label_pad=(0, 16),
            widget=self.apply_position,
        )
        self.apply_position_frame.grid(row=3, column=0, sticky="e")
        # Marker
        self.marker_scale = TypedEntry(self, entry_type=float, default=3.0, value_min=0.1, bd=0)
        self.marker_scale.grid(row=4, column=1)
        self.marker_scale_frame = LabelledWidget(
            self, text="Marker Scale",
            label_pad=(0, 16),
            widget=self.marker_scale,
        )
        self.marker_scale_frame.grid(row=4, column=0, sticky="e")

        self.root_scale = TypedEntry(self, entry_type=float, default=5.0, value_min=0.1, bd=0)
        self.root_scale.grid(row=5, column=1)
        self.root_scale_frame = LabelledWidget(
            self, text="Root Scale",
            label_pad=(0, 16),
            widget=self.root_scale,
        )
        self.root_scale_frame.grid(row=5, column=0, sticky="e")

        self.marker_prefix = TypedEntry(self, default="", bd=0)
        self.marker_prefix.grid(row=6, column=1)
        self.marker_prefix_frame = LabelledWidget(
            self, text="Marker Prefix",
            label_pad=(0, 16),
            widget=self.root_scale,
        )
        self.marker_prefix_frame.grid(row=6, column=0, sticky="e")

        self.local_rotation_x = TypedEntry(self, entry_type=float, default=0.0, bd=0)
        self.local_rotation_x.grid(row=7, column=1)
        self.local_rotation_x_frame = LabelledWidget(
            self, text="Local Rotation X",
            label_pad=(0, 16),
            widget=self.local_rotation_x,
        )
        self.local_rotation_x_frame.grid(row=7, column=0, sticky="e")

        self.local_rotation_y = TypedEntry(self, entry_type=float, default=0.0, bd=0)
        self.local_rotation_y.grid(row=8, column=1)
        self.local_rotation_y_frame = LabelledWidget(
            self, text="Y",
            label_pad=(0, 16),
            widget=self.local_rotation_y,
        )
        self.local_rotation_y_frame.grid(row=8, column=0, sticky="e")

        self.local_rotation_z = TypedEntry(self, entry_type=float, default=0.0, bd=0)
        self.local_rotation_z.grid(row=9, column=1)
        self.local_rotation_z_frame = LabelledWidget(
            self, text="Z",
            label_pad=(0, 16),
            widget=self.local_rotation_z,
        )
        self.local_rotation_z_frame.grid(row=9, column=0, sticky="e")

    def get_state(self):
        rotation = (
            float(self.rotation_x.get()),
            float(self.rotation_y.get()),
            float(self.rotation_z.get()),
        )
        apply_position = self.apply_position_var.get()
        marker_scale = float(self.marker_scale.get())
        root_scale = float(self.root_scale.get())
        marker_prefix = self.marker_prefix.get()

        local_rotation = (
            float(self.local_rotation_x.get()),
            float(self.local_rotation_y.get()),
            float(self.local_rotation_z.get()),
        )
        state = dict(
            rotation=rotation,
            local_rotation=local_rotation,
            apply_position=apply_position,
            marker_scale=marker_scale,
            root_scale=root_scale,
            marker_prefix=marker_prefix
        )
        return state


class ProgressBarFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master)
        self.configure(**frame)

        self.label = tk.Label(self)
        self.label.configure(**label)

        self.progress_bar = ttk.Progressbar(self)
        self.progress_bar.configure(**progress_bar)

        self.show()
        self.update()
        self.hide()

    def error(self, msg=""):
        self.label.configure(text=msg, fg="#986d6d", bg="#5a3535", width=len(msg), height=1, bd=0)

    def info(self, msg=""):
        self.label.configure(text=msg, fg="#AAAAAA", bg="#383838", width=len(msg), height=1, bd=0)

    def warn(self, msg=""):
        self.label.configure(text=msg, fg="#8e9262", bg="#5a5835", width=len(msg), height=1, bd=0)

    def hide(self):
        self.progress_bar.grid_forget()
        self.label.grid(row=0, column=0, pady=(0,5))
        self.info()

    def show(self):
        self.progress_bar.grid(row=0, column=0)
        self.label.grid_forget()

    def set(self, value=0):
        self.progress_bar["value"] = value
        self.update()


class CopyrightFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(**frame)

        self.im = ImageTk.PhotoImage(file="./assets/tbx_logo.png")
        self.logo = tk.Canvas(self, **canvas)
        self.logo.create_image(30, 35, image=self.im)
        self.logo.grid(row=0, column=0, padx=(32, 0), sticky="s")

        self.description_label = tk.Label(self, text="Tracking Data to FBX Conversion")
        config = deepcopy(label)
        config.update(fg=COLOR_TEXT)
        self.description_label.configure(config)
        self.description_label.grid(row=0, column=1, padx=(108, 0), sticky="s")

        self.copyright_label = tk.Label(self, text=u"\u00A9 Rig Vadar Systems",)
        self.copyright_label.configure(config)
        self.copyright_label.grid(row=0, column=2, padx=(78, 0), sticky="es")