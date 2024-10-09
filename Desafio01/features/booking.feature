Feature: API Booking

  Scenario: Create a booking
    Given I have valid booking details
    When I create a booking
    Then I should receive a confirmation from booking

  Scenario: Getting details of a booking
    Given I have a valid booking ID
    When I get the details of the booking
    Then I should see the correct booking information

  Scenario: Update a booking
    Given I have a valid token
    Given I have a valid booking ID
    And I have new booking details
    When I update the booking
    Then I should see the updated booking information

  Scenario: Delete a booking
    Given I have a valid token
    Given I have a valid booking ID
    When I delete the booking
    Then the booking should be deleted successfully

  Scenario: Trying to create a booking with invalid data
    Given I have invalid booking details
    When I try to create a booking
    Then I should receive a validation error

