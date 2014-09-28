Feature: Accounts
  As a user
  I want to manage multiple accounts
  So that transactions can be added to them.

  Scenario: Add an account
    When I run "bdgt account add test"
    Then the command output should equal:
      """
      Account 'test' created
      """
    And account "test" exists

  Scenario: Delete an account
    Given a set of specific accounts
      | name     |
      | cash     |
      | personal |
      | savings  |
    When I run "bdgt account delete cash"
    Then the command output should equal:
      """
      Account 'cash' deleted
      """
    And account "cash" doesn't exist

  Scenario: List accounts
    Given a set of specific accounts
      | name     |
      | cash     |
      | personal |
      | savings  |
    When I run "bdgt account list"
    Then the command output should equal:
      """
      cash
      personal
      savings
      """
