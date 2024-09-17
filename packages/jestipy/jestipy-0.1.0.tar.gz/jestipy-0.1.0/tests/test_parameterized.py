from jestipy.core import test

# Parameterized tests
test.each([
    [1, 2, 3],
    [2, 3, 5],
    [3, 3, 6]
])("adds %i + %i to equal %i", lambda a, b, expected: test.expect(a + b).toBe(expected))
