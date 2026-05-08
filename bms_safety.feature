Feature: BMS Battery Safety Validation

  Scenario: Normal voltage is accepted
    Given a BMS cell with voltage 3.7 and temperature 25
    When the safety check runs
    Then the result should be PASS

  Scenario: Overvoltage triggers fault
    Given a BMS cell with voltage 5.1 and temperature 25
    When the safety check runs
    Then the result should be FAIL
    And a ValueError should be raised

  Scenario: High temperature triggers fault
    Given a BMS cell with voltage 3.7 and temperature 60
    When the safety check runs
    Then the result should be FAIL
    And a ValueError should be raised