import pytest

from nodestream.schema.schema import (
    Cardinality,
    GraphObjectShape,
    GraphObjectType,
    GraphSchema,
    KnownTypeMarker,
    PresentRelationship,
    PropertyMetadata,
    PropertyMetadataSet,
    PropertyType,
)


@pytest.fixture
def basic_schema():
    return GraphSchema(
        [
            GraphObjectShape(
                GraphObjectType.NODE,
                KnownTypeMarker("Person"),
                PropertyMetadataSet(
                    {
                        "name": PropertyMetadata("name", PropertyType.STRING),
                        "age": PropertyMetadata("age", PropertyType.INTEGER),
                    }
                ),
            ),
            GraphObjectShape(
                GraphObjectType.NODE,
                KnownTypeMarker("Organization"),
                PropertyMetadataSet(
                    {
                        "name": PropertyMetadata("name", PropertyType.STRING),
                        "industry": PropertyMetadata("industry", PropertyType.STRING),
                    }
                ),
            ),
            GraphObjectShape(
                GraphObjectType.RELATIONSHIP,
                KnownTypeMarker("BEST_FRIEND_OF"),
                PropertyMetadataSet(
                    {
                        "since": PropertyMetadata("since", PropertyType.DATETIME),
                    }
                ),
            ),
            GraphObjectShape(
                GraphObjectType.RELATIONSHIP,
                KnownTypeMarker("HAS_EMPLOYEE"),
                PropertyMetadataSet(
                    {
                        "since": PropertyMetadata("since", PropertyType.DATETIME),
                    }
                ),
            ),
        ],
        [
            PresentRelationship(
                KnownTypeMarker("Person"),
                KnownTypeMarker("Person"),
                KnownTypeMarker("BEST_FRIEND_OF"),
                from_side_cardinality=Cardinality.SINGLE,
                to_side_cardinality=Cardinality.MANY,
            ),
            PresentRelationship(
                KnownTypeMarker("Organization"),
                KnownTypeMarker("Person"),
                KnownTypeMarker("HAS_EMPLOYEE"),
                from_side_cardinality=Cardinality.MANY,
                to_side_cardinality=Cardinality.MANY,
            ),
        ],
    )
