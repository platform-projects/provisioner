CONST_GIGABYTE = 1000000000
CONST_DEFAULT_SPACE_STORAGE = 1 * CONST_GIGABYTE
CONST_DEFAULT_SPACE_MEMORY = int(.5 * CONST_GIGABYTE)

business_builder_query = """{
    "SpaceID": "{space_name}",
    "Sort": { "Column": "Title", "isDescending": false },
    "HideEmptyPackages": false,
    "PackageSelectionAllowed": true,
    "currentPackage": -1,
    "filterData": [],
    "searchData": [],
    "typeOrder": [
        { "EntityType": "CubeSource",             "index": 0 },
        { "EntityType": "ResponsibilityScenario", "index": 1 },
        { "EntityType": "Business Semantic",      "index": 2 },
        { "EntityType": "MasterDataSource",       "index": 3 },
        { "EntityType": "KPI Model",              "index": 4 },
        { "EntityType": "Package",                "index": 5 },
        { "EntityType": "Perspective",            "index": 6 }
    ]
}"""

user_action = """[
  {
    "userName": "#UNAME",
    "operator": "#ACTION",
    "parameters": [
      { "name": "FIRST_NAME",    "value": "#FIRST" },
      { "name": "LAST_NAME",     "value": "#LAST" },
      { "name": "DISPLAY_NAME",  "value": "#DISPLAY" },
      { "name": "EMAIL",         "value": "#EMAIL" },
      { "name": "MANAGER",       "value": "#MANAGER" },
      { "name": "IS_CONCURRENT", "value": "0" }
    ],
    "metadata": {
      "samlUserMapping": [
        {
          "userName": "#UNAME",
          "provider": "ORCAHANAGWIDP",
          "samlUserName": "#EMAIL"
        }
      ],
      "isSamlEnabled": true
    },
    "roles": "PROFILE:sap.epm:Application_Creator;PROFILE:sap.epm:BI_Admin;PROFILE:sap.epm:BI_Content_Creator",
    "setUserConcurrent": false
  }
]"""
