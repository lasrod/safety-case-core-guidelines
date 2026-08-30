# Data Package Coverage

## Data packages by review profile

### Claim review (`claim_review`)

Required data:
- SELECTED_CLAIM
- PARENT
- CHILDREN
- STRATEGY
- DIRECT_CONTEXT
- INHERITED_CONTEXT
- EVIDENCE_PATH

Optional data:
- EVIDENCE_ITEM
- EVIDENCE_BASIS
- PROJECT_GLOSSARY
- STANDARD_LINKS
- CHANGE_HISTORY

### Strategy review (`strategy_review`)

Required data:
- SELECTED_STRATEGY
- PARENT
- CHILDREN
- DIRECT_CONTEXT

Optional data:
- INHERITED_CONTEXT
- EVIDENCE_PATH
- PROJECT_GLOSSARY
- STANDARD_LINKS
- CHANGE_HISTORY

### Evidence review (`evidence_review`)

Required data:
- SELECTED_EVIDENCE
- EVIDENCE_ITEM
- EVIDENCE_BASIS
- PARENT

Optional data:
- DIRECT_CONTEXT
- EVIDENCE_PATH
- PROJECT_GLOSSARY
- STANDARD_LINKS
- CHANGE_HISTORY

### Assumption review (`assumption_review`)

Required data:
- SELECTED_ASSUMPTION
- DIRECT_CONTEXT
- INHERITED_CONTEXT

Optional data:
- PARENT
- CHANGE_HISTORY
- PROJECT_GLOSSARY

### Justification review (`justification_review`)

Required data:
- SELECTED_JUSTIFICATION
- PARENT

Optional data:
- STRATEGY
- EVIDENCE_PATH
- EVIDENCE_ITEM
- EVIDENCE_BASIS
- CHANGE_HISTORY

### Context review (`context_review`)

Required data:
- SELECTED_CONTEXT
- PARENT

Optional data:
- INHERITED_CONTEXT
- PROJECT_GLOSSARY
- STANDARD_LINKS

### Challenge review (`challenge_review`)

Required data:
- SELECTED_CHALLENGE
- PARENT

Optional data:
- CHILDREN
- DIRECT_CONTEXT
- CHANGE_HISTORY

## Review profiles by data package

### SELECTED_CLAIM

- claim_review

### SELECTED_STRATEGY

- strategy_review

### SELECTED_EVIDENCE

- evidence_review

### SELECTED_CONTEXT

- context_review

### SELECTED_ASSUMPTION

- assumption_review

### SELECTED_JUSTIFICATION

- justification_review

### SELECTED_CHALLENGE

- challenge_review

### PARENT

- claim_review
- strategy_review
- evidence_review
- assumption_review
- justification_review
- context_review
- challenge_review

### CHILDREN

- claim_review
- strategy_review
- challenge_review

### DIRECT_CONTEXT

- claim_review
- strategy_review
- evidence_review
- assumption_review
- challenge_review

### INHERITED_CONTEXT

- claim_review
- strategy_review
- assumption_review
- context_review

### STRATEGY

- claim_review
- justification_review

### EVIDENCE_ITEM

- claim_review
- evidence_review
- justification_review

### EVIDENCE_PATH

- claim_review
- strategy_review
- evidence_review
- justification_review

### EVIDENCE_BASIS

- claim_review
- evidence_review
- justification_review

### PROJECT_GLOSSARY

- claim_review
- strategy_review
- evidence_review
- assumption_review
- context_review

### STANDARD_LINKS

- claim_review
- strategy_review
- evidence_review
- context_review

### CHANGE_HISTORY

- claim_review
- strategy_review
- evidence_review
- assumption_review
- justification_review
- challenge_review

### USER_REVIEW_INTENT

- None

## Data packages not used by any review profile

> WARNING: USER_REVIEW_INTENT
