from dataclasses import dataclass


def author() -> str:
    """
    Возвращает имя автора ответа и номер группы в формате: {Имя} {Фамилия}, {класс}-{номер}
    Examples:
        >>> author()
        'Вася Пупкин, 9-1'
    Returns:
        str: имя автора ответа и номер группы
    """

    return "Борисов Денис, 10-3"


@dataclass
class Vector:
    """
    Класс вектора.
    Должен иметь атрибуты `x` и `y`, задаваемые при инициализации (в конструкторе)
    Должен уметь:
        - складывать два вектора. если второй аргумент сложения не вектор - вызывать TypeError
        - вычитать вектор из вектора. если второй аргумент вычитания не вектор - вызывать TypeError
        - умножать вектор на число. если второй аргумент сложения не число - вызывать TypeError
        - находить свою длину (абсолютное значение (abs)). abs(Vector(3, 4)) -> 5.0
        - преобразовываться в кортеж и список. tuple(Vector(0, 0)) -> (0, 0)
    """

    x: float
    y: float

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            raise TypeError

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        else:
            raise TypeError

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** .5

    def __mul__number(self, other):
        return Vector(self.x * other, self.y * other)

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            return self.__mul__number(other)
        else:
            raise TypeError

    def __iter__(self):
        result = []
        result.append(self.x)
        result.append(self.y)
        return iter(result)

    def distance_to(self, other: "Vector") -> float:
        """
        Расстояние от этой точки до данной. (Точки обозначены радиус-векторами)
        Args:
            other (Vector): другая (данная) точка
        Returns:
            float: расстояние до точки
        """

        return (((self.x - other.x) ** 2) + (self.y - other.y) ** 2) ** .5


class NamedPos:
    """
    Класс "позиция с именем"
    Должна иметь `name` - имя и `pos` - позицию в двумерном пространстве, задаваемые при инициализации
    """

    name: str
    pos: Vector

    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

    def distance_to(self, other: "NamedPos") -> float:
        """
        Находит расстояние до другой именованной позиции
        Args:
            other (NamedPos): другая именованная позиция
        Returns:
            float: расстояние до другой именованной позиции
        """

        return self.pos.distance_to(other.pos)


class Participant:
    """
    Класс "участник"
    Должна иметь `name` - имя,  `pos` - позицию в двумерном пространстве, `speed` - скорость (float)
    задаваемые при инициализации
    """

    name: str
    pos: Vector
    speed: float

    def __init__(self, name, pos, speed):
        self.name = name
        self.pos = pos
        self.speed = speed

    def time_to(self, other: "NamedPos"):
        """
        Время, которое необходимо участнику чтобы добраться по прямой до определенной точки
        Args:
            other (NamedPos): - определенная точка в сторону которой движется участник
        Returns:
            float: необходимое время
        """

        return self.pos.distance_to(other.pos) / self.speed


def race(*participants: Participant, finish: NamedPos) -> str:
    """
    В гонке участвует несколько участников (не меньше одного), все они движутся по прямой до финиша.
    Находит имя участника, который доберется первым до финиша или имя первого переданного участника (participants[0])
    Args:
        *participants (Participant): набор участников
        finish (NamedPos): точка финиша
    Returns:
        str: имя участника, который доберется первым или имя первого переданного участника (participants[0])
    """

