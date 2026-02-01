# API Reference

This document describes the public API endpoints for the Clinical Intelligence Agent.

## POST /ask

### Description  
Submits a user question to the Clinical Intelligence Agent.  
The system retrieves relevant medical guideline documents and insurance rules, applies agent decision logic, and returns a user-facing message.

Internal confidence scoring and escalation decisions are logged but are not exposed in the API response.

### Request Body

```json
{
  "user_id": 1,
  "question": "Is insulin covered for Type 2 diabetes?"
}
```
### Fields
`user_id` (integer, required): Identifier of the user submitting the query

`question` (string, required): Natural language question

## Response Types
The /ask endpoint may return different responses depending on system behavior.

### 1. Successful Answer
Returned when relevant documents are retrieved and the system confidence is above the escalation threshold.
```json
{
  "message": "According to NICE guideline section 3.2, insulin is covered under your plan."
}
```
### 2. Clarification Required
Returned when the user question is ambiguous or missing required information.
```json
{
  "message": "Could you please clarify which medication, treatment, or condition you are asking about?"
}
```
### 3. Escalation Response
Returned when:

- No relevant documents are found, or

- The system confidence is below the defined threshold.
```json
{
  "message": "I could not find relevant medical guidelines. This will be reviewed by a human agent."
}
```
or
```json
{
  "message": "Your request requires review by a human specialist. Please wait for confirmation."
}
```
### 4. Error Response (User Not Found)
Returned when the provided user_id does not exist.
```json
{
  "message": "User not found"
}
```
## GET /logs

### Description
- Returns recent query logs for monitoring and audit purposes.
- This endpoint is intended for internal or administrative use only.

### Response
```json
[
  {
    "id": 15,
    "user_id": 1,
    "query": "Is insulin covered for Type 2 diabetes?",
    "answer": "According to NICE guideline section 3.2, insulin is covered under your plan.",
    "confidence": 0.87,
    "action": "answer",
    "created_at": "2026-01-30T14:22:10.123456"
  }
]
```
### Fields
- `id`: Log entry identifier

- `user_id`: User identifier

- `query`: Original user question

- `answer`: Generated response

- `confidence`: Internal confidence score

- `action`: System decision (answer, clarify, or escalate)

- `created_at`: Timestamp in ISO 8601 format

## Error Handling
### 500 Internal Server Error

Returned when an unexpected system failure occurs.
```json
{
  "detail": "Internal Server Error"
}
```
## Security and Access Notes
- The /logs endpoint should be restricted to authorized users

- All queries and responses are logged for audit and quality assurance

- Sensitive personal health data should not be submitted unless permitted by policy

## Internal Behavior Notes
- Confidence scores and agent decisions are stored internally in the database

- The /ask endpoint returns only a user-facing message

- Human-in-the-loop escalation is triggered for low-confidence or unsafe queries

## Versioning
This API reference applies to the current version of the Clinical Intelligence Agent API.
Documentation must be updated when endpoint behavior or response formats change.