# Development Log

## Day 1:

### Completed:
 - Created Github repo
 - Setup project structure with FastApi

### Decisions:
 - Chose FastApi because it supports clean API dev, testing and async communication

### Issues:

### Evidence:
 - Initial commit: "Project startup"



## Day 2:

### Completed:
 - Integrated backend with robot simulator REST API
 - Added status, map, sensor, move, and reset routes
 - Added validation for both coordinate bounds and battery percent
 - Added error handling for robot connection/API errors
 - Confirmed backend works thus far
 - Built a server-rendered dashboard, using Jinja templates
 - Added robot status and battery display, including corresponding warnings, interactive movement controls and all the required buttons and sections
 - Implemented a map visualisation, including obstacles, robot positioning and axis labels
 - Implemented HMTX partial rendering for robot status, map and connection displays
 - Added error handling on the displays for robot connection/API errors

 
### Decisions:
 -  Chose Jinja + HTMX frontend over something like react due to its reduced complexity, which allows more focus on backend reliability, architecture and API integration.
 - HTMX partial rendering was used to keep the dashboard display up to date whilst the robot moves, so the user can see its status and location on the map. Also, because each partial is individually rendered, if a robot connection/API error occurs, that section can be handled on its own, without breaking the whole dashboard.

### Issues:
 - FIXED/CONFIRMED: Robot wouldnt move long distances, and would change status to 'STUCK', was due to map constrictions, not backend error
 - FIXED: rendering errors when simulator response returned 'None' during API outages, fixed by adding defensive conditional rendering inside each partial template.
 - FIXED: during connection instability, the page would lose displays or break, and so fallbacks displays, ie 'attempting to reconnect' or offline indicators were added.
 - FIXED: map wouldnt refresh on the current move, you could only see the robots movements on the next move, initially tried refreshing the full page, but was slow and difficult to look at, so switched to HTMX partials where needed.

### Evidence:
 - Commit: "Implemented API integration"
 - Commit: "Implemented Dashboard"



## Day 3:

### Completed:
- Integrated SQlit database
- Completed the dedicated database layer, e.g. 'database.py', 'models.py'
- Implemented 'CommandLog' database which logs; command type, target coords, the result/success, and the utc timestamp of the action
- Cleaned up move robotapi and dashboard routes, including the changes made to log actions

### Decisions:
 - Used sqlite because its lightweight and doesnt require an external database server
 - timestamps stored in UTC to ensure consistency, avoiding timezone related issues

### Issues:
 - FIXED: Database tables were created but initially empty. Discovered that previously, the dashboard move route didnt call the correct robot_move_to funciton, which was where the moves get logged,
 now it calls the correct function that both moves and logs the movements of the robot.
 - UNFIXED: Currently the database setup only logs movement actions, the robots status, battery etc etc, are not logged, additional logging is required, which there was not time for today

### Evidence:
 - Commit: "Implemented action logger"

 
## Day 4:

### Completed:
 - Implemented a 'User' database model, which stores user account info
 - Implemented password hashing using passlib and bcrypt
 - Added a registration endpoint
 - Added validation for duplicate usernames

### Decisions:
 - Password hashing implemented to avoid storing plaintext sensitive credential, eg passwords

### Issues:
 - FIXED: Encountered an issue with bcrypt, where the newest version was not compatible with passlib, so swapped to using an older version (4.0.1)

### Evidence:
 - Commit: "Implemented user registration and password hashing"

## Day 5:

### Completed:
 - Added CI/CD automatic testing
 - Implemented login and logout session handling
 - Added login and logout corresponding displays
 - Added persistent storage for user ID, username, and role.
 - Modularised architecture further, by refactoring routes into their own route files
 - Create a separate command services file for service-layer helper functions  (execute_robot_move)
 - Cleaned up main.py
 - Fully integrated registration into dashboard UI
 - Added displayable feedback for login/registration
 - Added role management for admins, can only be accessed through /docs/admin for role testing

### Decisions:
 - Reached a point where testing each part of the program with each implementation became too time consuming, and so testing parts of the project automatically helps save time here
 - main.py became over crowded with routes for different aspects of the project, so each was moved into its own corresponding file,
 reflects a better separation of concerns principle.
 - Used backend promote/demote routes as backend only, so only admin can promote a users role

### Issues:
 - FIXED: After changing code structure, the automatic tests imported incorrect file names, and so they failed. Fixed by correcting imports.
 - FIXED: FastAPI validation error expecting query instead of Form data, fixed by converting route inputs to str = Form(...)
 - FIXED: Authentication success messages initially constantly stayed on screeen, which was fixed by using request.session.pop()  

### Evidence:
 - Commit: "Added automatic testing through github"
 - Commit: "Refactored routes and added authentication foundations"
 - Commit: "Implemented dashboard auth flow and role management"

## Day 6:

### Completed:
 - Added and automated tests for coverage of authentication, RBAC, command validation and audit logging
 - Implemented Docker Compose for both dashboard application and robot simulator
 - Improved dashboard RBAC behaviour, so that only authenticated users can see past login
 - Refactored dashboard UI into a multi column layout
 - Improved audit logging to include username, battery snapshot and robot status snapshot

### Decisions:
 - Improved and expanded automated testing to allow for less testing time between code changes/improvements/tweaks, especially as project complexity increased.
 - Used mock robot responses in testing to ensure tests remain deterministic and work for CI
 - Reworked dashboard layout to improve usability and readability, making more efficient use of screen space.

### Issues:
 - FIXED: Docker containers could not communicate with the robot simulator becuase of incorrect/outdated environment configuration. Fixed by correcting the environment variable names.
 - FIXED: SQLite database volume mount initially created a folder instead of a file, which was fixed by manually creating the database file before mounting.
 - FIXED: Docker containers also continued to use an outdated static file, which was fixed by building containers without cache.
 - FIXED: Dashboard columns overlapped in some places after redisign. Fixed by adjusting column sizing and overflow handling.


### Evidence:
 - Commit: "Implementation of Docker compose, and Improved audit logging and automated tests"

## Day 7:

### Completed:
 - Added focused code comments
 - Cleaned up remaining architecture inconsistencies and or naming issues
 - Redirected Route directly to dashboard interface on app startup
 - Improved overall code readability
 - Refactored SQLITE database setup to use a dedicated mounted data directory, instead of mounting the database file directly

### Decisions:
 - Added comments to ensure code is maintainable for future works
 - Removed old debugging function that is no longer required, reflects a cleaner deployment state
 - Chose to mount a decicated data directorey through docker compose rather than mounting the file directly, which prevents docker from incorrectly creating a directory in place of the database file

### Issues:
 - FIXED: removed any code made redundant, fixed any incorrectly named imports after Docker/Network debugging phase.
 - FIXED: Docker initially created a directory named 'robot_management.db' on first startup when the file did not already exsist locally. Fixed by restructuring to use a mounted data directory, docker now create a file inside data directory, instead of creating a directory itself.

### Evidence:
 - Commit: "Final code documentation and maintainability improvements"
