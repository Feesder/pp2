from class2 import Shape

class Rectangle(Shape):
    def __init__(self, length: int, width: int):
        super().__init__()
        self.length = length
        self.width = width

    def calculateArea(self) -> int:
        return self.length * self.width


if __name__ == '__main__':
    rectangle = Rectangle(3, 4)
    print(rectangle.calculateArea())
