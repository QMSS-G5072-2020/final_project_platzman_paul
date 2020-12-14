# Week 7 - Testing

![](images/testing_banner_01.png)

## Automated vs. Manual Testing

![](images/human_vs_robot.png)

# Automated vs. Manual Testing

When writing code we often intuitively test a couple of use cases, something known as **exploratory testing**, a form of manual testing. Usually, there is no exhaustive plan, just exploring the options.

You could think of a list of  
  - all the **features and methods** your code has
  - the different **input** it can accept
  - and the **expected results**

Now, _each time you make a change to your code_, you need to go through every single item on that list and check it.

Not much fun! Hence the need for automated testing.

## Unit Tests vs. Integration Tests

Suppose your code is an API that calls some results from Google and provides back the URLs of the top results and the (NLP based) sentiment of the text of the web sites.

An **integration test** of this code would run the API call and see if the Top 10 results coming back are complete (this would be a _test assertion_), provide reasonable sentiment estimates etc. **Testing multiple components** is known as integration testing.

But suppose the sentiment scores are unexpected or incomplete. What now?

Ideally, we also have test of each sub-part of our code. Are we able to get 10 results back from Google, can we get text from all these URLs. Do our NLP and sentiment functions work properly ...

A **unit test** is a smaller test, one that **checks that a single component operates in the expected way**. A unit test helps you to isolate what is broken in your code and fix it faster.


## Unit Tests vs. Integration Tests

![](images/unit-tests-passing-no-integration-tests.jpg)

## Choosing a test runner

There are lots of available **test runners** in Python. 

- `unittest`: built-in standard library. Basic framework for writing, discovering, and running tests in python.
- `nose` and `nose2`: Used to be a very common test runner on python project because it provided a lot  of missing functionality from python `unittest`. The original nosetests is a mostly inactive project in maintenance mode, and the successor `nose2` is not too popular anymore either.
- `pytest`: by far the most popular python test runner out there. It provides a great user experience, has great integration with lots of editors (e.g. Pycharm) and seems to have the most momentum as a python test runner.

We will focus on `pytest` in this course.

![](images/pytest_logo.png)

# Writing Unit Tests



Suppose we wanted to test our palindrome function below:


```python
def palindrome_detector(s):
    """Return True if string, once downcased and
    with spaces removed, is a palindrome, else return False."""
    s = s.lower().replace(' ', '')
    return s == s[::-1]
```


```python
palindrome_detector('hello')
```




    False




```python
palindrome_detector('Anna')
```




    True



## Writing a test function

- Unit tests are python functions.
- Name you test function name so that it begins with `test_`. This is a naming convention but some test runners actually pick up all files and functions with that prefix.
- Your test function should contain an **assert statement** comparing the **actual result** with the **expected result**.

For example, suppose we wanted to test our palindrome function:


```python
def test_palindrome_detector():
    example = 'Lisa Bonet ate no basil'
    expected = True
    actual = palindrome_detector(example)
    assert actual == expected

test_palindrome_detector()
```

Kind of anti-climactic but no output is good here because that means the assertion was not raised and hence the test passed.

## Example: Testing the `sum` function

Let's test the built-in `sum` function. How would you write two unit tests that ensure that the sum functions works for (1) a list of numbers and (2) a tuple of numbers?


```python
def test_sum_with_list():
    assert sum([1, 2, 3]) == 6, "Should be 6"

def test_sum_with_tuple():
    assert sum((1, 2, 2)) == 6, "Should be 6"
```


```python
test_sum_with_list()
test_sum_with_tuple() ## Just to make sure this works, I set the test up to fail above.
```


    ---------------------------------------------------------------------------

    AssertionError                            Traceback (most recent call last)

    <ipython-input-60-7eaf02e5e63f> in <module>
          1 test_sum_with_list()
    ----> 2 test_sum_with_tuple() ## Just to make sure this works, I set the test up to fail above.
    

    <ipython-input-59-3d1abb669b8c> in test_sum_with_tuple()
          3 
          4 def test_sum_with_tuple():
    ----> 5     assert sum((1, 2, 2)) == 6, "Should be 6"
    

    AssertionError: Should be 6


## Running tests at the command-line

We can run tests from the command line. Place the the two test functions (with the second test corrected) into a file called `test_sum.py`. To run it, you go into the terminal and type:

        py.test test_sum.py

This is short for

        python -m pytest test_sum.py

which will also work.

Add the `-vv` flag to get an even fuller report:

        py.test -vv test_sum.py

If you have lots of tests in `test_sum.py` and want to run just one of them:

        py.test -vv test_sum.py::test_sum_with_list



## Running `test_sum.py` in the terminal

A passing test will be indicated by a `.` and failing one with an `F`. 

![](images/test_sum_terminal_04.png)

With the verbose flag, we get a list of test and an indication whether they passed:

![](images/test_sum_terminal_05.png)

## Running unit tests in Pycharm

If you’re using the PyCharm IDE, you can run `pytest` by following these steps:

1. In the Project tool window, select the `tests` directory.
2. On the context menu, choose the `run` command for your file tests file. For example, choose _Run `Unittests` in my Tests…_.

This will execute `unittest` in a test window and give you the results within PyCharm ([here for more](https://www.jetbrains.com/help/pycharm/performing-tests.html)):

![](images/pycharm_run_pytest.png)
    
    

## How to Structure a Simple Test

Before we dive into writing tests, here is guideline on what to think about:

**What** do you want to test?
Are you writing a **unit test** or an **integration test**?

Then the structure of a test should loosely follow this workflow:

1. Create your **inputs**
2. Execute the code being tested, capturing the **output**
3. **Compare** the **actual** output with an **expected** result

![](images/comparison_funny.jpg)

![](images/unit_test_dilemma_funny.png)

## Example: Own sum function called `total`

Let's write our own sum function and test it. 


```python
def total(arg):
    total = 0
    for val in arg:
        total += val
    return total
```


```python
total([1,2,3])
```




    6




```python
total((1,2,3))
```




    6



So, good news so far: our function works and can take in lists and tuples.

## What would you want to check for this `total` function using unit tests? 

Here are few things we could check:

- Can it sum a list, set, or dict?
- Can it sum a list of floats?
- Can it sum a list of integers?
- What happens if we provide a single integer rather than an iterable?
- What happens if send along a bad value, like a string?
- Do we get the correct sum if we include negative values?
- What if one of the values is missing?  
...

![](images/cant_fail_unit_tests_meme.png)

## Example: Write unit test for `total` testing functionality missing values


```python
def test_total_with_missing_values():
    actual = total([1, 2, np.nan])
    assert np.isnan(actual) # "Should be NaN."
    
test_total_with_missing_values()
```

So, the expected behavior for our function is to return `NaN` when an missing values is included. You could, of course, go back to the function and implement it differently. 

# Asserting with the `assert` statement

In each test, we compare the `actual` output of function with an `expected` output. 

Basic python assertion with the `assert` statement (as we have used thus far) are a good way to get started. In addition, the `unittest` package comes with some methods to assert on the values, types, and existence of variables. Here are some of the most commonly used methods:

| Method | Equivalent to  |
|---------| -------------- |
.assertEqual(a, b)	| a == b
.assertTrue(x)	| bool(x) is True
.assertFalse(x)	| bool(x) is False
.assertIs(a, b)	| a is b
.assertIsNone(x) |	x is None
.assertIn(a, b)	| a in b
.assertIsInstance(a, b)	| isinstance(a, b)

`.assertIs()`, `.assertIsNone()`, `.assertIn()`, and `.assertIsInstance()` all have opposite methods, named `.assertIsNot()`, and so forth.

![](images/assert_coffee.jpg)

## Assertions about expected exceptions

If our code is meant to raise exceptions, we can also test that these are raised correctly. In order to write assertions about raised exceptions, you can use `pytest.raises` as a context manager like this:


```python
with pytest.raises(ZeroDivisionError):
    1 / 0
```

If you code does not raise the _expected exception_ the test will fail:


```python
with pytest.raises(ZeroDivisionError):
    1 / 1
```


    ---------------------------------------------------------------------------

    Failed                                    Traceback (most recent call last)

    <ipython-input-70-86576288d062> in <module>
          1 with pytest.raises(ZeroDivisionError):
    ----> 2     1 / 1
    

        [... skipping hidden 2 frame]
    

    Failed: DID NOT RAISE <class 'ZeroDivisionError'>


# `pytest` functionalities for improved testing

![](images/python_testing_with_pytest.png)

## Using context-sensitive comparisons

`pytest` really starts to shine when we tap into its extended functionality. It does offer great support for providing context-sensitive information when it encounters comparisons.


```python
def test_set_comparison():
    set1 = set("1308")
    set2 = set("8035")
    assert set1 == set2
```

When run with `pytest` (see file `test_with_context.py`), we obtain meaningful comparison going well beyond the simple exception.

## Using context-sensitive comparisons

![](images/set_assertion_with_context.png)

See here for many more example: https://docs.pytest.org/en/2.0.3/example/reportingdemo.html.

## Using context-sensitive comparisons

Here is another example of testing long strings:


```python
def test_eq_long_text():
        a = '1'*100 + 'a' + '2'*100
        b = '1'*100 + 'b' + '2'*100
        assert a == b
```

![](images/test_long_strings_comparison.png)

## Using context-sensitive comparisons

Here a last example with sets. In short, `pyest` makes finding bugs a lot easier on the eye.


```python
def test_eq_set():
    assert set([0, 10, 11, 12]) == set([0, 20, 21])
```

![](images/test_difference_in_sets.png)

## Testing multiple examples efficiently

Let's go back to our palindrome checking function above. Suppose we want to check a bunch of examples. Writing separate tests would not be great because it would create lots of tests with repetitive code. Instead, we could use a simple loop:


```python
def test_palindrome_detector_looping():
    examples = [
        ('deleveled', True),
        ('Malayalam', True),
        ('detartrated', True),
        ('a', True),
        ('repaper', True),
        ('Al lets Della call Ed Stella', True),
        ('Lisa Bonet ate no basil', True),
        ('Linguistics', False),
        ('Python', False),
        ('palindrome', False),
        ('an', False),
        ('re-paper', False)]
    for example, expected in examples:
        result = palindrome_detector(example)
        assert result == expected
```

Not bad but with a major drawback: the test will stop (and the test report "Failed") as soon as it hits a case where the assert statement returns False. So we will not be able to see how we did on later tests, which might cause us to fail to see the full scope of the problems.

## Testing multiple examples efficiently using `@pytest.mark.parametrize`

We can test lots of test examples using `@pytest.mark.parametrize`.

To do this better, `pytest` uses Python decorators. I have only mentioned them once or twice, but [here](https://realpython.com/primer-on-python-decorators/) is a good tutorial.


```python
@pytest.mark.parametrize("example, expected", [
    ('deleveled', True),
    ('Malayalam', True),
    ('detartrated', True),
    ('a', True),
    ('repaper', True),
    ('Al lets Della call Ed Stella', True),
    ('Lisa Bonet ate no basil', True),
    ('Linguistics', False),
    ('Python', False),
    ('palindrome', False),
    ('an', False),
    ('re-paper', False)
])
def test_palindrome_detector_looping_(example, expected):
    result = palindrome_detector(example)
    assert result == expected
```

Here are couple of important things to notice:
    
- parametrize is spelled with only two `e`'s.
- The first argument to `@pytest.mark.parametrize` is a string that gives the arguments you'll be feeding to the test.
- The actual test needs to be given those same arguments, in the same order and with the same names, but as a list of arguments (as usual in Python).
- The second argument to `@pytest.mark.parametrize` is a list. Each member of the list has to have the same number of arguments as the test has.
- pytest reports each of the test cases as a separate test; each can in turn pass or fail on its own.

## Shared resources using fixtures

It is quite common to have **tests that share a single resource** (e.g. some API call, a data file etc. In that case, pytest allows us to share that resource using a `fixture` on your test functions.

### Example:
Suppose you have written some functions that read in and process a corpus of tweets. For the testing of all these functions, you may rely on a local copy of a test corpus. It would be inefficient to read the corpus in for every test, and doing that would lead to code with a lot of redundancy.

The `@pytest.fixture` decorator allows you to set up these resources once and use them across your tests.



## Example: Use of `@pytest.fixture`


```python
import pytest
import pandas as pd

@pytest.fixture
def toy_csv_df():
    link = "https://web.stanford.edu/class/linguist278/data/toy-csv.csv"
    df = pd.read_csv(link, index_col=0)
    return df

def test_height_mean(toy_csv_df):
    expected = 68.9003
    result = round(toy_csv_df['Height'].mean(), 4)
    assert result == expected

def test_occupation_counts(toy_csv_df):
    expected = pd.Series({'Psychologist': 7, 'Linguist': 3})
    result = toy_csv_df['Occupation'].value_counts()
    assert result.equals(expected)

@pytest.mark.parametrize("subject, expected", [
    (1, "Psychologist"),
    (5, "Linguist")
])
def test_subject_values(toy_csv_df, subject, expected):
    result = toy_csv_df.loc[subject]['Occupation']
    assert result == expected
```

Most importantly, we can see that `toy_csv_df` is defined as a fixture and then given as an argument to any tests that need it. `pytest` will run `toy_csv_df` just once here.

## Side effects 

When introducing functions we also learned about `side effects` which is altering other things in the environment, such as the attribute of a class, a file on the filesystem, or a value in a database that go beyond the `return` statement of a function. 

A pure function is a function which:
- Given the same input, will always return the same output.
- Doesn’t depend on and doesn’t modify the states of variables out of its scope.
- Relies on no side-causes — hidden inputs.
- Produces no side effects — hidden outputs.

When testing, we need to **decide if the side effect is being tested** before including it in your list of assertions.

![](images/functional-programmig-side-effects.png)

## Single Responsibility Principle


If you find that the unit of code you want to test has lots of side effects, you might be breaking the **Single Responsibility Principle** which [states]((https://en.wikipedia.org/wiki/Single-responsibility_principle)) that _every module, class or function in a computer program should have responsibility over a single part of that program's functionality, which it should encapsulate._

Breaking the Single Responsibility Principle means the piece of code is doing too many things and would be better off being refactored. Following the Single Responsibility Principle is a great way to design code that it is easy to write repeatable and simple unit tests for, and ultimately, reliable applications.

![](images/single_responsibility_principle.png)

## Isolating Behaviors in Your Code

![](images/side_effect_bears.gif)

Side effects make unit testing harder since, each time a test is run, it might give a different result, or even worse, one test could impact the state of the application and cause another test to fail!






## How to deal with side effects?

There are some simple techniques you can use to test parts of your application that have many side effects:

- **Refactor your code** to follow the _Single Responsibility Principle_
- **Mock out** any method or function calls to remove side effects (see [`pytest-mock` package](https://pypi.org/project/pytest-mock/) and this tutorial on [command line app testing](https://realpython.com/python-cli-testing/#mocks))
- Use **integration testing** instead of unit testing for this piece of the application

# Mocking in Python

![](images/mock_banner.png)

## Mocking out parts of a function

A **mock** replaces a function with a dummy you can program to do whatever you choose.

In Python, to mock, be it functions, objects or classes, you will mostly use `Mock` class which comes from the built-in `unittest.mock` module.

In addition, we will rely on `pytest-mock` to add a mocker fixture to allow these mocking capabilities in `pytest`.




![](images/mocking_fish.jpg)

## Mocking a simple function

Say, we have a function `get_operating_system` that tells us whether we are using Windows or Linux and would like to write a unit test for it.


```python
# application.py 
from time import sleep  
def is_windows():    
    # This sleep could be some complex operation instead
    sleep(5)  
    return True
def get_operating_system():    
    return 'Windows' if is_windows() else 'Linux'
```

This function uses another function `is_windows` to check if the current system is Windows or not. 

For at least two reasons, we should mock out `is_windows` in our test of `get_operating_system`.

1. Speed
Assume that this `is_windows` function is quite complex taking several seconds to run. We can simulate this slow function by making the program sleep for 5 seconds every time it is called.

2. OS Interoperability
Clearly, `is_windows` would give us different answers depending on the operating system. But given that we run the test on one specific operating system, our test for `get_operating_system` would only ever consider one specific part of the code.

## Testing `get_operating` system with `pytest`

A simple `pytest` module would be:


```python
# test_application.py
# from application import get_operating_system

def test_get_operating_system():
    assert get_operating_system() == 'Windows'
```

Since, `get_operating_system()` calls a slower function `is_windows`, the test is going to be slow. This can be seen below in the output of running pytest which took 5.07 seconds.

![](images/test_get_operating_system.png)

## Mocking out 

Unit tests should be fast and operating system independent. So, let's mock out the `is_windows` function. This time we simply determine that the `is_windows` function will return `True` without taking those five long seconds. We can patch it as follows:


```python
# 'mocker' fixture provided by pytest-mock
def test_get_operating_system(mocker):  
    # Mock the slow function and return True always
    mocker.patch('application.is_windows', return_value=True) 
    assert get_operating_system() == 'Windows'
```

And indeed, now it runs quickly and we can set whatever value we want for `is_windows` independent of our operating system.

![](images/test_get_operating_system_with_mock.png)

## Real unit tests with Mock

When we do the patch, we create a new mocked function that gets called, bypassing the original function. That way, we can test the `get_operating_system` function independent of the `is_windows` function - a true unit test.

![](images/mock_is_windows.png)

For the full example, see this mock tutorial here (part [1](https://medium.com/analytics-vidhya/mocking-in-python-with-pytest-mock-part-i-6203c8ad3606) and [2](https://medium.com/@durgaswaroop/writing-better-tests-in-python-with-pytest-mock-part-2-92b828e1453c))

# Writing integration tests

![](images/testing_banner_02.png)

## Unit testing vs. Integration testing

So far we mainly talked about unit testing. Unit testing is a great way to build predictable and stable code. But at the end of the day, your application needs to work when it starts!



**Integration testing** is the **testing of multiple components of the application** to check that they **work together**. 

Integration testing might require acting like a consumer or user of the application by:

- Calling an HTTP REST API
- Calling a Python API
- Calling a web service
- Running a command line

![](images/unit_vs_integration_test.gif)

## Testing pyramid

![](images/testing_pyramid.png)

## Project Organization

Once we combine our code into a package, it is best to **separate tests out from the actual source code**. 

Similarly, it is often useful to separate unit test and integration test to keep an overview.

![](images/project_structure_tests.png)
