# import pytest
# from pathlib import Path
# from dbma.implementation.services.schema_storage_service import SchemaStorageService
# from dbma.native.domain.db_schema import DBSchema

# class TestSchemaStorageService:
#     @pytest.fixture
#     def test_data_dir(self):
#         return Path(__file__).parent / "test_data"

#     @pytest.fixture
#     def schema_storage_service(self, test_data_dir):
#         return SchemaStorageService(test_data_dir)

#     def test_load_db_document(self, schema_storage_service: SchemaStorageService):
#         """Test loading of schema descriptions"""
#         # Arrange
#         expected_schemas = ["sales", "inventory", "hr", "finance"]
        
#         print("List schemas: ", schema_storage_service.list_schemas)
#         print("DB description: ", schema_storage_service.db_description)
#         # Assert
#         assert set(schema_storage_service.list_schemas) == set(expected_schemas)
#         assert len(schema_storage_service.db_description) == len(expected_schemas)
#         for schema in expected_schemas:
#             assert schema in schema_storage_service.db_description
#             assert isinstance(schema_storage_service.db_description[schema], str)
#             assert len(schema_storage_service.db_description[schema]) > 0

#     def test_get_schema_valid(self, schema_storage_service: SchemaStorageService):
#         """Test getting schema with valid schema name"""
#         # Arrange
#         schema_name = "hr"
        
#         # Act
#         schema = schema_storage_service.get_schema(schema_name)
#         print("Schema: ", schema)
#         # Assert
#         assert isinstance(schema, DBSchema)
#         assert schema.schema_name == schema_name
#         assert isinstance(schema.schema_detail, str)
#         assert len(schema.schema_detail) > 0
#         assert isinstance(schema.schema_tables, list)
#         assert len(schema.schema_tables) > 0

#     def test_get_schema_invalid(self, schema_storage_service: SchemaStorageService):
#         """Test getting schema with invalid schema name"""
#         # Arrange
#         invalid_schema_name = "invalid"
#         expected_error_message = f"Schema {invalid_schema_name} is not valid"
        
#         # Act & Assert
#         with pytest.raises(ValueError, match=expected_error_message):
#             schema_storage_service.get_schema(invalid_schema_name)


#     def test_get_db_description(self, schema_storage_service: SchemaStorageService):
#         """Test getting database description"""
#         # Arrange
#         expected_schemas = schema_storage_service.list_schemas
        
#         # Act
#         description = schema_storage_service.get_db_description()
        
#         # Assert
#         assert isinstance(description, str)
#         assert len(description) > 0
#         for schema in expected_schemas:
#             assert schema in description

#     def test_schema_content_validation(self, schema_storage_service: SchemaStorageService):
#         """Test validation of schema content"""
#         # Arrange
#         schema_name = "hr"
        
#         # Act
#         schema: DBSchema = schema_storage_service.get_schema(schema_name)
        
#         # Assert
#         assert "CREATE TABLE" in schema.schema_detail.upper()
#         assert len(schema.schema_tables) > 0
#         for table_name in schema.schema_tables:
#             assert table_name in schema.schema_detail 