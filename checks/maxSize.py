from typings import MaxSizeConfig, ErrorsContext
from typing import List

def maxSizeCheck(
        annotations: List[dict],
        maxSizeConfig: MaxSizeConfig, 
        errors: List[ErrorsContext], 
        errorsContext: ErrorsContext
    ):
    for annotation in annotations:
        width = annotation.get("width")
        height = annotation.get("height")

        try:
            meetsMaxWidth = width <= maxSizeConfig.maxWidth
            meetsMaxHeight = height <= maxSizeConfig.maxHeight
        except TypeError:
            continue

        if not meetsMaxWidth or not meetsMaxHeight: 
            errors.append(ErrorsContext(
                message = f"Annotation {annotation.get('uuid', 'unknown')}: {errorsContext.message}",
                severity = errorsContext.severity
            ))