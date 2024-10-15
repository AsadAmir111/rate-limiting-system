# Rate Limiting System
## Local Setup
- Run `docker-compose up` to start a container running rate_limiting_service and another running Redis.
- MAX_TOKENS and SECONDS_PER_TOKEN are environment variables that can be set inside the docker-compose file to configure the rate limit.
- Make a `GET` request at `http://localhost:5000/` with a User-Token in the headers.
- Example: `curl -H "User-Token: user1234" http://localhost:5000/`
