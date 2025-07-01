from typings import AttributeConditionConfig, ErrorsContext 
from typing import List
from typing import Optional

def attributesConditionCheck(
        annotations: List[dict], 
        config: AttributeConditionConfig, 
        errors: List[ErrorsContext], 
        errorContext: ErrorsContext
    ):
    for annotation in annotations:
        label = annotation.get("label")
        if label not in config.labels:
            continue

        matchesCondtion: List[bool] = []
        
        for attributeName, attributeValue in config.attributes.items():
            currentValue = annotation.get("attributes", {}).get(attributeName)
            matchesCondtion.append(currentValue == attributeValue)

        failsCheck = not any(matchesCondtion) if config.shouldMatchAttributes else any(matchesCondtion)

        if failsCheck:
            errors.append(ErrorsContext(
                message = f"Annotation {annotation.get('uuid', 'unknown')}: {errorContext.message}",
                severity = errorContext.severity
            ))
            

            