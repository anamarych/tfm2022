# Azure Provider source and version being used
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.13.0"
    }
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {}
}

# Create a resource group
resource "azurerm_resource_group" "rg" {
  name     = "IoTResources"
  location = "westeurope"
}

# Create IoTHub
resource "azurerm_iothub" "iothub" {
  name                = "tfmIoTHub"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  sku {
    name     = "F1"
    capacity = "1"
  }
}

# IoT Hub device creation is not yet supported, manually add the devices needed

# Create CosmosDB account
resource "azurerm_cosmosdb_account" "db" {
  name                = "tfmcosmosdb"
  location            = "switzerlandnorth"
  resource_group_name = azurerm_resource_group.rg.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"
  
  consistency_policy {
    consistency_level       = "Session"
    max_interval_in_seconds = 5
    max_staleness_prefix    = 100
  }
  
  geo_location {
    location          = "switzerlandnorth"
    failover_priority = 0
  }
}

# Create CosmosDB database
resource "azurerm_cosmosdb_sql_database" "db" {
  name                = "siotcom"
  resource_group_name = azurerm_cosmosdb_account.db.resource_group_name
  account_name        = azurerm_cosmosdb_account.db.name
}

# Create CosmosDB container
resource "azurerm_cosmosdb_sql_container" "container" {
  name                  = "sensor"
  resource_group_name   = azurerm_cosmosdb_account.db.resource_group_name
  account_name          = azurerm_cosmosdb_account.db.name
  database_name         = azurerm_cosmosdb_sql_database.db.name
  partition_key_path    = "/id"
  throughput            = 400
  
   indexing_policy {
    indexing_mode = "consistent"
	
	included_path {
		path = "/*"
		}
	excluded_path {
		path = "/\"_etag\"/?"
		}
	
	}
}

# Create Stream Analytics job
resource "azurerm_stream_analytics_job" "stream" {
  name                                     = "tfmstream"
  resource_group_name                      = azurerm_resource_group.rg.name
  location                                 = azurerm_resource_group.rg.location
  compatibility_level                      = "1.2"
  data_locale                              = "en-US"
  events_late_arrival_max_delay_in_seconds = 5
  events_out_of_order_max_delay_in_seconds = 0
  events_out_of_order_policy               = "Adjust"
  output_error_policy                      = "Stop"
  streaming_units                          = 3

  transformation_query = <<QUERY
    SELECT
    GetMetadataPropertyValue(datastreaminput, 'EventId') AS id,
    datastreaminput.time,
    datastreaminput.class,
    datastreaminput.hub,
    datastreaminput.node,
    datastreaminput.data
	INTO
    [cosmosdboutput]
	FROM
    [datastreaminput]

	SELECT
    datastreaminput.time,
    datastreaminput.class,
    datastreaminput.hub,
    datastreaminput.node,
    datastreaminput.data.*
	INTO
    [powerbioutput]
	FROM
    [datastreaminput]

QUERY

}

# Stream analytics input
resource "azurerm_stream_analytics_stream_input_iothub" "datastreaminput" {
  name                         = "datastreaminput"
  stream_analytics_job_name    = azurerm_stream_analytics_job.stream.name
  resource_group_name          = azurerm_stream_analytics_job.stream.resource_group_name
  endpoint                     = "messages/events"
  eventhub_consumer_group_name = "messageconsumer"
  iothub_namespace             = azurerm_iothub.iothub.name
  shared_access_policy_key     = azurerm_iothub.iothub.shared_access_policy[0].primary_key
  shared_access_policy_name    = "iothubowner"

  serialization {
    type     = "Json"
    encoding = "UTF8"
  }
}

#Stream Analytics output to CosmosDB
resource "azurerm_stream_analytics_output_cosmosdb" "cosmosdboutput" {
  name                     = "cosmosdboutput"
  stream_analytics_job_id  = azurerm_stream_analytics_job.stream.id
  cosmosdb_account_key     = azurerm_cosmosdb_account.db.primary_key
 cosmosdb_sql_database_id = azurerm_cosmosdb_sql_database.db.id
 container_name           = azurerm_cosmosdb_sql_container.container.name
 document_id              = "_1234567834567845e"
}

#Stream Analytics output to powerbi not supported resource type "azurerm_stream_analytics_output_powerbi"
resource "azurerm_stream_analytics_output_powerbi" "powerbioutput" {
 name                    = "powerbioutput"
 stream_analytics_job_id = azurerm_stream_analytics_job.stream.id
 dataset                 = "tfm"
 table                   = "sensordata"
 group_id                = "00000000-0000-0000-0000-000000000000"
 group_name              = "some-group-name"
}
