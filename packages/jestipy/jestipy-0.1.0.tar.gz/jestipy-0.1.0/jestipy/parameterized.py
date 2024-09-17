def test_each(test, table):
    def decorator(name, fn):
        for params in table:
            test_name = name % tuple(params)
            test(test_name, lambda: fn(*params))
    return decorator

def describe_each(describe, table):
    def decorator(name, fn):
        for params in table:
            describe_name = name % tuple(params)
            describe(describe_name, lambda: fn(*params))
    return decorator
