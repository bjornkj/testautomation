


def min_dekorator(f):
    def inner():
        print("Hejsan, jag är en dekorerad funktion")
        f()
        print("hejdå")
    return inner


@min_dekorator
def do_a():
    print("a")


f = do_a

def square(n):
    return n*n


def yield_demo1():
    yield 1
    yield 2
    yield 3


def yield_demo2():
    a = 1
    r = 1
    while True:
        yield r
        r = r * a
        a += 1




def fixture_example():
    print("Setting up before test")
    yield "hej"
    print("Teardown")



if __name__ == '__main__':
    v = next(fixture_example())
    assert v == "hej"
    next(fixture_example())


