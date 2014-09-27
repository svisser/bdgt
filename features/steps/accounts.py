from behave import given, when, then


@given('a set of specific accounts')
def step_add_accounts(context):
    for row in context.table:
        context.cmd_line.run("bdgt account add {}".format(row['name']))


@then('account "{account_name}" exists')
def step_account_exists(context, account_name):
    cmd = 'bdgt account list'
    cmd_output = context.cmd_line.run(cmd)
    assert account_name in cmd_output


@then('account "{account_name}" doesn\'t exist')
def step_account_doesnt_exist(context, account_name):
    cmd = 'bdgt account list'
    cmd_output = context.cmd_line.run(cmd)
    assert account_name not in cmd_output
