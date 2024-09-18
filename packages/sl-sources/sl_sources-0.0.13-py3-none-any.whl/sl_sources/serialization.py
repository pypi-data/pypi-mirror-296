import json
import os
from typing import List

from .models import ENTITY_TYPES


def serialize_entity_array(
    entities: List[ENTITY_TYPES], filename: str, dir="serialization_results"
):
    # Check if directory exists and create it if it doesn't
    os.makedirs(dir, exist_ok=True)

    # Construct the full file path
    file_path = os.path.join(dir, filename)

    entity_dicts = [entity.model_dump() for entity in entities]
    with open(file_path, "w") as f:
        json.dump(entity_dicts, f, indent=2)
