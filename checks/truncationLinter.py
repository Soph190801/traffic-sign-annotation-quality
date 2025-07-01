import requests
from PIL import Image
from io import BytesIO
from typings import TruncationConfig, ErrorsContext
from typing import List, Tuple

def getImageSize(url: str) -> Tuple[float, float]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        return image.size
    except Exception as e:
        raise RuntimeError(f"Failed to get image size from {url}: {e}") from e


def isCloseToBorders(
        top: float, 
        left: float, 
        width: float, 
        height: float, 
        image_width: float, 
        image_height: float, 
        threshold: int
    ) -> bool:
    topIsTruncated = top <= threshold
    rightIsTruncated = image_width - left - width <= threshold
    bottomIsTruncated = image_height - top - height <= threshold
    leftIsTruncated = left <= threshold

    return any([
        topIsTruncated,
        rightIsTruncated,
        bottomIsTruncated,
        leftIsTruncated
    ])

def truncationCheck(
        params: dict, 
        annotations: List[dict], 
        config: TruncationConfig, 
        errors: List[ErrorsContext], 
        errorContext: ErrorsContext
    ):
    try:
        image_url = params.get("attachment")
        if not image_url:
            return

        image_width, image_height = getImageSize(image_url)

        for annotation in annotations or []:
            truncationValue = annotation.get("attributes", {}).get(config.attributeName)
            top = annotation.get("top")
            left = annotation.get("left")
            width = annotation.get("width")
            height = annotation.get("height")

            if any(value is None for value in [truncationValue, top, left, width, height]):
                continue

            isTruncated = isCloseToBorders(
                top,
                left,
                width,
                height,
                image_width,
                image_height,
                config.threshold
            )

            hasTruncationValue = truncationValue in config.truncationValues

            if hasTruncationValue and not isTruncated:
                errors.append(ErrorsContext(
                    message=f"Annotation {annotation.get('uuid', 'unknown')}: Has truncation values but is not close to the edges",
                    severity=errorContext.severity
                ))

            if not hasTruncationValue and isTruncated:
                errors.append(ErrorsContext(
                    message=f"Annotation {annotation.get('uuid', 'unknown')}: Doesn't have truncation values but is close to the edges",
                    severity=errorContext.severity
                ))
    except Exception as e:
        errors.append(ErrorsContext(
            message=f"Exception in truncationCheck: {e}",
            severity="error"
        ))

