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
 - Confirmed backend works so far
 
### Decisions:


### Issues:
 - FIXED/CONFIRMED: Robot wouldnt move long distances, and would change status to 'STUCK', was due to map constrictions, not backend error

### Evidence:
 - Commit: "Implemented API integration"