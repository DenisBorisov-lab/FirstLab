import unittest
import re
import random
import operator

import tasks


AUTHOR_RE = re.compile(r'^[A-ZА-Я]\w+ [A-ZА-Я]\w+, \d{1,2}-\d$')


class TestAuthor(unittest.TestCase):
    def test_author(self):
        author = tasks.author()
        self.assertRegex(author, AUTHOR_RE, msg="Укажите данные согласно заданию и правилам языка")


class TestVector(unittest.TestCase):
    def setUp(self) -> None:
        random.seed(tasks.author())

    def test_init(self):
        x = random.random()
        y = random.random()
        vec = tasks.Vector(x, y)

        self.assertEqual(x, vec.x)
        self.assertEqual(y, vec.y)

    @staticmethod
    def prepare_vec():
        x = random.random()
        y = random.random()
        return x, y, tasks.Vector(x, y)

    def __test_vec_vec(self, operation):
        x1, y1, left = self.prepare_vec()
        x2, y2, right = self.prepare_vec()

        result = operation(left, right)

        self.assertEqual(left, tasks.Vector(x1, y1), msg="Действие не должно менять исходные данные")
        self.assertEqual(right, tasks.Vector(x2, y2), msg="Действие не должно менять исходные данные")
        self.assertEqual(result, tasks.Vector(operation(x1, x2), operation(y1, y2)))

    def __test_vec_num(self, operation):
        x1, y1, left = self.prepare_vec()
        right = random.random()

        result = operation(left, right)

        self.assertEqual(left, tasks.Vector(x1, y1), msg="Действие не должно менять исходные данные")
        self.assertEqual(result, tasks.Vector(operation(x1, right), operation(y1, right)))

    def test_add(self):
        self.__test_vec_vec(operator.add)

    def test_add_raises(self):
        def vec_num_addition():
            self.__test_vec_num(operator.add)

        self.assertRaises(TypeError, vec_num_addition)

    def test_sub_raises(self):
        def vec_num_subtraction():
            self.__test_vec_num(operator.sub)

        self.assertRaises(TypeError, vec_num_subtraction)

    def test_sub(self):
        self.__test_vec_vec(operator.sub)

    def test_mul(self):
        self.__test_vec_num(operator.mul)

    def test_mul_raises(self):
        def vec_by_vec_multiplication():
            self.__test_vec_vec(operator.mul)

        self.assertRaises(TypeError, vec_by_vec_multiplication)

    def test_abs(self):
        x, y, vec = self.prepare_vec()

        result = abs(vec)
        true_result = (x ** 2 + y ** 2) ** .5

        self.assertEqual(true_result, result)

    def test_iter(self):
        x, y, vec = self.prepare_vec()

        self.assertEqual([x, y], list(vec))
        self.assertEqual((x, y), tuple(vec))

    def test_distance_to(self):
        x1, y1, left = self.prepare_vec()
        x2, y2, right = self.prepare_vec()

        result = left.distance_to(right)
        true_result = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5

        self.assertEqual(true_result, result)


class TestNamedPos(unittest.TestCase):
    @staticmethod
    def rand_name() -> str:
        return "".join(chr(random.randint(0, 255)) for _ in range(random.randint(100, 500)))

    def test_init(self):
        name = self.rand_name()
        _, _, pos = TestVector.prepare_vec()

        obj = tasks.NamedPos(str(name), pos)

        self.assertEqual(name, obj.name)
        self.assertEqual(pos, obj.pos)

    def test_distance_to(self):
        _, _, pos1 = TestVector.prepare_vec()
        _, _, pos2 = TestVector.prepare_vec()

        left = tasks.NamedPos(self.rand_name(), pos1)
        right = tasks.NamedPos(self.rand_name(), pos2)

        result = left.distance_to(right)
        true_result = pos1.distance_to(pos2)

        self.assertEqual(true_result, result)


class TestParticipant(unittest.TestCase):
    @staticmethod
    def prepare_part():
        name = TestNamedPos.rand_name()
        _, _, pos = TestVector.prepare_vec()
        speed = random.random()
        return name, pos, speed, tasks.Participant(name, pos, speed)

    def test_init(self):
        name, pos, speed, part = self.prepare_part()

        self.assertEqual(name, part.name)
        self.assertEqual(pos, part.pos)
        self.assertEqual(speed, part.speed)

    def test_time_to(self):
        _, part_pos, part_speed, part = self.prepare_part()
        _, _, pos = TestVector.prepare_vec()
        finish = tasks.NamedPos(TestNamedPos.rand_name(), pos)

        result = part.time_to(finish)
        true_result = part_pos.distance_to(finish.pos) / part_speed

        self.assertEqual(true_result, result)


class TestRace(unittest.TestCase):
    def test_race(self):
        finish = tasks.NamedPos(TestNamedPos.rand_name(), tasks.Vector(random.random(), random.random()))
        _, _, _, part = TestParticipant.prepare_part()
        minimal = part.time_to(finish), part
        participants = [part]
        for _ in range(random.randint(10, 100)):
            _, pos, speed, part = TestParticipant.prepare_part()
            if pos.distance_to(finish.pos) / speed < minimal[0]:
                minimal = pos.distance_to(finish.pos) / speed, part
            participants.append(part)

        result = tasks.race(*participants, finish=finish)

        self.assertEqual(minimal[1].name, result)