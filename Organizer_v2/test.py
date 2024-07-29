def test_func(info):
    info = info
    def wrapper():
        print(info)
    return wrapper


test = test_func('test')
test1 = test_func('test1')

test()
test1()
