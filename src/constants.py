CONST_GIGABYTE = 1000000000
CONST_DEFAULT_SPACE_STORAGE = 1 * CONST_GIGABYTE
CONST_DEFAULT_SPACE_MEMORY = int(.5 * CONST_GIGABYTE)

CONST_SPACE_NAME = 0
CONST_LABEL = 1
CONST_DISK = 2
CONST_MEMORY = 3
CONST_TEMPLATE = 4
CONST_FORCE = 5
CONST_USERS = 6

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

default_space_definition = {
    "spaceDefinition": {
        "version": "1.0.4",
        "label": "",
        "assignedStorage": 1000000000,
        "assignedRam": 500000000,
        "priority": 5,
        "auditing": {
            "dppRead": {
                "retentionPeriod": 7,
                "isAuditPolicyActive": False
            },
            "dppChange": {
                "retentionPeriod": 7,
                "isAuditPolicyActive": False
            }
        },
        "allowConsumption": False,
        "enableDataLake": False,
        "members": [],
        "dbusers": {},
        "hdicontainers": {},
        "workloadClass": {
            "totalStatementMemoryLimit": {
                "value": None,
                "unit": "Gigabyte"
            },
            "totalStatementThreadLimit": {
                "value": None,
                "unit": "Counter"
            }
        },
        "workloadType": "default"
    }
}

# s = string
# e = epoch date
# g = gigabyte (=#/1GB)

templates = {
  "users" : {
    "fields" : {
      "user_name"      : { "path" : "userName",                   "format" : "25s", "heading" : "User" },
      "user_email"     : { "path" : "parameters.EMAIL",           "format" : "35s", "heading" : "Email" },
      "user_lastLogin" : { "path" : "parameters.LAST_LOGIN_DATE", "format" : "10e", "heading" : "Last Login" },
      "role_name"      : { "path" : "roleName",                   "format" : "30s", "heading" : "Role" }
    },
    "rows" : [
      { "type" : "row", "layout" : "{user_name} {user_email} {user_lastLogin}\n" },
      { "type" : "list", "path" : "roles_list", "layout" : "  Role: {role_name}\n" }
    ]
  },
  "spaces" : {
    "fields" : {
      "space_name"            : { "path" : "$.name",                      "format" : "30s" },
      "space_memory_assigned" : { "path" : "$.resources.memory.assigned", "format" : "6g"  },
      "space_memory_used"     : { "path" : "$.resources.memory.used",     "format" : "6g"  },
      "enabledDataLake"       : { "path" : "$.enableDataLake",            "format" : "10s" },
      "space_members"         : { "path" : "$.members[*]",                "format" : "30s", "aggregate" : "$.name" },
      "space_dbusers"         : { "path" : "$.dbusers.*",                 "format" : "30s", "aggregate" : "$.key" },
      "member_name"           : { "path" : "$.name",                      "format" : "30s" }
    },
    "rows" : [
      { "type" : "row", "layout" : "{space_name} {space_memory_assigned} {space_memory_used} {enabledDataLake} {space_dbusers}\n" },
      { "type" : "row", "path" : "$.members", "layout" : "  Member(s): {space_members}" }
    ]
    }
  }
