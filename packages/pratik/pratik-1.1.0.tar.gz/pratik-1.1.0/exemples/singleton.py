from pratik.singleton import Singleton


def basic_exemple():
    class BasicSingleton(Singleton):
        def singleton_init(self, value):
            self.value = value

    print("\n# Basic example of using singleton")

    print("\t A first singleton is initialized.")
    print("\t\t Singleton 1 (BasicSingleton) takes 42.")
    singleton1 = BasicSingleton(42)
    print("\t\t\t - Singleton 1:", singleton1.value)

    print("\t A second singleton is created without parameters.")
    print("\t\t Singleton 2 (BasicSingleton) takes nothing.")
    singleton2 = BasicSingleton()
    print("\t\t\t - Singleton 1:", singleton1.value)
    print("\t\t\t - Singleton 2:", singleton2.value)

    print("\t A third singleton is created with 84 as parameter.")
    print("\t\t Singleton 3 (BasicSingleton) takes 84.")
    singleton3 = BasicSingleton(84)
    print("\t\t\t - Singleton 1:", singleton1.value)
    print("\t\t\t - Singleton 2:", singleton2.value)
    print("\t\t\t - Singleton 3:", singleton3.value)


def create_singleton_without_parameters_exemple():
    class BasicSingleton(Singleton):
        def singleton_init(self, value):
            self.value = value

    print("\n# Create a first singleton without parameters")

    print("\t A first singleton is initialized.")
    print("\t\t Singleton 1 (BasicSingleton) takes nothing.")
    try:
        singleton1 = BasicSingleton()
    except TypeError as te:
        print("\t\t\t -", type(te).__name__, ':', te)


def multiple_singleton_exemple():
    class FirstBasicSingleton(Singleton):
        def singleton_init(self, value):
            self.value = value

    class SecondBasicSingleton(Singleton):
        def singleton_init(self, value):
            self.value = value

    print("\n# Multiple singleton type using library co-exists")

    print("\t A first singleton is initialized.")
    print("\t\t Singleton 1 (FirstBasicSingleton) takes 42.")
    singleton1 = FirstBasicSingleton(42)
    print("\t\t\t - Singleton 1:", singleton1.value)

    print("\t A second singleton is initialized.")
    print("\t\t Singleton 2 (SecondBasicSingleton) takes 84.")
    singleton2 = SecondBasicSingleton(84)
    print("\t\t\t - Singleton 1:", singleton1.value)
    print("\t\t\t - Singleton 2:", singleton2.value)


if __name__ == "__main__":
    basic_exemple()
    create_singleton_without_parameters_exemple()
    multiple_singleton_exemple()
