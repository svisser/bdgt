from behave import given


@given('a file named "{fname}" with')
def step_create_file(context, fname):
    with open(fname, 'w') as f:
        f.write(context.text)
    context.test_data_files.append(fname)
