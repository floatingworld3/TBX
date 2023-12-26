
class UnrealMapper:
    markers = {
        "EyeBlinkLeft" : {
            "points": ["LeftEyeUpper1", "LeftEyeLower1"],
            "component": "Y"
        },
        "EyeLookdownLeft": {
            "points": [None, "NoseBridge"],
            "component": "Y"
        },
        "EyeLookinLeft": {
            "points": [None, "NoseBridge"],
            "component": "X"
        },
        "EyeLookOutLeft":  {
            "points": [None, "NoseBridge"],
            "component": "X"
        },
        
        "EyeLookUptLeft":  {
            "points": [None, "NoseBridge"],
            "component": "Y"
        },
        "EyeSquintLeft": {
            "points": ["LeftEyebrow2", "LeftEyeUpper1"],
            "component": "Y"
        },
    }

    @staticmethod
    def add_marker(name, point1, point2, component, weight=1):
        UnrealMapper.markers[name] = {
            "points": [point1, point2],
            "component": component,
            "weight": weight
        },



UnrealMapper.add_marker(name="EyeBlinkLeft",point1="LeftEyeUpper1", point2="LeftEyeLower1", component="Y")
UnrealMapper.add_marker(name="EyeLookDownLeft",point1=None, point2="NoseBridge", component="Y")
UnrealMapper.add_marker(name="EyeLookInLeft",point1=None, point2="NoseBridge", component="X")
UnrealMapper.add_marker(name="EyeWideLeft",point1="LeftEyeUpper2", point2="LeftEyeLower2", component="Y")