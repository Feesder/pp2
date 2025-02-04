class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def show(self):
        print(self.x, self.y)

    def move(self, new_x: int, new_y: int):
        self.x = new_x
        self.y = new_y

    def dist(self, other_point):
        return (self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2


point1 = Point(6, 8)
point2 = Point(1, 2)

point1.show()
point2.show()

point1.move(9, 5)
point2.move(8, 4)

point1.show()
point2.show()

print(point1.dist(point2))
