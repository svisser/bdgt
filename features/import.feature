Feature: Import transactions
  As a user
  I want to import transactions from a file
  In order to add them to an account quickly

  Scenario: Import MT940
    Given the following accounts
      | name | number    |
      | test | 987654321 |
    And a file named "test.mt940" with:
      """
      ABNANL2A
      940
      ABNANL2A
      :20:ABN AMRO BANK NV
      :25:123456789
      :28:13501/1
      :60F:C120511EUR5138,61
      :61:1205120514C500,01N654NONREF
      987654321
      :86:/TRTP/SEPA OVERBOEKING/IBAN/FR12345678901234/BIC/GEFRADAM
      /NAME/QASD JGRED/REMI/description lines/EREF/NOTPRO
      VIDED
      :62F:C120514EUR5638,62
      """
    When I run "bdgt import mt940 test.mt940"
    Then the command output should equal:
      """
      Imported 1 transactions into account 'test'
      """
    And account "test" has 1 unreconciled transactions
