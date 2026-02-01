# Limitations and Risks

## Knowledge Scope
The Clinical Intelligence Agent only answers questions based on:
- Uploaded NICE guideline documents
- Predefined insurance plan rules (Gold, Silver, and Bronze)

It does not access external or real-time medical databases.

## Hallucination Risk
Although the system restricts responses to retrieved documents, there is still a risk of:
- Partial or incomplete answers
- Misinterpretation of guideline text
- Incorrect summarization

Fallback responses and human review are used to mitigate this risk.

## Medical Safety
The system:
- Does not provide diagnosis
- Does not prescribe treatment
- Does not replace medical professionals
- Is not suitable for emergency situations

## Data Quality Dependence
System accuracy depends on:
- Completeness of guideline documents
- Quality of PDF extraction
- Proper chunking and embedding generation

Errors in ingestion may lead to incorrect answers.

## Bias and Coverage Gaps
- Guidelines may not cover all medical conditions
- Insurance rules may not reflect real-world exceptions
- Some queries may fall outside supported scope

## Privacy and Compliance
- All interactions are logged for audit purposes
- Sensitive personal health information should not be entered
- Logs must be handled according to data protection policies

## Human-in-the-Loop Controls
Queries are escalated when:
- Confidence is below threshold
- Retrieval fails
- Safety risk is detected
- Question is ambiguous

Human reviewers must verify responses before final decisions.

## System Misuse
The system should not be used for:
- Legal decisions
- Clinical diagnosis
- Patient treatment planning
- Emergency response

## Monitoring and Maintenance
Regular monitoring is required for:
- Retrieval quality
- Hallucination incidents
- User feedback
- Document updates

## Disclaimer
The Clinical Intelligence Agent is an informational support tool and does not constitute medical or legal advice.