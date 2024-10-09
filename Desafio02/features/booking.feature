Feature: Booking App
  Scenario: Correct booking
    Given I am at home
    When I search for hotels in "Cusco"
    And I select the second available hotel
    And I enter personal information
    And I enter credit card information
    Then I should see the booking