from jestipy.core import test, describe

test.beforeAll(lambda: print("Running setup before all tests"))

describe("Lifecycle Hooks", lambda: [
    test("Test 1", lambda: test.expect(1).toBe(1)),
    test("Test 2", lambda: test.expect(1).toBe(1)),
])
