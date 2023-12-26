import enum
from inspect import isframe
import re
import copy

class RigVadarDataParser(object):
    def __init__(self):
        super(RigVadarDataParser, self).__init__()
        self.path = None
        self.data = None
        self.df_regexes = ["Rig Vadar Facial Performance Analysis", "_Track Point", "Rotation Data",
                           "Scale Data", "Mask Position Data",
                           "End of Keyframe Data"]

    def inject_static_frames(self, next_line):
        splitted_line = split_line(next_line)
        number = int(splitted_line[0])

        static_frames = []
        for i in range(1,number):
            l = [ str(i), splitted_line[1] ]

            if len(splitted_line) > 2:
                l.append(splitted_line[2])
            
            if len(splitted_line) > 3:
                l.append(splitted_line[3])

            static_frames.append(",".join(l))

        return static_frames

    def csv_to_txt(self, inspect, start, end):
        with open(self.path) as f:
            lines = []
            lines_read = f.readlines()
            static_frames_length = 0

            i = 0
            # loop until the file is over
            while True:
                try:
                    line = lines_read[i]
                except:
                    break

                # fix the extra points that have typos
                if "TrackPoint" in line:
                    lines_read[i] = line.replace('TrackPoint',"Track Point")
                
                # check for static frames
                if "Frame,X Pixels,Y Pixels" in line or "Frame,Scale" in line or "Frame,X Rot,Y Rot,Z Rot" in line or "Frame,X pixels,X pixels" in line or "Frame," in line:
                    static_frames = self.inject_static_frames(lines_read[i+1])
                    static_frames_length = len(static_frames)
                    for x in static_frames[::-1]:
                        lines_read.insert(i+1,x)

                # check if this frame number is the start frame number provided by the user
                if not inspect:
                    if is_frame_line(line):
                        start_frame_line = get_frame_data(lines=lines_read[i+1:], index=start)
                        end_frame_line = get_frame_data(lines=lines_read[i+1:], index=end)
                        # print("start", start_frame_line)
                        # print("end", end_frame_line)
                        if start_frame_line:
                            lines_read_update = replace_frames(lines=lines_read[i+1:], new_line=start_frame_line, to_index=start)
                            lines_read[i+1:] = lines_read_update
                        if end_frame_line:
                            lines_read_update = replace_frames(lines=lines_read[i+1:], new_line=end_frame_line, from_index=end)
                            lines_read[i+1:] = lines_read_update
                i += 1

                    
            for i, line in enumerate(lines_read):
                if i in [0,1,2]:
                    lines.append(line[:-4] + '\n')
                    if i == 2:
                        lines.append('\n')
                elif i in list(range(3,8)):
                    lines.append('      ' + line[:-1].replace(',','\t')+ '\n')
                elif i == 8:
                    lines.append( line[:-1].replace(',','\t')+ '\n')
                elif i == 9:
                    lines.append('  \t'+ line[:-2].replace(',','\t')+ '\n')
                    lines.append('\n')
                elif any([True for x in ["_Track Point",'Data'] if x in line]):
                    lines.append( line[:-4].replace(',','\t')+ '\n')
                else:
                    lines.append('  ' +line.replace(',','\t').strip()+ '\n')


            lines.append('End of Keyframe Data')
            if inspect:
                lines = lines[:50]          

            for i,line in enumerate(lines):
                if "Frame Count" in line:
                    splitted_line: list = line.split('\t')
                    index_frame_count_number = find_index_of_substring(splitted_line, "Frame") + 1
                    splitted_line[index_frame_count_number] = str( int(splitted_line[index_frame_count_number]) + static_frames_length )
                    lines[i] = '\t'.join(splitted_line)
                    break
        
        # with open("test.txt", 'w+') as f:
        #     f.writelines(lines)
        return lines, static_frames_length+1

    def parse(self, path, inspect=False, start=None, end=None):
        self.path = path
        # if the file extension is a csv file then convert it to a txt readable file
        if '.csv' in path:
            lines, start_frame = self.csv_to_txt(inspect, start, end)
        else:
            lines, start_frame = self.load_file(inspect, start, end)

        lines = [line.replace('Pixels', "pixels") for line in lines]

        # print(lines)
        dfs = self.extract_data_frames(lines)
        data = self.data_frames_to_dict(dfs)
        self.data = data
        self.data['Meta']['StartFrame'] = start_frame
        
        return self.data


    def load_file(self, inspect=False, start=None, end=None):
        with open(self.path) as f:
            lines = f.readlines()
            if inspect:
                lines = lines[:50]

        static_frames_length = 0

        # check for static frames
        for i,line in enumerate(lines):
            if is_frame_line_txt(line):
                static_frames = self.inject_static_frames(lines[i+1])
                static_frames_length = len(static_frames)
                for x in static_frames[::-1]:
                    lines.insert(i+1,x)
                    
        lines = [line.replace('TrackPoint','Track Point') for line in lines]

        # check if this frame number is the start frame number provided by the user
        if not inspect:
            for i in range(len(lines)):
                line = lines[i]
                if is_frame_line_txt(line):
                    start_frame_line = get_frame_data(lines=lines[i+1:], index=start)
                    end_frame_line = get_frame_data(lines=lines[i+1:], index=end)
                    if start_frame_line:
                        lines_read_update = replace_frames(lines=lines[i+1:], new_line=start_frame_line, to_index=start)
                        lines[i+1:] = lines_read_update
                    if end_frame_line:
                        lines_read_update = replace_frames(lines=lines[i+1:], new_line=end_frame_line, from_index=end)
                        lines[i+1:] = lines_read_update
        with open("test.txt", 'w+') as f:
            f.writelines(lines)

        for i,line in enumerate(lines):
                if "Frame Count" in line:
                    splitted_line = line.split('\t')
                    splitted_line[2] = str( int(splitted_line[2]) + static_frames_length )
                    lines[i] = '\t'.join(splitted_line)
                    break
        return lines, static_frames_length+1
            

    def extract_data_frames(self, lines):
        frame_split_idxs = [i for i, line in enumerate(lines) if
                            any(df_regex in line for df_regex
                                in self.df_regexes)]

        sections = [lines[frame_split_idxs[i]: frame_split_idxs[i + 1]]
                    for i, idx in enumerate(frame_split_idxs)
                    if i < len(frame_split_idxs) - 1]
     
        dfs = [[[item.strip(" ") for item in re.split("\n|\t|:|\r" if 'Time Code' not in line else "\n|\t|\r", line) if item]
                for line in section] for section in sections]

        return dfs

    def data_frames_to_dict(self, dfs):
        dfs_dict = dict()
        for df in dfs:
            # Extract dataframe id
            id_raw = df[0][0]

            id_words_raw = id_raw.split()
            id_split_idxs = [i for i, word in enumerate(id_words_raw)
                             if any([s for s in ["Point", "#"] if s in word])]
            if not id_split_idxs:
                id_split_idxs = [-1, len(id_words_raw)]
            
            try:
                id = "".join(id_words_raw[id_split_idxs[0] + 1: id_split_idxs[1]])
            except:
                id = "".join(id_words_raw[id_words_raw.index("Point")+1:]).replace(' ','')

            # Extract dataframe data
            data = dict()
            # print(df)

            if any([not item for item in df]):
                # meta data
                data["Header"] = id
                id = "Meta"
                meta = [[s.replace(";", "").replace(" ", "") for s in d if s]
                        for d in df[3:] if d]

                for key, val in meta:
                    try:
                        if("TimeCode" in key):
                            data[key.replace(':', '')] = val
                        else:
                            data[key] = eval(val)
                    except NameError:
                        data[key] = val
            else:
                for i, key in enumerate(df[1]):
                    data[key] = [eval(v[i]) for v in df[2:]]
            dfs_dict[id] = data
            

        return dfs_dict



def is_frame_line(line):
    return "Frame,X Pixels,Y Pixels" in line or "Frame,Scale" in line or "Frame,X Rot,Y Rot,Z Rot" in line or "Frame,X pixels,X pixels" in line or "Frame," in line

def is_frame_line_txt(line):
    line = str(line).lower()
    return ("frame" in line and "x pixels" in line and "y pixels" in line) or ("frame" in line and "scale" in line) or ("frame" in line and "x rot" in line and "y rot" in line and "z rot" in line) or ("frame" in line and "x pixels" in line and "x pixels" in line) or ("frame," in line)


def get_frame_data(lines, index):
    for line in lines:
        if is_frame_line(line) or is_frame_line_txt(line) or "Track Point" in line or "Data" in line:
            return False
        frame_number = int(split_line(line)[0]) 
        if frame_number == index:
            return line
    return False

def replace_frames(lines, new_line, to_index=None, from_index=None):
    splitted_new_line = split_line(new_line)
    # print(splitted_new_line)
    for i, line in enumerate(lines):
        if is_frame_line(line) or is_frame_line_txt(line) or "Track Point" in line or "Data" in line:
            break
        splitted_line = split_line(line)
        frame_number = int(splitted_line[0]) 
        if to_index is not None and frame_number < to_index:
            splitted_new_line[0] = str(frame_number)
            lines[i] = ','.join(splitted_new_line)

        if from_index is not None and frame_number > from_index:
            splitted_new_line[0] = str(frame_number)
            lines[i] = ','.join(splitted_new_line)

        if "," not in new_line:
                lines[i] = '  ' +lines[i].replace(',','\t').strip()+ '\n'
    return lines


def split_line(line):
    l = copy.deepcopy(line)
    return l.split(',') if "," in l else l.strip().split('\t')
     

def find_index_of_substring(lst, substring):
    for i, element in enumerate(lst):
        if substring in element:
            return i
    return -1 

def timecode_to_frames(timecode: str, frame_rate: int) -> int:
    hours, minutes, seconds, frames = map(int, timecode.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    total_frames = total_seconds * frame_rate + frames
    return total_frames

def frames_to_timecode(total_frames: int, frame_rate: int) -> str:
    total_seconds = total_frames // frame_rate
    frames = total_frames % frame_rate
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}:{frames}"

# # Example usage
# frame_rate = 30  # example frame rate
# timecode = "00:00:11:9"
# frames_to_add = 10  # example number of frames to add

# # Convert to frames
# total_frames = timecode_to_frames(timecode, frame_rate)

# # Add frames
# total_frames += frames_to_add

# # Convert back to timecode
# new_timecode = frames_to_timecode(total_frames, frame_rate)

# print(new_timecode)
