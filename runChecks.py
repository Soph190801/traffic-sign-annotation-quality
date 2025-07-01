from taskRetrieval import getTaskInfo 
from checks.truncationLinter import truncationCheck
from checks.attributeConditions import attributesConditionCheck
from checks.maxSize import maxSizeCheck
from typings import TruncationConfig, AttributeConditionConfig, ErrorsContext, MaxSizeConfig
from typing import List, Tuple

def runChecks(task: dict) -> Tuple[str, List[ErrorsContext]]:
    try: 
        errors: List[ErrorsContext] = []
        task_id, params, annotations = getTaskInfo(task)

        # This check raises an error if a box is near the edges but does not have  a truncation value
        # or if the box is not near the edges yet has a truncation value assigned
        truncationConfig = TruncationConfig(
            threshold = 1,
            attributeName = "truncation",
            truncationValues = ["25%", "50%", "75%", "100%"]
        )

        errorContext = ErrorsContext(
            severity = "error"
        )

        truncationCheck(params, annotations, truncationConfig, errors, errorContext)

        # This check issues a warning if a construction sign does not have its background color set to orange
        constructionSignConfig = AttributeConditionConfig(
            attributes = {"background_color": "orange"},
            labels = ["construction_sign"]
        )

        errorContext = ErrorsContext(
            message = "Construction signs are usually orange, double check the background color",
            severity = "warning"
        )

        attributesConditionCheck(annotations, constructionSignConfig, errors, errorContext)

        # This check raises an error if a non_visible_face does not have its background color set to 'not_applicable'
        nonVisibleFaceConfig = AttributeConditionConfig(
            attributes = {"background_color": "not_applicable"},
            labels = ["non_visible_face"]
        )

        errorContext = ErrorsContext(
            message = "non_visible_face should always have the background color set as not_applicable",
            severity = "error"
        )

        attributesConditionCheck(annotations, nonVisibleFaceConfig, errors, errorContext)

        # This check raises an error if a label other than 'non_visible_face' has its background color set to 'not_applicable'
        notApplicableConfig = AttributeConditionConfig(
            attributes = {"background_color": "not_applicable"},
            labels = [
                "traffic_control_sign",
                "construction_sign",
                "information_sign",
                "policy_sign"
            ],
            shouldMatchAttributes = False
        )

        errorContext = ErrorsContext(
            message = "Only non_visible_face should have the background color set as not_applicable",
            severity = "error"
        )

        attributesConditionCheck(annotations, notApplicableConfig, errors, errorContext)

    # This check raises an error if a traffic_control_sign does not have its background color set to 'other'
        trafficSignConfig = AttributeConditionConfig(
            attributes = {"background_color": "other"},
            labels = ["traffic_control_sign"]
        )

        errorContext = ErrorsContext(
            message = "Traffic lights should have background color set as other, double check if this is a traffic light",
            severity = "warning"
        )

        attributesConditionCheck(annotations, trafficSignConfig, errors, errorContext)

        # This check raises an error if a box exceeds 500 pixels in either height or width
        maxSizeConfig = MaxSizeConfig(
            maxWidth = 500,
            maxHeight = 500
        )

        errorContext = ErrorsContext(
            message = "Boxes should not exceed 500px in width or height",
            severity = "error"
        )

        maxSizeCheck(annotations, maxSizeConfig, errors, errorContext)

        return task_id, errors
    except ValueError as ve:
        task_id = task.get("task_id", "unknown")
        return task_id, [ErrorsContext(severity="error", message=str(ve))]
