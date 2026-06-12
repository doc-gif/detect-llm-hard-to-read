colors = list(map(int, input().split()))
faces = {
    "top": colors[:4],
    "front": colors[4:8],
    "bottom": colors[8:12],
    "left": colors[12:16],
    "right": colors[16:20],
    "back": [colors[21], colors[20], colors[23], colors[22]],
}
status = {}
for face, cols in faces.items():
    if max(cols) == min(cols):
        status[face] = "ok"
    elif cols[0] == cols[1] and cols[2] == cols[3]:
        status[face] = "h"
    elif cols[0] == cols[2] and cols[1] == cols[3]:
        status[face] = "v"
    else:
        status[face] = "bad"
if "bad" in status.values():
    print("NO")
else:
    if (
        status["top"] == status["bottom"] == "ok"
        and status["front"]
        == status["left"]
        == status["right"]
        == status["back"]
        == "h"
    ):
        cond1 = (
            faces["front"][0] == faces["left"][3]
            and faces["left"][0] == faces["back"][3]
            and faces["back"][0] == faces["right"][3]
            and faces["right"][0] == faces["front"][3]
        )
        cond2 = (
            faces["front"][0] == faces["right"][3]
            and faces["right"][0] == faces["back"][3]
            and faces["back"][0] == faces["left"][3]
            and faces["left"][0] == faces["front"][3]
        )
        print("YES" if cond1 or cond2 else "NO")
    elif (
        status["left"] == status["right"] == "ok"
        and status["front"]
        == status["top"]
        == status["bottom"]
        == status["back"]
        == "v"
    ):
        cond1 = (
            faces["front"][0] == faces["top"][3]
            and faces["top"][0] == faces["back"][3]
            and faces["back"][0] == faces["bottom"][3]
            and faces["bottom"][0] == faces["front"][3]
        )
        cond2 = (
            faces["front"][0] == faces["bottom"][3]
            and faces["bottom"][0] == faces["back"][3]
            and faces["back"][0] == faces["top"][3]
            and faces["top"][0] == faces["front"][3]
        )
        print("YES" if cond1 or cond2 else "NO")
    elif (
        status["front"] == status["back"] == "ok"
        and status["top"]
        == status["left"]
        == status["right"]
        == status["bottom"]
        == "v"
    ):
        cond1 = (
            faces["top"][0] == faces["left"][3]
            and faces["left"][0] == faces["bottom"][3]
            and faces["bottom"][0] == faces["right"][3]
            and faces["right"][0] == faces["top"][3]
        )
        cond2 = (
            faces["top"][0] == faces["right"][3]
            and faces["right"][0] == faces["bottom"][3]
            and faces["bottom"][0] == faces["left"][3]
            and faces["left"][0] == faces["top"][3]
        )
        print("YES" if cond1 or cond2 else "NO")
    else:
        print("NO")
