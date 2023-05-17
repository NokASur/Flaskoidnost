level = []
for i in range(0, 8):
    level.append(1)
for i in range(8, 15):
    level.append(2)
for i in range(15, 20):
    level.append(3)
for i in range(20, 24):
    level.append(4)
for i in range(24, max(30, 100)):
    level.append(5)


def get_level(points):
    return level[points]
