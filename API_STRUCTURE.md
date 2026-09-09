# CivicShield API Structure

## Incidents
- GET /incidents/
- POST /incidents/
- GET /incidents/{incident_id}
- PUT /incidents/{incident_id}

## Safety Zones
- POST /incidents/zones
- GET /incidents/zones
- PUT /incidents/zones/{zone_id}

## Restrictions
- POST /incidents/restrictions
- GET /incidents/restrictions
- PUT /incidents/restrictions/{restriction_id}

## Restriction Services
- POST /incidents/restriction-services
- GET /incidents/restriction-services

## Alerts
- POST /incidents/alerts
- GET /incidents/alerts

## Emergency Units
- POST /incidents/emergency-units
- GET /incidents/emergency-units

## Worker Locations
- POST /incidents/worker-locations
- GET /incidents/worker-locations

## Worker Safety
- POST /incidents/worker-check

## Citizen Reports
- POST /incidents/citizen-reports
- GET /incidents/citizen-reports

## Audit Logs
- POST /incidents/audit-logs
- GET /incidents/audit-logs