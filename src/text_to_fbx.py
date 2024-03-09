import math
import os
import tkinter as tk
from functools import partial
import shutil
from tkinter import ttk, HORIZONTAL, X, BOTH, CENTER
from tkinter.tix import Tk
from .styles import COLOR_TEXT, checkbox
import fbx, fbxsip
import numpy as np
import pandas as pd
import ffmpeg
import webbrowser
from moviepy.video.io.VideoFileClip import VideoFileClip
from .styles import COLOR_BASE
from .ui_file import LabelledWidget
from .ui_file import PathExplorerFrame, ProgressBarFrame, MaskFrame, \
    SceneFrame, Button, CopyrightFrame, ClipFrame
from .vadar_parser import RigVadarDataParser
from .unreal_mappings import UnrealMapper
from .ui_file import TypedEntry
import pickle

VALID_HEADERS = ["Rig Vadar Facial Performance Analysis", ]
SAVING_FRAMES_PER_SECOND = 30
DOCUMENTATION_URL = os.path.join(os.path.abspath(os.getcwd()) , "documentation/home.html")



class UnrealScaleWindow(object):
    def __init__(self, master):
        top=self.top=tk.Toplevel(master)
        self.frame = tk.Frame(top, bg='#383838')
        self.frame.grid(row=0, column=0)

        mapper = UnrealMapper()
        self.frame.inputs = []
        self.frame.inputs_frame = []
        self.mappings = {}
        self.mappings_index = []
        max_rows_per_column = 20

        try:
            with open('unreal_mappings.pkl' ,'rb') as f:
                saved_inputs = pickle.load(f)
        except Exception:
            saved_inputs = {}
        
        for i, marker in enumerate(mapper.markers.keys()):
            column_index = i // max_rows_per_column
            row_index = i % max_rows_per_column

            self.mappings[marker] = i
            self.mappings_index.append(marker)
            self.frame.inputs.append(TypedEntry(self.frame, entry_type=float, default=float(saved_inputs.get(marker, 5)), value_min=0.1, bd=0, callback=self.on_scale_input_change, index=i))
            self.frame.inputs[-1].grid(row=row_index, column=1 + column_index * 2)
            
            self.frame.inputs_frame.append(LabelledWidget(
                self.frame, text=marker,
                label_pad=(16, 16),
                widget=self.frame.inputs[-1],
            ))
            self.frame.inputs_frame[-1].grid(row=row_index, column=column_index * 2, sticky="e")

    def on_scale_input_change(self, *args):
        inputs = {self.mappings_index[i]: input.get() for i, input in enumerate(self.frame.inputs)}
        if len(inputs.keys()) == 61:
            with open('unreal_mappings.pkl' ,'wb') as f:
                pickle.dump(inputs, f)
                print()

    def get_state(self, marker):
        return self.frame.inputs[self.mappings[marker]].get()

    def cleanup(self):
        self.top.destroy()

class TxtToFbx(tk.Frame):
    valid_headers = [h.replace(" ", "") for h in VALID_HEADERS]

    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, bg=COLOR_BASE)
        self.master = master
        self.pack(pady=15)
        self.scene = None
        self.manager = None
        self.parser = RigVadarDataParser()
        self.progress = ProgressBarFrame(self)
        self.progress.grid(row=12, column=0, columnspan=12, pady=(16, 16), )

        # Define column configurations (example)
        for i in range(12):
            self.grid_columnconfigure(i, weight=1)
            
        self.video_to_frame_button = Button(self, text="Extract", command=self.video_to_frame, width=140)
        self.video_to_frame_button.grid(row=9, column=0, columnspan=5, padx=10, pady=10)

        # Convert FBX Button
        self.convert_button = Button(self, text="Convert FBX", command=self.convert, width=140)
        self.convert_button.grid(row=10, column=0, columnspan=5, padx=5, pady=2)
        
        # Convert Unreal Button
        self.convert_unreal = Button(self, text="Convert Unreal", command=self.generate_unreal_csv, width=140)
        self.convert_unreal.grid(row=11, column=0, columnspan=5, padx=5, pady=2)

        self.unreal_scale_open_btn = Button(self, text="Edit scale", command=self.open_unreal_scale_window)
        self.unreal_scale_open_btn.grid(row=11, column=8, padx=5, pady=2)

        self.unreal_root_scale_frame = LabelledWidget(
            self, text="Unreal Root Scale: Custom",
            label_pad=(0, 16),
            widget=self.unreal_scale_open_btn,
        )
        self.unreal_root_scale_frame.grid(row=11, column=6, sticky="e")


        vadar_file_types = (("Rig vadar file", "*.txt"), ("Rig vadar file", "*.csv"))
        self.vadar_explorer = PathExplorerFrame(
            self, placeholder="",
            file_types=vadar_file_types,
            on_finish_callback=self.verify_vadar,
            on_edit_callback=self.verify_vadar,
        )
        self.title_label = LabelledWidget(
            self, text="Tracking data to FBX Conversion ",
            label_pad=(0, 16),
            widget=self.vadar_explorer,
        )
        self.title_label.grid(row=0, column=4, sticky="e", padx=5, pady=5)

        self.help_button = Button(self, text="Help", command=self.launch_documentation, width=70, height=20)
        self.help_button.grid(row=12, column=11, sticky="e", padx=(0,20), pady=5)

        self.frame_title = LabelledWidget(
            self, text="Frames and Audio Extraction",
            label_pad=(40, 16),
            widget=self.vadar_explorer,
        )

        self.frame_title.grid(row=5, column=4, sticky="n", padx=5, pady=0)
        self.vadar_explorer.grid(row=1, column=1, columnspan=12, pady=(0, 0))
        self.vadar_explorer_label = LabelledWidget(
            self, text="Tracking file",
            label_pad=(0, 16),
            widget=self.vadar_explorer,
        )
        self.vadar_explorer_label.grid(row=1, column=0, sticky="e")

        audio_file_types = (("Audio file", "*.wav"),)
        self.audio_explorer = PathExplorerFrame(
            self, placeholder="",
            file_types=audio_file_types,
            progress=self.progress,
            on_edit_callback=partial(self.progress.info, ""),
            on_finish_callback=partial(self.progress.warn, "Audio files are only supported by Autodesk Maya")
        )

        self.audio_explorer.grid(row=2, column=1, columnspan=12)
        self.audio_explorer_label = LabelledWidget(
            self, text="Audio file",
            label_pad=(0, 16),
            widget=self.audio_explorer,
        )
        self.audio_explorer_label.grid(row=2, column=0, sticky="e")

        out_file_types = (("fbx file", "*.fbx"),)
        self.out_explorer = PathExplorerFrame(
            self, placeholder="",
            file_types=out_file_types,
            mode="save"
        )
        self.out_explorer.grid(row=3, column=1, columnspan=12)
        self.out_explorer_label = LabelledWidget(
            self, text="Output file",
            label_pad=(0, 16),
            widget=self.out_explorer,
        )
        self.out_explorer_label.grid(row=3, column=0, sticky="e")
        # HERE VIDEO
        video_file_types = (
            ("Video file", "*.webm"), ("Video file", "*.mpg"), ("Video file", "*.mpeg"), ("Video file", "*.ogg"),
            ("Video file", "*.mp4"), ("Video file", "*.m4p"), ("Video file", "*.m4v"), ("Video file", "*.avi"), 
            ("Video file", "*.wmv"), ("Video file", "*.mov"), ("Video file", "*.flv"), ("Video file", "*.avchd"))
        self.video_explorer = PathExplorerFrame(self, placeholder="",
                                                file_types=video_file_types,
                                                progress=self.progress,

                                                )

        self.video_explorer.grid(row=6, column=1, columnspan=12)
        self.video_explorer_label = LabelledWidget(
            self, text="Video file",
            label_pad=(0, 16),
            widget=self.video_explorer,
        )
        self.video_explorer_label.grid(row=6, column=0, sticky="e")
        self.mask_frame = MaskFrame(self)
        self.mask_frame.grid(row=4, column=2, columnspan=4, sticky="n", pady=(30, 32))

        self.scene_frame = SceneFrame(self)
        self.scene_frame.grid(row=4, column=6, columnspan=6, sticky="n", pady=(30, 16))

        self.clip_frame = ClipFrame(self)
        self.clip_frame.grid(row=4, column=0, columnspan=2, sticky="n", pady=(30, 16))

        self.copyright = CopyrightFrame(self)
        self.copyright.grid(row=13, column=0, columnspan=12)

        ### create video checkbox ###
        self.create_video_var = tk.BooleanVar()
        self.create_video_var.set(True)
        self.on_check_video = tk.PhotoImage(width=7, height=7)
        self.on_check_video.put((COLOR_TEXT), to=(0, 0, 6, 6))
        self.on_uncheck_video = tk.PhotoImage(width=7, height=7)
        self.on_uncheck_video.put((), to=(0, 0, 6, 6))
        self.create_video = tk.Checkbutton(
            self, image=self.on_uncheck_video,
            selectimage=self.on_check_video,
            variable=self.create_video_var
        )
        self.create_video.configure(**checkbox)

        self.create_video.grid(row=7, column=1)
        self.create_video_frame = LabelledWidget(
            self, text="Extract frames zip",
            label_pad=(0, 16),
            widget=self.create_video,
        )
        self.create_video_frame.grid(row=7, column=0, sticky="e")
        ####

        ### create audio checkbox ###
        self.create_audio_var = tk.BooleanVar()
        self.create_audio_var.set(True)
        self.on_check_audio = tk.PhotoImage(width=7, height=7)
        self.on_check_audio.put((COLOR_TEXT), to=(0, 0, 6, 6))
        self.on_uncheck_audio = tk.PhotoImage(width=7, height=7)
        self.on_uncheck_audio.put((), to=(0, 0, 6, 6))
        self.create_audio = tk.Checkbutton(
            self, image=self.on_uncheck_audio,
            selectimage=self.on_check_audio,
            variable=self.create_audio_var
        )
        self.create_audio.configure(**checkbox)

        self.create_audio.grid(row=8, column=1)
        self.create_audio_frame = LabelledWidget(
            self, text="Extract audio file",
            label_pad=(0, 16),
            widget=self.create_audio,
        )
        self.create_audio_frame.grid(row=8, column=0, sticky="e")
        ####

        self.unreal_popup = UnrealScaleWindow(self.master)
        self.unreal_popup.cleanup()
        
        # webbrowser.open(url=help_url)
        # self.open_unreal_scale_window()


    def launch_documentation(self):
        webbrowser.open(url=DOCUMENTATION_URL)

    def open_unreal_scale_window(self):
        self.unreal_popup = UnrealScaleWindow(self.master)
        self.master.wait_window(self.unreal_popup.top)
        # top = tk.Toplevel(self.master)
        # top.title = "Unreal Engine scale"


    def video_to_frame(self):
        create_frames = self.create_video_var.get()
        create_audio = self.create_audio_var.get()

        if self.video_explorer.entry.get_text():
            video_filename = self.video_explorer.get_filename().strip()
            # if webm then convert to mp4
            if "webm" in  video_filename:
                self.progress.show()
                self.progress.set(50)
                video_filename = webm_to_mp4(video_filename)
                self.progress.hide()

            video_clip = VideoFileClip(filename=video_filename)
            # make a folder by the name of the video file
            filepath, _ = os.path.splitext(video_filename)
            video_filename = filepath.split('/')[-1]
            print()
            
            if create_frames:
                self.progress.show()
                self.progress.set(0)

                try:
                    saving_frames_per_second = int(float(self.scene_frame.fps.get()))
                except:
                    saving_frames_per_second = round(video_clip.fps)
                # if SAVING_FRAMES_PER_SECOND is set to 0, step is 1/fps, else 1/SAVING_FRAMES_PER_SECOND
                step = (1 / video_clip.fps) if saving_frames_per_second == 0 else (1 / saving_frames_per_second)


                filepath += "_frames"
                if not os.path.isdir(filepath):
                    os.mkdir(filepath)

                i = 0

                frames_length = int(video_clip.duration * saving_frames_per_second)
                filename_width = len(str(frames_length))
                for current_duration in np.arange(0, video_clip.duration, step):
                    self.progress.set((i + 1) * 100 / video_clip.fps)

                    fileframe_path = os.path.join(filepath, f"{str(i).zfill(filename_width)}.jpg")
                    i += 1
                    video_clip.save_frame(fileframe_path, current_duration)
                self.progress.hide()

                shutil.make_archive(filepath , 'zip', filepath)
                shutil.rmtree(filepath)
                self.progress.info("File '%s' created." % filepath)

            if create_audio:
                audio_filename = filepath+"_audio.wav"
                video_clip.audio.write_audiofile(audio_filename)
                self.audio_explorer.entry.set_text(audio_filename)

    def get_app_state(self):
        vadar_path = self.vadar_explorer.get_filename().strip()
        audio_path = self.audio_explorer.get_filename().strip()
        video_path = self.video_explorer.get_filename().strip()  
        out_path = self.out_explorer.get_filename().strip()
        state = dict(
            vadar_path=vadar_path,
            audio_path=audio_path,
            out_path=out_path,
            video_path=video_path,
        )
        state.update(**self.mask_frame.get_state())
        state.update(**self.scene_frame.get_state())
        state.update(**self.clip_frame.get_state())

        return state

    def convert(self):
        app_state = self.get_app_state()
        vadar_path = app_state["vadar_path"]
        print(app_state)
        vadar_data = self.read_vadar(vadar_path, start=app_state.get("start_frame"), end=app_state.get("end_frame"))
        if vadar_data and vadar_data.get("Meta"):
            audio_path = app_state["audio_path"]
            is_audio_valid = self.verify_audio(audio_path)
            if is_audio_valid:
                out_path = self.get_out_path(app_state)
                self.generate_scene(vadar_data, **app_state)
                self.export_scene(out_path)
                filename = os.path.basename(out_path)
                self.progress.info("File '%s' created." % filename)

        else:
            self.progress.error("Invalid vadar file!")

    def verify_audio(self, path):
        if not path:
            return True
        if not os.path.exists(path):
            self.progress.error("Audio file not found!")
            return False
        if not os.path.splitext(path)[-1] == ".wav":
            self.progress.error("Invalid audio file, only 'wav' format supported!")
            return False
        return True

    def verify_vadar(self):
        self.convert_button.disable()
        path = self.vadar_explorer.get_filename().strip()
        if not path:
            self.progress.info("")
            return True
        elif not os.path.exists(path):
            self.progress.error("Vadar file not found!")
            return False
        else:
            vadar_data = self.read_vadar(path, inspect=True)
            if vadar_data and vadar_data.get("Meta") and vadar_data["Meta"]["Header"] in self.valid_headers:
                fps = vadar_data.get("Meta").get("UnitsPerSecond")
                if fps and fps != "undefined":
                    self.scene_frame.fps.set(fps)
                self.progress.info("")
                self.convert_button.enable()
                # set the max frame count on the end frame input
                self.clip_frame.end_frame.set(int(vadar_data['Meta'].get('FrameCount', 99999)))
                self.clip_frame.start_frame.set(int(vadar_data['Meta'].get('StartFrame', 1)))
            else:
                self.progress.error("Invalid vadar file!")
        return True

    def get_out_path(self, app_state):
        out_path = app_state["out_path"]
        vadar_path = app_state["vadar_path"]
        out_path = out_path if out_path else os.path.splitext(vadar_path)[0]
        if not out_path.lower().endswith(".fbx"):
            out_path = out_path + ".fbx"
        try:
            os.makedirs(os.path.dirname(out_path))
        except Exception:
            pass
        return out_path

    def read_vadar(self, path, inspect=False, start=None, end=None):
        print(start, end)
        data = {}
        if os.path.exists(path) and os.path.isfile(path):
            data = self.parser.parse(path, inspect, start=start, end=end)
            file_name = str(os.path.basename(path).split(".")[0])
            try:
                data["Meta"]["file_name"] = file_name
            except KeyError:
                pass
        else:
            if path:
                self.progress.error("Vadar file not found!")
            else:
                self.progress.info("")
        return data

    def generate_unreal_csv(self, **opts):
        self.progress.show()
        self.progress.set(0)
        app_state = self.get_app_state()
        vadar_path = app_state["vadar_path"]
        data = self.read_vadar(vadar_path, start=app_state.get("start_frame"), end=app_state.get("end_frame"))

        unreal_scale = 5
        time_code = data['Meta'].get('TimeCode')
        fps = data['Meta'].get('UnitsPerSecond', 30)
        frame_count = data['Meta'].get('FrameCount', 0)

        mapper = UnrealMapper()
        reference_frame = data.get("Meta", {}).get("ReferenceFrameNo", 1)
 
        # Loop through each node (marker)
        for  i,(unreal_node_id, marker) in enumerate(mapper.markers.items()):
            self.progress.set(int((i+1)/len(mapper.markers))*100)
            point_1_data = data.get(marker.points[0])
            point_2_data = data.get(marker.points[1])

            detailed_scale = self.unreal_popup.get_state(marker.name)
            detailed_scale = float(detailed_scale) if detailed_scale else unreal_scale

            # If we have data for both markers
            if point_1_data and point_2_data:
                calculated_point_percentages = {}

                # Calculate the reference frame X and Y
                ref_x1 = point_1_data['X pixels'][reference_frame]
                ref_x2 = point_2_data['X pixels'][reference_frame]
                ref_y1 = point_1_data['Y pixels'][reference_frame]
                ref_y2 = point_2_data['Y pixels'][reference_frame]

                ref_point_x_square = (ref_x2 - ref_x1)**2
                ref_point_y_square = (ref_y2 - ref_y1)**2
                reference_point_distance = math.sqrt(ref_point_x_square + ref_point_y_square)

                ref_theta = math.atan( (ref_y2 - ref_y1)/ (ref_x2 - ref_x1) )
                ref_x = reference_point_distance * math.cos(ref_theta)
                ref_y = reference_point_distance * math.sin(ref_theta)

                # Loop through each point
                for  i, frame in enumerate(point_1_data['Frame']):
                    try:
                        # Calculate each frame's X and Y
                        current_point_x1 = point_1_data['X pixels'][i]
                        current_point_x2 = point_2_data['X pixels'][i]
                        current_point_y1 = point_1_data['Y pixels'][i]
                        current_point_y2 = point_2_data['Y pixels'][i]

                        current_point_point_x_square = (current_point_x2 - current_point_x1)**2
                        current_point_point_y_square = (current_point_y2 - current_point_y1)**2
                        current_point_distance = math.sqrt(current_point_point_x_square + current_point_point_y_square)

                        current_point_theta = math.atan( (current_point_y2 - current_point_y1)/ (current_point_x2 - current_point_x1) )
                        current_point_x = current_point_distance * math.cos(current_point_theta)
                        current_point_y = current_point_distance * math.sin(current_point_theta)

                        # Calculate the percentage difference between the reference point and the current frame X and Y
                        if marker.component.upper() == 'X':
                            pct =  (1 - abs(current_point_x / ref_x ) ) if marker.inverted_percentage else ((abs(current_point_x / ref_x ) ) - 1)
                        elif marker.component.upper() == 'Y':
                            pct =  (1 - abs(current_point_y / ref_y ) ) if marker.inverted_percentage else ((abs(current_point_y / ref_y ) ) - 1)
                    except Exception as e:
                        print(unreal_node_id, frame, e)
                        pct = 0
                        
                    scaled_pct = pct*detailed_scale
                    # pct should be between 0 and 1 
                    if scaled_pct > 1:
                        calculated_point_percentages[frame] = 1
                    elif scaled_pct > 0:
                        calculated_point_percentages[frame] = scaled_pct
                    else:
                        calculated_point_percentages[frame] = 0
                        
            elif point_1_data:
                is_rotation_frame = 'Rot' in marker.component
                reference_point = point_1_data[f'{marker.component}{"" if "Rot" in marker.component else " pixels"}'][reference_frame]
                for  i, frame in enumerate(point_1_data['Frame']):
                    calculated_point = point_1_data[f'{marker.component}{"" if "Rot" in marker.component else " pixels"}'][i]
                    if is_rotation_frame:
                        pct = math.degrees(calculated_point)
                    else:
                        pct = (reference_point / calculated_point ) -1 
                    calculated_point_percentages[frame] = pct 
            else:
                calculated_point_percentages = {frame+1: 0 for frame in range(data.get("Meta", {}).get('FrameCount'))}
            marker.percentages = calculated_point_percentages
            
        df = pd.DataFrame({point: marker.percentages for point, marker in mapper.markers.items()})
        time_codes = []
        for frame in range(int(frame_count)):
            time_codes.append(time_code)
            time_code = add_frame_to_timecode(time_code, fps) 
        df.insert(0,'Timecode',  time_codes) 
        df.insert(1,'BlendshapeCount',  [61 for i in range(len(time_codes))]) 
        full_output_path = '/'.join(vadar_path.split('/')[:-1]) 
        df.to_excel(full_output_path+ '/Metahuman.xlsx', index=None)
        df.to_csv(full_output_path+ '/Metahuman.csv', index=None)
        self.progress.hide()
        self.progress.info(f"Exported file to {full_output_path+ '/Metahuman.csv'}")
        print(full_output_path)



    def generate_scene(self, data, **opts):
        self.manager = fbx.FbxManager.Create()
        self.scene = fbx.FbxScene.Create(self.manager, "MocapScene")

        self.set_scene_settings(up_axis=opts.get("up_vector"))

        anim_stack = fbx.FbxAnimStack.Create(self.scene, "AnimStack")
        anim_layer = fbx.FbxAnimLayer.Create(self.scene, "AnimLayer")
        audio_layer = fbx.FbxAudioLayer.Create(self.scene, "AudioLayer")
        anim_stack.AddMember(anim_layer)
        anim_stack.AddMember(audio_layer)

        marker_prefix = opts["marker_prefix"] + "_" if opts["marker_prefix"] else ""
        base_id = marker_prefix + data["Meta"]["file_name"]
        base_node = self.create_null_node(base_id,
                                          translation=(0, 0, 0),
                                          rotation=opts.get("rotation"),
                                          scale=(4, 4, 4))

        root_node = self.scene.GetRootNode()
        root_node.AddChild(base_node)

        n_frames = data["Meta"]["FrameCount"]
        scale_data = data.get("ScaleData", {})
        scale_values = scale_data.get("Scale", [1.] * n_frames)
        scene_scale = 4  # 4 * 10

        root_scale = opts.get("root_scale", 5.)
        src_width = data["Meta"]["SourceWidth"]
        src_height = data["Meta"]["SourceHeight"]
        x_scales = [scene_scale * (src_width / src_height) / (root_scale * (s / 10)) for s in scale_values][:n_frames]
        y_scales = [scene_scale * (src_width / src_height) / (root_scale * (s / 10)) for s in scale_values][:n_frames]
        z_scales = [scene_scale * (src_width / src_height) / (root_scale * (s / 10)) for s in scale_values][:n_frames]

        # x_scales = [1 for s in scale_values][:n_frames]
        # y_scales = [1 for s in scale_values][:n_frames]
        # z_scales = [1 for s in scale_values][:n_frames]

        self.animate_property(property=base_node.LclScaling,
                              animation_data=dict(X=x_scales, Y=y_scales, Z=z_scales),
                              fps=opts.get("fps"))

        if opts.get("apply_position"):
            position_data = data.get("MaskPositionData", {})
            x_px = position_data.get("X pixels", [])[:n_frames]
            y_px = position_data.get("Y pixels", [])[:n_frames]
            x = [scene_scale * (p - (src_width / 2)) * (src_width / src_height) / (root_scale * (scale_values[i_] / 10))
                 for i_, p in enumerate(x_px)]
            y = [scene_scale * (p - (src_height)) * (src_width / src_height) / (root_scale * (scale_values[i_] / 10))
                 for i_, p in enumerate(y_px)]
            self.animate_property(property=base_node.LclTranslation,
                                  animation_data=dict(X=x, Y=y),
                                  fps=opts.get("fps"))

        fixed_pos = False
        for i, (node_id, node_data) in enumerate(data.items()):
            # print(len(node_data['Frame']), len(node_data['X pixels']), len(node_data['Y pixels']))
            self.progress.show()
            self.progress.set((i + 1) * 100 / len(data))
            if node_id in ["ScaleData", "MaskPositionData", "Meta"]:
                continue
            node = self.create_null_node(marker_prefix + node_id)

            if node_id == "RotationData":
                x_rad = node_data.get("X Rot", [0.] * n_frames)[:n_frames]
                y_rad = node_data.get("Y Rot", [0.] * n_frames)[:n_frames]
                z_rad = node_data.get("Z Rot", [0.] * n_frames)[:n_frames]
                x_degree = [r * 180 / math.pi for r in x_rad]
                y_degree = [r * 180 / math.pi for r in y_rad]
                z_degree = [r * 180 / math.pi for r in z_rad]
                self.animate_property(property=node.LclRotation,
                                      animation_data=dict(X=x_degree, Y=y_degree, Z=z_degree),
                                      fps=opts.get("fps"))

            else:  # TranslationData
                x_px = node_data.get("X pixels", [])[:n_frames]
                y_px = node_data.get("Y pixels", [])[:n_frames]
                x = [scene_scale * (p - (src_width / 2)) * (src_width / src_height) / (root_scale) for i_, p in
                     enumerate(x_px)]
                y = [scene_scale * (p - (src_height)) * (src_width / src_height) / (root_scale) for i_, p in
                     enumerate(y_px)]
                marker_scale = 4 * opts.get("marker_scale", 3.)
                node.LclScaling.Set(
                    fbx.FbxDouble3(
                        marker_scale / (root_scale),
                        marker_scale / (root_scale),
                        marker_scale / (root_scale)
                    )
                )
                node.LclRotation.Set(fbx.FbxDouble3(*opts.get("local_rotation")))
                self.animate_property(property=node.LclTranslation,
                                      animation_data=dict(X=x, Y=y),
                                      fps=opts.get("fps"))

            base_node.AddChild(node)

        if opts.get("audio_path"):
            audio = fbx.FbxAudio.Create(self.scene, "Audio")
            audio.SetFileName(opts.get("audio_path"))
            fbx_time = fbx.FbxTime(0)
            audio.SetClipIn(fbx_time)
            scene_duration = 1000 * n_frames / opts.get("fps")
            fbx_time.SetMilliSeconds(scene_duration)
            audio.SetClipOut(fbx_time)
            audio.Duration.Set(fbx_time)
            audio.Channels.Set(1)
            audio_layer.AddMember(audio)
        self.progress.hide()

    def export_scene(self, file_path):
        exporter = fbx.FbxExporter.Create(self.manager, "fbx_exporter")
        status = exporter.Initialize(file_path)
        if not status:
            raise IOError("Unable to export file: '{}'".format(file_path))
        exporter.Export(self.scene)
        exporter.Destroy()
        return status

    @staticmethod
    def add_keyframe(anim_curve, frame_id, key, fps=None):
        time_fbx = fbx.FbxTime()
        e_mode = fbx.FbxTime.eDefaultMode
        fps = fbx.FbxTime.GetFrameRate(e_mode) if fps is None else fps
        time_fbx.SetSecondDouble(float(frame_id) / fps)
        key_fbx = fbx.FbxAnimCurveKey()
        key_fbx.Set(time_fbx, key)
        anim_curve.KeyAdd(time_fbx, key_fbx)

    def keyframe_property(self, property, anim_layer, axes_data, fps=None):
        for axis, keyframes_data in axes_data.items():
            # Create axis animation curve
            anim_curve = property.GetCurve(anim_layer, axis, True)
            # Keyframe axis transformations
            anim_curve.KeyModifyBegin()
            for frame_id, frame_value in enumerate(keyframes_data):
                self.add_keyframe(anim_curve=anim_curve,
                                  key=frame_value,
                                  frame_id=frame_id,
                                  fps=fps)
            anim_curve.KeyModifyEnd()

    @staticmethod
    def set_node_transform(node, translation=(0., 0., 0.),
                           rotation=(0., 0., 0.), scale=(1., 1., 1.)):
        node.LclTranslation.Set(fbx.FbxDouble3(*translation))
        node.LclRotation.Set(fbx.FbxDouble3(*rotation))
        node.LclScaling.Set(fbx.FbxDouble3(*scale))

    def create_null_node(self, name="", translation=(0., 0., 0.),
                         rotation=(0., 0., 0.), scale=(1., 1., 1.)):
        node = fbx.FbxNode.Create(self.scene, name)
        null = fbx.FbxNull.Create(self.scene, name + "Null")
        node.SetNodeAttribute(null)
        self.set_node_transform(node, translation, rotation, scale)
        return node

    def set_axis_system(self, up_axis="Y"):
        if up_axis == "Y":
            axis_system = fbx.FbxAxisSystem.MayaYUp
            self.scene.GetGlobalSettings().SetAxisSystem(axis_system)
        elif up_axis == "Z":
            axis_system = fbx.FbxAxisSystem.MayaZUp
            self.scene.GetGlobalSettings().SetAxisSystem(axis_system)
        else:
            pass

    def set_scene_settings(self, up_axis):
        self.set_axis_system(up_axis)

    def animate_property(self, property, animation_data={}, fps=None):
        anim_stack = self.scene.GetCurrentAnimationStack()
        anim_layer = anim_stack.GetSrcObject(0)
        self.keyframe_property(property=property, anim_layer=anim_layer,
                               axes_data=animation_data, fps=fps)


def webm_to_mp4(input_file_path):
    # try:
    output_file_path, _ = os.path.splitext(input_file_path) 
    output_file_path += ".mp4"
    if os.path.exists(output_file_path):
        return output_file_path
    stream = ffmpeg.input(input_file_path)
    stream = ffmpeg.output(stream, output_file_path)
    ffmpeg.run(stream)
    # except Exception as e:
    #     print(e)

    return output_file_path

def timecode_to_frames(timecode, fps):
    # Convert timecode to frames
    hours, minutes, seconds, frames = map(int, timecode.split(':'))
    total_frames = frames + (seconds + minutes * 60 + hours * 3600) * fps
    return total_frames

def frames_to_timecode(frames, fps):
    # Convert frames to timecode
    total_seconds = frames / fps
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    frames = frames % fps
    return "{:02d}:{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds), int(frames))

def add_frame_to_timecode(timecode, fps):
    current_frames = timecode_to_frames(timecode, fps)
    new_frames = current_frames + 1
    new_timecode = frames_to_timecode(new_frames, fps)
    return new_timecode