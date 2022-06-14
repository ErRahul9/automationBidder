from behave import given, when, then


@given('"{SysName}" system is up and running')
def givenCondition(context, SysName):
    print("sysName")


@when('we update the "{testCase}" data in the bidder file')
def step_impl_goto_page(context, testCase):
    print('I go to {} page'.format(testCase))


@then('the amount generated by the bidder file is "{Amount}" and Response recieved from beeswax is "{Response}"')
def step_impl_verify_component(context, component):
    print('I see this component "{}"'.format(component))