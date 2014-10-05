import os

from behave import given, then


@given('a file named "{fname}" with')
def step_create_file(context, fname):
    if '~' in fname:
        fname = os.path.expanduser(fname)

    if os.path.exists(fname):
        raise ValueError("{} already exists".format(fname))

    with open(fname, 'w') as f:
        f.write(context.text)
    context.test_data_files.append(fname)


@given("a file named '{fname}' doesn't exist")
def step_file_doesnt_exist(context, fname):
    if '~' in fname:
        fname = os.path.expanduser(fname)
    assert not os.path.exists(fname)


@given("a file named '{fname}' exists")
def step_file_exists(context, fname):
    if '~' in fname:
        fname = os.path.expanduser(fname)
    assert os.path.exists(fname)


@then("a file named '{fname}' was created")
def step_a_file_was_created(context, fname):
    if '~' in fname:
        fname = os.path.expanduser(fname)

    if os.path.exists(fname):
        context.test_data_files.append(fname)
    else:
        assert False
