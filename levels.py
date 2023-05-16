level = []
for i in range(0, 1):
    level.append(1)
for i in range(1, 2):
    level.append(2)
for i in range(2, 3):
    level.append(3)
for i in range(3, 4):
    level.append(4)
for i in range(4, 5):
    level.append(5)


def get_level(points):
    return level[points]
