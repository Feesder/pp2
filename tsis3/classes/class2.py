class Shape:
    def __init__(self):
        pass

    def calculateArea(self):
        return 0

class Square(Shape):
    def __init__(self, length: int):
        super().__init__()
        self.length = length

    def calculateArea(self) -> int:
        return self.length ** 2


if __name__ == '__main__':
    square = Square(3)
    print(square.calculateArea())