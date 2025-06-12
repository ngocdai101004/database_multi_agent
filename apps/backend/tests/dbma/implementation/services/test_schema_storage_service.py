import pytest
from pathlib import Path
from dbma.implementation.services.schema_storage_service import SchemaStorageService
from dbma.native.domain.db_schema import DBSchema
from dbma.dependencies.container import Container

class TestSchemaStorageService:


    @pytest.fixture
    def schema_storage_service(self, container: Container):
        return container.schema_storage_service()

    def test_load_db_document(self, schema_storage_service: SchemaStorageService):
        """Test loading of schema descriptions"""
        # Arrange
        
        print("List schemas: ", schema_storage_service.list_schemas)
        print("DB description: ", schema_storage_service.db_description)
        # Assert
        assert len(schema_storage_service.list_schemas) > 0

    def test_get_schema_valid(self, schema_storage_service: SchemaStorageService):
        """Test getting schema with valid schema name"""
        # Arrange
        print("List schemas: ", schema_storage_service.list_schemas)
        schema_name = "california_schools"
        
        # Act
        schema = schema_storage_service.get_schema(schema_name)
        print("Schema: ", schema)
        # Assert
        assert schema is not None

    def test_get_schema_invalid(self, schema_storage_service: SchemaStorageService):
        """Test getting schema with invalid schema name"""
        # Arrange
        invalid_schema_name = "invalid"
        expected_error_message = f"Schema {invalid_schema_name} is not valid"
        
        # Act & Assert
        with pytest.raises(ValueError, match=expected_error_message):
            schema_storage_service.get_schema(invalid_schema_name)


    def test_get_db_description(self, schema_storage_service: SchemaStorageService):
        """Test getting database description"""
        
        # Act
        description = schema_storage_service.get_db_description()
        
        # Assert
        assert description is not None