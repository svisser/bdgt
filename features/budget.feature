Feature: Budget
  As a user,
  I'd like to budget my spending by setting spending limits on categories
  So that I can track my spending in each category.

  Scenario: Set a weekly spending limit
    Given the following categories
      | name |
      | cat1 |
    When I run "bdgt set cat1 week 150.00"
    Then the command output should equal:
      """
      Budget for "cat1" is set to 150.00 per week
      """
    And "cat1" has 1 budget items

  Scenario: Set a monthly spending limit
    Given the following categories
      | name |
      | cat1 |
    When I run "bdgt set cat1 month 150.00"
    Then the command output should equal:
      """
      Budget for "cat1" is set to 150.00 per month
      """
    And "cat1" has 1 budget items

  Scenario: Set a quaterly spending limit
    Given the following categories
      | name |
      | cat1 |
    When I run "bdgt set cat1 quarter 150.00"
    Then the command output should equal:
      """
      Budget for "cat1" is set to 150.00 per quarter
      """
    And "cat1" has 1 budget items

  Scenario: Set a yearly spending limit
    Given the following categories
      | name |
      | cat1 |
    When I run "bdgt set cat1 year 150.00"
    Then the command output should equal:
      """
      Budget for "cat1" is set to 150.00 per year
      """
    And "cat1" has 1 budget items
