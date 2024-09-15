import asyncio
import time

PASSED_SYMBOL = "✔"
FAILED_SYMBOL = "✖"
SKIPPED_SYMBOL = "➖"
TODO_SYMBOL = "📝"
ONLY_SYMBOL = "⭐"
RUNNING_SYMBOL = "➤"

_test_registry = []
_skipped_tests = []
_only_tests = []
_todo_tests = []
_failing_tests = []

_lifecycle_hooks = {
    "beforeAll": None,
    "beforeEach": None,
    "afterEach": None,
    "afterAll": None
}

test_results = []
test_file_stats = []

def describe(name, fn):
    print(f"\n++++ {name} ++++")  
    fn()

def it(name, fn):
    _test_registry.append((name, fn))

def test(name, fn):
    _test_registry.append((name, fn))

def expect(value):
    class Matcher:
        def toBe(self, expected):
            if value != expected:
                raise AssertionError(f"{FAILED_SYMBOL} Expected {value} to be {expected}")
            else:
                print(f"{PASSED_SYMBOL} {value} equals {expected}") 
    return Matcher()

def test_skip(name, fn=None):
    print(f"{SKIPPED_SYMBOL} Skipped: {name}")
    _skipped_tests.append(name)

def test_only(name, fn):
    print(f"{ONLY_SYMBOL} Running only: {name}")
    _only_tests.clear()
    _only_tests.append((name, fn))

def test_failing(name, fn):
    async def failing_test():
        try:
            fn()
            raise AssertionError(f"Expected test to fail but it passed")
        except AssertionError:
            print(f"{PASSED_SYMBOL} Failing test '{name}' correctly failed.")
    _failing_tests.append((name, failing_test))

def test_todo(name):
    print(f"{TODO_SYMBOL} TODO: {name}")
    _todo_tests.append(name)

def beforeAll(fn):
    _lifecycle_hooks["beforeAll"] = fn

def afterAll(fn):
    _lifecycle_hooks["afterAll"] = fn

def beforeEach(fn):
    _lifecycle_hooks["beforeEach"] = fn

def afterEach(fn):
    _lifecycle_hooks["afterEach"] = fn

test.beforeAll = beforeAll
test.afterAll = afterAll
test.beforeEach = beforeEach
test.afterEach = afterEach
test.failing = test_failing
test.skip = test_skip
test.only = test_only
test.todo = test_todo

test.concurrent = lambda name, fn, timeout=5: asyncio.wait_for(fn(), timeout)

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

test.each = lambda table: test_each(test, table)
describe.each = lambda table: describe_each(describe, table)

test.expect = expect

async def run_tests():
    total_tests = len(_test_registry)
    passed_tests = 0
    failed_tests = 0
    skipped_tests = len(_skipped_tests)
    todo_tests = len(_todo_tests)

    await run_lifecycle_hooks("beforeAll")

    for name, fn in _test_registry:
        file_start_time = time.time()
        file_passed = 0
        file_failed = 0
        file_skipped = 0
        file_todo = 0

        if name in _skipped_tests:
            print(f"{SKIPPED_SYMBOL} Skipped: {name}")
            file_skipped += 1
            continue
        if name in _todo_tests:
            print(f"{TODO_SYMBOL} TODO: {name}")
            file_todo += 1
            continue

        await run_lifecycle_hooks("beforeEach")

        start_time = time.time()
        try:
            print(f"{RUNNING_SYMBOL} Running test: {name}...")
            await fn()
            duration = time.time() - start_time
            print(f"{PASSED_SYMBOL} {name} ({duration:.2f}s)")
            passed_tests += 1
            file_passed += 1
        except AssertionError as e:
            duration = time.time() - start_time
            print(f"{FAILED_SYMBOL} {name} ({duration:.2f}s): {e}")
            failed_tests += 1
            file_failed += 1

        await run_lifecycle_hooks("afterEach")

        file_duration = time.time() - file_start_time
        print(f"\n--- Stats for {name} ---")
        print(f"Passed: {file_passed}, Failed: {file_failed}, Skipped: {file_skipped}, TODO: {file_todo}")
        print(f"Time for {name}: {file_duration:.2f}s\n")

    await run_lifecycle_hooks("afterAll")

    # Final stats summary
    print(f"\n--- Final Test Suite Stats ---")
    print(f"Total tests: {total_tests}")
    print(f"{PASSED_SYMBOL} Passed: {passed_tests}")
    print(f"{FAILED_SYMBOL} Failed: {failed_tests}")
    print(f"{SKIPPED_SYMBOL} Skipped: {skipped_tests}")
    print(f"{TODO_SYMBOL} TODO: {todo_tests}")
    print(f"Time for all tests: {time.time() - file_start_time:.2f}s")

async def run_with_timeout(fn, timeout):
    try:
        if asyncio.iscoroutinefunction(fn):
            await asyncio.wait_for(fn(), timeout)
        else:
            await asyncio.wait_for(asyncio.to_thread(fn), timeout)
    except asyncio.TimeoutError:
        raise TimeoutError(f"Test exceeded timeout of {timeout} seconds")

async def run_lifecycle_hooks(hook_name):
    hook = _lifecycle_hooks.get(hook_name)
    if hook:
        print(f"Running {hook_name} hook")
        await run_with_timeout(hook, 5)  
