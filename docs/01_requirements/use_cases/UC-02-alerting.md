# UC-02 Alerting / Incident Handling

## Primary Actor
Farm Operator

## Preconditions
- Telemetry ingestion active
- Rules configured

## Main Flow
1. Telemetry violates rule
2. Incident is created
3. Operator is notified via dashboard
4. Operator acknowledges incident
5. Operator resolves incident

## Postconditions
- Incident state is updated
- Audit trail preserved

## Mapping
- rules → incidents
- Sequence: Telemetry → Incident
- Tests: incident lifecycle tests
