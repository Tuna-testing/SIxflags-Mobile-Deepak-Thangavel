Feature: User Signup and Account Creation Flow

  @regression @android @ios
  Scenario: regression sign up flow
    Given User enters an unregistered email and submits
    And User verifies the UI elements for the signup bottom sheet
    And User clicks submit on the signup bottom sheet
    And User verifies the UI elements for the signup form
    When User enters an invalid first name and verifies the error message
    And User enters a valid first name
    And User enters an invalid last name and verifies the error message
    And User enters a valid last name
    And User selects date of birth
    And User selects a park with phone number and enters the phone number
    And User selects a park without phone number
    And User selects a park with phone number and enters the phone number
    And User enters a valid password and shows the password
    And User enters a mismatching confirm password and verifies the error message
    And User enters a valid confirm password and shows the password
    And User hides the password and confirm password
    Then User verifies the SMS checkbox is only visible when a park with phone number is selected
    When User checks and unchecks the SMS option
    And User checks and unchecks the email option
    And User clicks create account
    Then User verifies the UI elements in the OTP bottom sheet
    When User enters an invalid OTP and verifies the error message
    And User clicks resend OTP and waits for 60 seconds
    And User enters a valid OTP and submits
    Then User verifies the success message and clicks login to your account

  @smoke @android @ios
  Scenario: smoke sign up flow
    Given User enters an unregistered email and submits
    And User verifies the UI elements for the signup bottom sheet
    And User clicks submit on the signup bottom sheet
    And User verifies the UI elements for the signup form
    When User enters a valid first name
    And User enters a valid last name
    And User selects date of birth
    And User selects a park with phone number and enters the phone number
    And User selects a park without phone number
    And User selects a park with phone number and enters the phone number
    And User enters a valid password and shows the password
    And User enters a valid confirm password and shows the password
    And User hides the password and confirm password
    And User checks and unchecks the SMS option
    And User checks and unchecks the email option
    And User clicks create account
    Then User verifies the UI elements in the OTP bottom sheet
    When User enters a valid OTP and submits
    Then User verifies the success message and clicks login to your account

  @sanity @android @ios
  Scenario: sanity sign up flow
    Given User enters an unregistered email and submits
    And User clicks submit on the signup bottom sheet
    When User enters a valid first name
    And User enters a valid last name
    And User selects date of birth
    And User selects a park with phone number and enters the phone number
    And User enters a valid password and shows the password
    And User enters a valid confirm password and shows the password
    And User checks and unchecks the SMS option
    And User checks and unchecks the email option
    And User clicks create account
    When User enters a valid OTP and submits
    Then User verifies the success message and clicks login to your account