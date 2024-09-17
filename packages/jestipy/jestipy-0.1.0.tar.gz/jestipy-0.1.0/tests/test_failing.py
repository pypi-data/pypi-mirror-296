from jestipy.core import test, describe

describe("Failing Tests", lambda: [
    test.failing("failing test", lambda: test.expect(1 + 1).toBe(3)),
])
