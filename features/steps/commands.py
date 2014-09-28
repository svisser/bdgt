from nose.tools import ok_
from behave import then, when


@when('I run "{command}"')
def step_run_command(context, command):
    context.cmd_output = context.cmd_line.run(command)


@then('the command output should contain')
def step_output_contains(context):
    ok_(context.text in context.cmd_output)


@then('the command output should equal')
def step_output_equals(context):
    ok_(context.text == context.cmd_output.strip())
