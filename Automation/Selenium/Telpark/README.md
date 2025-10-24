# TEST PLAN

| ID       | TEST_CASE_NAME | PRIORITY | AREA | TYPE | DESCRIPTION | TEST_EXECUTION
|:-----------:|:------:|:-----------:|:-----------:|:-----------:|:-----------:|:-----------:|
| TC01     | Login with valid credentials    | High  | Login | Functional | Validate that a user can log in successfully with valid credentials. | pytest -v test_login.py::test_login_sucessfull
| TC02     | Login with invalid credentials  | High  | Login | Negative | Validate system behavior when invalid credentials are used.| pytest -v test_login.py::test_login_unsucessfull
| TC03     | Validate logout    | Medium | Login | Functional | Ensure that the user can log out and session is cleared.
| TC04     | Verify “Mais opções” page layout redesign    | Medium | UI | Visual | Ensure that all UI elements match the new design specifications.
| TC05     | Verify presence of new “Veículos” menu option    | High | Vehicles | Functional/UI | Check that “Veículos” option is displayed and accessible.
| TC06     | Add a new vehicle with valid details (Other country)   | High | Vehicles | Functional | Validate adding a vehicle for country “Other”. | pytest -v test_vehicle.py::test_add_vehicle_other_country
| TC07     | Remove a vehicle successfully | High | Vehicles | Functional | Tests the ability to remove a vehicle. | pytest -v test_vehicle.py::test_remove_vehicle
| TC08     | Verify error when trying to add duplicate vehicle    | Medium | Vehicles | Negative | Validate app prevents adding the same vehicle twice. | pytest -v test_vehicle.py::test_add_duplicate_vehicle


| AREA  | TEST_EXECUTION |
|:-----------:|:------:|
| Login     | pytest -v test_login   |
| Vehicles  | pytest -v test_vehicle |
