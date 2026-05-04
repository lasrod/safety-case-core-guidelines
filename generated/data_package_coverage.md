# Data Package Coverage

## Data packages by review profile

### Claim wording review (`claim_wording_review`)

Required data:
- SEL
- DIRECT_CONTEXT

Optional data:
- PARENT
- CHILDREN
- INHERITED_CONTEXT
- PROJECT_GLOSSARY

### Claim context review (`claim_context_review`)

Required data:
- SEL
- DIRECT_CONTEXT
- INHERITED_CONTEXT

Optional data:
- PARENT
- PROJECT_GLOSSARY
- STANDARD_LINKS

### Decomposition review (`decomposition_review`)

Required data:
- SEL
- PARENT
- CHILDREN
- STRATEGY
- DIRECT_CONTEXT
- INHERITED_CONTEXT

Optional data:
- EVIDENCE_PATH
- PROJECT_GLOSSARY

### Strategy review (`strategy_review`)

Required data:
- SEL
- PARENT
- CHILDREN
- DIRECT_CONTEXT

Optional data:
- INHERITED_CONTEXT
- PROJECT_GLOSSARY
- STANDARD_LINKS

### Evidence item review (`evidence_item_review`)

Required data:
- SEL
- EVIDENCE_ITEM

Optional data:
- EVIDENCE_BASIS
- CHANGE_HISTORY

### Evidence path review (`evidence_path_review`)

Required data:
- SEL
- EVIDENCE_PATH
- CHILDREN

Optional data:
- STRATEGY
- EVIDENCE_ITEM
- EVIDENCE_BASIS
- DIRECT_CONTEXT

### Assumption review (`assumption_review`)

Required data:
- SEL
- DIRECT_CONTEXT
- INHERITED_CONTEXT

Optional data:
- PARENT

### Justification review (`justification_review`)

Required data:
- SEL
- PARENT

Optional data:
- STRATEGY
- EVIDENCE_PATH
- EVIDENCE_ITEM
- CHANGE_HISTORY

## Review profiles by data package

### SEL

- claim_wording_review
- claim_context_review
- decomposition_review
- strategy_review
- evidence_item_review
- evidence_path_review
- assumption_review
- justification_review

### PARENT

- claim_wording_review
- claim_context_review
- decomposition_review
- strategy_review
- assumption_review
- justification_review

### CHILDREN

- claim_wording_review
- decomposition_review
- strategy_review
- evidence_path_review

### DIRECT_CONTEXT

- claim_wording_review
- claim_context_review
- decomposition_review
- strategy_review
- evidence_path_review
- assumption_review

### INHERITED_CONTEXT

- claim_wording_review
- claim_context_review
- decomposition_review
- strategy_review
- assumption_review

### STRATEGY

- decomposition_review
- evidence_path_review
- justification_review

### EVIDENCE_ITEM

- evidence_item_review
- evidence_path_review
- justification_review

### EVIDENCE_PATH

- decomposition_review
- evidence_path_review
- justification_review

### EVIDENCE_BASIS

- evidence_item_review
- evidence_path_review

### PROJECT_GLOSSARY

- claim_wording_review
- claim_context_review
- decomposition_review
- strategy_review

### STANDARD_LINKS

- claim_context_review
- strategy_review

### CHANGE_HISTORY

- evidence_item_review
- justification_review

### USER_REVIEW_INTENT

- None

## Data packages not used by any review profile

> WARNING: USER_REVIEW_INTENT
