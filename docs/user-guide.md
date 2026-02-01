# Clinical Intelligence Agent – User Guide

## 1. Purpose

The Clinical Intelligence Agent is an AI-powered assistant designed to answer questions about medical guidelines and insurance coverage using official NICE documents and predefined insurance plan rules.
The system provides grounded responses based only on retrieved documents and does not generate free-form medical advice.

## 2. Intended Users

This system is intended for:

- End users seeking information about medical guidelines and insurance coverage

- Insurance support staff

- Internal reviewers and administrators

- Policy and compliance teams

It is not intended for direct patient diagnosis or emergency medical use.

## 3. Supported Question Types

Users can ask questions related to:

- Insurance coverage

    - “Is insulin covered for Type 2 diabetes under the Gold plan?”

    - “Does the Silver plan cover COPD medication?”

- Medical guideline clarification

    - “What do NICE guidelines recommend for COPD management?”

    - “What is the standard treatment for hypertension according to NICE?”

- Policy-related queries

    - “What are the eligibility rules for diabetes medication coverage?”

## 4. How to Ask Questions

Users should:

- Ask clear and specific questions

- Mention the medical condition and insurance plan when relevant

- Avoid vague or incomplete queries

Recommended format:

- Include condition: Type 2 diabetes, COPD, asthma

- Include plan: Gold, Silver or Bronze

- Ask one question at a time

Good example:

- Is insulin covered for Type 2 diabetes under the Gold plan?

Poor example:

- Is this covered?

## 5. Example Interaction

User:
- Is insulin covered for Type 2 diabetes under the Gold plan?

System:
- According to NICE guideline section 3.2, insulin is covered for Type 2 diabetes patients under the Gold insurance plan.

## 6. Clarification Requests

If a user question is ambiguous or missing key information, the system will request clarification.

Example:

- Please specify the medical condition and insurance plan so I can provide an accurate answer.

Common causes for clarification:

- Missing insurance plan

- Unclear medical condition

- Broad or multi-part questions

## 7. Escalation to Human Review

The system escalates a query for human review when:

- No relevant documents are retrieved

- The confidence score is below a defined threshold

- The question falls outside supported topics

- The system detects potential safety risk

Escalated responses are flagged and require manual review before a final decision is made.

## 8. Limitations

The Clinical Intelligence Agent has the following limitations:

- It only answers based on uploaded NICE guideline documents and insurance rules

- It does not provide medical diagnosis or treatment advice

- It cannot access external or real-time medical databases

- Results depend on the quality and completeness of the ingested documents

## 9. Safety and Compliance

- The system does not replace medical professionals

- All interactions are logged for audit and quality assurance

- Sensitive health data should not be entered unless permitted by policy

- Human-in-the-loop review is used for uncertain or high-risk queries

## 10. Error Handling

Possible error scenarios:

- Invalid input:
User submits an empty or malformed question

- No documents found:
System returns a fallback response

- System failure:
A generic error message is displayed and the event is logged

Example error message:

- An internal error occurred while processing your request. Please try again later.

## 11. Best Practices

- Ask specific and focused questions

- Include medical condition and insurance plan

- Rephrase unclear queries

- Review escalated answers manually

- Do not use the system for urgent medical decisions

## 12. Out of Scope

The system does NOT support:

- Emergency medical advice

- Personalized treatment recommendations

- Legal decisions

- Diagnosing diseases

- Prescribing medication

## 13. Versioning

This user guide applies to the current version of the Clinical Intelligence Agent and should be updated whenever:

- guideline documents change

- insurance rules are updated

- system logic is modified