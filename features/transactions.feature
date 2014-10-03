Feature: Features
  As a user
  I want to manage transactions

  Scenario: List transactions
    Given the following accounts
      | name | number    |
      | test | 987654321 |
    And the following transactions
      | account | date_time  | desc  | amount  | reconciled |
      | test    | 01-01-2014 | desc1 | 100.00  | False      |
      | test    | 10-05-2007 | desc2 | -76.00  | False      |
    When I run "bdgt tx list test"
    Then the command output should equal:
      """
      | 2007-05-10 | desc2 | -76.00 | N |
      | 2014-01-01 | desc1 | 100.00 | N |
      """
