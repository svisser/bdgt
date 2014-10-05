Feature: Import transactions
  As a user
  I want to import transactions from a file
  In order to add them to an account quickly

  Scenario: Import MT940
    Given the following accounts
      | name     | number    |
      | account1 | 987654321 |
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
    When I run "bdgt import account1 mt940 test.mt940"
    Then the command output should equal:
      """
      Imported 1 transactions into account 'account1'
      """
    And account "account1" has 1 unreconciled transactions

  Scenario: Import OFX
    Given the following accounts
      | name     | number    |
      | account1 | 987654321 |
    And a file named "test.ofx" with:
      """
      <OFX>
        <SIGNONMSGSRSV1>
          <SONRS>
            <STATUS>
              <CODE>0
              <SEVERITY>INFO
            </STATUS>
            <DTSERVER>20071015021529.000[-8:PST]
            <LANGUAGE>ENG
            <DTACCTUP>19900101000000
            <FI>
              <ORG>MYBANK
              <FID>01234
            </FI>
          </SONRS>
        </SIGNONMSGSRSV1>
        <BANKMSGSRSV1>
            <STMTTRNRS>
              <TRNUID>23382938
              <STATUS>
                <CODE>0
                <SEVERITY>INFO
              </STATUS>
              <STMTRS>
                <CURDEF>USD
                <BANKACCTFROM>
                  <BANKID>987654321
                  <ACCTID>098-121
                  <ACCTTYPE>SAVINGS
                </BANKACCTFROM>
                <BANKTRANLIST>
                  <DTSTART>20070101
                  <DTEND>20071015
                  <STMTTRN>
                    <TRNTYPE>CREDIT
                    <DTPOSTED>20070315
                    <DTUSER>20070315
                    <TRNAMT>200.00
                    <FITID>980315001
                    <NAME>DEPOSIT
                    <MEMO>automatic deposit
                  </STMTTRN>
                </BANKTRANLIST>
                <LEDGERBAL>
                  <BALAMT>5250.00
                  <DTASOF>20071015021529.000[-8:PST]
                </LEDGERBAL>
                <AVAILBAL>
                  <BALAMT>5250.00
                  <DTASOF>20071015021529.000[-8:PST]
                </AVAILBAL>
              </STMTRS>
            </STMTTRNRS>
        </BANKMSGSRSV1>
      </OFX>
      """
    When I run "bdgt import account1 ofx test.ofx"
    Then the command output should equal:
      """
      Imported 1 transactions into account 'account1'
      """
    And account "account1" has 1 unreconciled transactions

  Scenario: Show error when importing into a non-existant account
    Given the following accounts
      | name     | number    |
      | account1 | 987654321 |
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
    When I run "bdgt import account2 mt940 test.mt940"
    Then the command output should equal:
      """
      Error: Account 'account2' not found.
      """
