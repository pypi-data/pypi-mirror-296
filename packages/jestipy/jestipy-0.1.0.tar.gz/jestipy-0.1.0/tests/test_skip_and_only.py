from jestipy.core import test, describe

describe("Skipped and Only Tests", lambda: [
    test.skip("skipped test", lambda: test.expect(1 + 1).toBe(3)),
    test.only("only test", lambda: test.expect(1 + 1).toBe(2)),
])
