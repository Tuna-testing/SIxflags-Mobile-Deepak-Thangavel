Run the program
Navigate to root folder 
check pytest to collet the items to run 

Parallel  - pytest -m "android or ios" -n 2
ONLY IN IOS - pytest -m ios
only in Android - pytest -m android



Get UDID of the device

Android - ADB devices
IOS - xcrun xctrace list devices

Allure 
Generate Allure - allure generate reports/allure-results -o reports/allure-report --clean

View allure report - allure serve reports/allure-results
Generate sharable allure report -> allure serve reports/allure-results allure generate reports/allure-results -o reports/allure-report --single-file --clean 


Device config stored in conftest.py
compile all files python -m compileall 
Dry run pytest --collect-only
syntaxerror flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

run test tag wise 
pytest -m "@tag name and platform name" 
pytest -m "smoke and android"
pytest -m "regression and ios"

for parallel execution 
pytest -n 2 --platform all -m <tag name>

generate feaure snippet :- pytest-bdd generate path of the feature file    

Dry run - pytest -m "smoke and ios" --collect-only

pytest test_cases/test_e2e_runner.py::test_03_sign_up_scenarios -m "smoke and android" -s -v

run in Android on uat env - pytest --platform android --env uat -n 0
generate and view aure report - allure serve reports/allure-results