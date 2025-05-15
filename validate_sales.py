from great_expectations.data_context import DataContext

context = DataContext()

batch = {
    "datasource_name": "sales_filesystem",
    "data_connector_name": "default_runtime_data_connector_name",
    "data_asset_name": "sales_data",
    "runtime_parameters": {"path": "./data/sales.csv"},
    "batch_identifiers": {"default_identifier_name": "default_id"},
}

results = context.run_validation_operator(
    "action_list_operator",
    assets_to_validate=[{"batch_kwargs": batch,
                         "expectation_suite_name": "sales_suite"}],
)

if not results["success"]:
    raise ValueError("Validation failed")
else:
    print("Validation passed")
