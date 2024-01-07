from typing import Dict

class UnrealMarker:
    def __init__(self, name, points, component, weight) -> None:
        self.points = points
        self.component = component
        self.weight = weight
        self.percentages = None
        self.name = name

    def __str__(self) -> str:
        return f"{self.name}: {self.percentages}"
    
    def __repr__(self) -> str:
        return f"{self.name}: {self.percentages}"
    
class UnrealMapper:

    def __init__(self) -> None:
        self.markers: Dict[str, UnrealMarker] = {}
        self.add_marker(name="EyeBlinkLeft",point1="LeftEyeUpper1", point2="LeftEyeLower1", component="Y")
        self.add_marker(name="EyeLookDownLeft",point1="pupilpointL", point2="NoseBridge", component="Y")
        self.add_marker(name="EyeLookInLeft",point1="pupilpointL", point2="NoseBridge", component="X")
        self.add_marker(name="EyeLookOutLeft",point1="pupilpointL", point2="NoseBridge", component="X")
        self.add_marker(name="EyeLookUpLeft",point1="pupilpointL", point2="NoseBridge", component="Y")
        self.add_marker(name="EyeSquintleft",point1="LeftEyeBrow2", point2="LeftEyeUpper1", component="Y") 
        self.add_marker(name="EyeWideleft",point1="LeftEyeUpper2", point2="LeftEyeLower2", component="Y")
        self.add_marker(name="EyeBlinkRight",point1="RightEyeUpper", point2="RightEyeLower1", component="Y")
        self.add_marker(name="EyeLookDownRight",point1="pupilpointR", point2="NoseBridge", component="Y")
        self.add_marker(name="EyeLookInRight",point1="pupilpointR", point2="NoseBridge", component="X")
        self.add_marker(name="EyeLookOutRight",point1="pupilpointR", point2="NoseBridge", component="X")
        self.add_marker(name="EyeLookUpRight",point1="pupilpointR", point2="NoseBridge", component="Y")
        self.add_marker(name="EyeSquintRight",point1="RightEyeUpper", point2="RightEyebrow2", component="Y")
        self.add_marker(name="EyeWideRight",point1="RightEyeUpper", point2="RightEyeLower1", component="Y")
        self.add_marker(name="JawForward",point1="", point2="", component="Y")
        self.add_marker(name="JawRight",point1="NoseTip", point2="Chin", component="X")
        self.add_marker(name="JawLeft",point1="NoseTip", point2="Chin", component="Y")
        self.add_marker(name="JawOpen",point1="NoseTip", point2="Chin", component="Y")
        self.add_marker(name="MouthClose",point1="MouthTopInner2", point2="MouthTopInner1", component="Y")
        self.add_marker(name="MouthFunnel",point1="MouthLeft", point2="MouthRight", component="X")
        self.add_marker(name="MouthPucker",point1="MouthLet", point2="MouthRight", component="X")
        self.add_marker(name="MouthRight",point1="MouthLeft", point2="MouthRight", component="X")
        self.add_marker(name="MouthLeft",point1="MouthRight", point2="MouthLeft", component="X")
        self.add_marker(name="MouthSmileleft",point1="MouthLeft", point2="NoseTip", component="Y")
        self.add_marker(name="MouthSmileRight",point1="MouthRight", point2="NoseTip", component="Y")
        self.add_marker(name="Mouthfrownleft",point1="NoseTip", point2="MouthRight", component="Y")
        self.add_marker(name="Mouthfrownright",point1="MouthRight", point2="NoseTip", component="Y")
        self.add_marker(name="Mouthdimpleleft",point1="", point2="", component="Y")
        self.add_marker(name="Mouthdimpleright",point1="", point2="", component="Y")
        self.add_marker(name="Mouthstretchleft",point1="MouthLeft", point2="NoseTip", component="X")
        self.add_marker(name="Mouthstretchright",point1="NoseTip", point2="MouthLeft", component="X")
        self.add_marker(name="MouthrollLower",point1="NoseTip", point2="MouthBottom", component="Y")
        self.add_marker(name="MouthrollUpper",point1="NoseTip", point2="MouthTop", component="Y")
        self.add_marker(name="MouthshrugLower",point1="MouthBottom", point2="Chin", component="Y")
        self.add_marker(name="MouthshrugUpper",point1="MouthTop", point2="Chin", component="Y")
        self.add_marker(name="Mouthpressleft",point1="MouthLeftInnerLwr", point2="MouthLeftInner", component="Y")
        self.add_marker(name="Mouthpressright",point1="MouthRightInnerLwr", point2="MouthRightInner1", component="Y")
        self.add_marker(name="Mouthlowerdownleft",point1="MouthLeft", point2="Chin", component="Y")
        self.add_marker(name="Mouthlowerdownright",point1="MouthRight", point2="Chin", component="Y")
        self.add_marker(name="MouthUpperUpLeft",point1="MouthLeftTop", point2="NoseTip", component="Y")
        self.add_marker(name="MouthUpperUpright",point1="MouthRTop", point2="NoseTip", component="Y")
        self.add_marker(name="BrowDownLeft",point1="LeftEyebrowMiddle", point2="NoseBridge", component="Y")
        self.add_marker(name="BrowDownRight",point1="RightEyebrow2Middle", point2="NoseBridge", component="Y")
        self.add_marker(name="BrowInnerUp",point1="RightEyebrowInner", point2="NoseBridge", component="Y")
        self.add_marker(name="BrowOuterUpLeft",point1="LeftEyebrowOuter", point2="NoseBridge", component="Y")
        self.add_marker(name="BrowOuterUpRight",point1="RightEyebrowOuter", point2="NoseBridge", component="Y")
        self.add_marker(name="CheekPuff",point1="NoseTip", point2="", component="X")
        self.add_marker(name="CheekSquintleft",point1="", point2="", component="Y")
        self.add_marker(name="CheekSquintright",point1="", point2="", component="Y")
        self.add_marker(name="NoseSneerLeft",point1="LeftNostril", point2="NoseTip", component="Y")
        self.add_marker(name="NoseSneerRight",point1="RightNostril", point2="NoseTip", component="Y")
        self.add_marker(name="TongueOut",point1="", point2="", component="")
        self.add_marker(name="HeadYaw",point1="RotationData", point2="", component="X Rot")
        self.add_marker(name="HeadPitch",point1="RotationData", point2="", component="Y Rot")
        self.add_marker(name="HeadRoll",point1="RotationData", point2="", component="Z Rot")
        self.add_marker(name="LeftEyeYaw",point1="pupilpointL", point2="NoseBridge", component="X")
        self.add_marker(name="LeftEyePitch",point1="pupilpointL", point2="NoseBridge", component="Y")
        self.add_marker(name="LeftEyeRoll",point1="", point2="", component="Y")
        self.add_marker(name="RightEyeYaw",point1="pupilpointR", point2="NoseBridge", component="X")
        self.add_marker(name="RightEyePitch",point1="pupilpointR", point2="NoseBridge", component="Y")
        self.add_marker(name="RightEyeRoll",point1="", point2="", component="Y")


    def add_marker(self, name, point1, point2, component, weight=1):
        self.markers[name] = UnrealMarker(
            name=name,
            points= [point1, point2],
            component= component,
            weight= weight
        )

