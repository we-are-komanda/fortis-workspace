# Non-Functional Requirements

## Purpose

This note tracks non-functional requirements for Fortis.

## Initial Categories

- Performance
- Security
- Availability
- Observability
- Audit and logging
- Data retention
- Deployment constraints
- Frontend responsiveness
- Backend reliability
- Model and API rate limits

## Neuraldeep API Rate Limit

Integrations routed through `neuraldeep.api` must target no more than 4 requests per minute and avoid polling more often than every 30 seconds.

