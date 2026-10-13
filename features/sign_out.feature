Feature: Sign Out Functionality

   Background:
         Given the user is logged into the application

  @regression @ios @android
  Scenario: sign out flow
    When the user navigates to the More tab
    Then the More screen title should be displayed
    When the user scrolls to the bottom of the More screen
    And the user clicks on Sign Out
    And the user cancels the sign out confirmation
    Then the More screen should still be displayed
    When the user clicks on Sign Out
    And the user confirms the sign out action
    Then the Enter Email screen should be displayed

 @smoke @ios @android
 Scenario: sign out flow
    Given the user is logged into the application
    When the user navigates to the More tab
    Then the More screen title should be displayed
    When the user scrolls to the bottom of the More screen
    And the user clicks on Sign Out
    And the user confirms the sign out action
    Then the Enter Email screen should be displayed



 @sanity @ios @android
 Scenario: sign out flow
    Given the user is logged into the application
    When the user navigates to the More tab
    Then the More screen title should be displayed
    When the user scrolls to the bottom of the More screen
    And the user clicks on Sign Out
    And the user confirms the sign out action
    Then the Enter Email screen should be displayed


