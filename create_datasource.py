import yaml
from great_expectations.data_context import DataContext

context = DataContext()

datasource_config = {
    "name": "sales_filesystem",
    "class_name": "Datasource",
    "execution_engine": {
        "class_name": "PandasExecutionEngine",
    },
    "data_connectors": {
        "default_runtime_data_connector_name": {
            "class_name": "RuntimeDataConnector",
            "batch_identifiers": ["default_identifier_name"],
        }
    },
}

print(context.test_yaml_config(yaml.dump(datasource_config)))

context.add_datasource(**datasource_config)
