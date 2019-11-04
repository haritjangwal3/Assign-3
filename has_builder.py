from abc import ABC, abstractmethod


# The whole product
class Car:
    """
    The final product.
    """

    def __init__(self):
        self._wheels = list()
        self._engine = None
        self._body = None

    def specification(self):
        print("body: {}".format(self._body.shape))
        print("engine horsepower: {}".format(self._engine.horsepower))
        print("tire size: {}\'".format(self._wheels[0].size))


# Car parts
class Wheel:
    def __init__(self):
        self.__size = None

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        self.__size = size


class Engine:
    def __init__(self):
        self.__horsepower = None

    @property
    def horsepower(self):
        return self.__horsepower

    @horsepower.setter
    def horsepower(self, horsepower):
        self.__horsepower = horsepower


class Body:
    def __init__(self):
        self.__shape = None

    @property
    def shape(self):
        return self.__shape

    @shape.setter
    def shape(self, shape):
        self.__shape = shape


class AbstractBuilder(ABC):
    def __init__(self):
        self._product = Car()

    @abstractmethod
    def attach_wheels(self):
        pass

    @abstractmethod
    def set_engine(self):
        pass

    @abstractmethod
    def set_body(self):
        pass

    def get_result(self):
        return self._product


class JeepBuilder(AbstractBuilder):
    def attach_wheels(self):
        jeep_wheel = Wheel()
        jeep_wheel.size = 22
        self._product._wheels.append(jeep_wheel)

    def set_engine(self):
        jeep_engine = Engine()
        jeep_engine.horsepower = 400
        self._product._engine = jeep_engine

    def set_body(self):
        jeep_body = Body()
        jeep_body.shape = 'SUV'
        self._product._body = jeep_body


class NissanBuilder(AbstractBuilder):
    def attach_wheels(self):
        jeep_wheel = Wheel()
        jeep_wheel.size = 16
        self._product._wheels.append(jeep_wheel)

    def set_engine(self):
        jeep_engine = Engine()
        jeep_engine.horsepower = 85
        self._product._engine = jeep_engine

    def set_body(self):
        jeep_body = Body()
        jeep_body.shape = 'hatchback'
        self._product._body = jeep_body


class Director(object):
    def __init__(self, builder):
        if not isinstance(builder, AbstractBuilder):
            raise TypeError('please pass in a builder object')
        self.__builder = builder
        self.__build_lock = False

    def construct(self):
        self.__build_lock = True
        self.__builder.set_body()
        self.__builder.set_engine()
        for _ in range(4):
            self.__builder.attach_wheels()
        self.__build_lock = False

    def set_builder(self, new_builder):
        if self.__build_lock:
            raise RuntimeError('builder is building stuff')
        self.__builder = new_builder


if __name__ == '__main__':
    print('building Jeep...')
    jeep_builder = JeepBuilder()
    director = Director(jeep_builder)
    director.construct()
    jeep_builder.get_result().specification()

    print('')

    print('building Nissan...')
    nissan_builder = NissanBuilder()
    director.set_builder(nissan_builder)
    director.construct()
    nissan_builder.get_result().specification()
