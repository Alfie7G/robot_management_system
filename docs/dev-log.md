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
 -  Chose Jinja + HTMX frontend over something like react due to its reduceded complexity, which allows more focus on backend reliability, architecture and API integration.
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
- Intergrated SQlit database
- Completed the dedicated database layer, e.g. 'database.py', 'models.py'
- Implemented 'CommandLog' database which logs; command type, target coords, the result/success, and the utc timestamp of the action
- Cleaned up move robotapi and dashboard routes, including the changes made to log actions

### Decisions:
 - Used sqlite because its lightweight and doesnt require an external database server
 - timestamps stored in UTC to ensure consitency, avoiding timezone related issues

### Issues:
 - FIXED: Database tables were created but initially empty. Discovered that previously, the dashboard move route didnt call the correct robot_move_to funciton, which was where the moves get logged,
 now it calls the correct function that both moves and logs the movements of the robot.
 -UNFIXED: Currently the database setup only logs movement actions, the robots status, battery etc etc, are not logged, additional logging is required, which there was not time for today

### Evidence:
 - Commit: "Implemented action logger"

 
## Day 3:

### Completed:

### Decisions:


### Issues:


### Evidence: