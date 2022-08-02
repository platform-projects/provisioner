# SAP Data Warehouse Cloud Provisioner

## Table of Contents
* [1.0 - Description](#description)
* [2.0 - Requirements](#requirements)
* [3.0 - Check the environment](#check)
* [4.0 - Download](#download)
* [5.0 - Optional Python setup](#python-config)
* [6.0 - Install Python packages](#python-install)
* [7.0 - Configure HANA (optional)](#config-hana)
* [8.0 - Provisioner Configuration](#config)
* [9.0 - Command Syntax](#syntax)
* [10.0 - Uninstall](#uninstall)
* [11.0 - Errata](#errata)

## <a href="#description"></a>1.0 Description
This sample tool provides an example of how to programmatically create, update, and delete SAP Data Warehouse Cloud artifacts. The tool, referred to as **provisioner**, is written in Python and demonstrates how to automate various SAP Data Warehouse Cloud provisioning activities. The **provisioner** can perform the following actions against SAP Data Warehouse Cloud tenants:
- create and remove spaces with a simplified command line
- bulk create and remove spaces using a CSV file
- create and remove connections in one, or many spaces
- create and remove shared objects from one space to another
- create scripts of multiple commands
- generate a HANA tables for monitoring and analytics

## <a href="#requirements"></a>2.0 - Requirements
Before installing andrunning the **provisioner**, the following configurations and 3rd party components must be available.

### 2.1 - Required
- SAP Data Warehouse Cloud administrator access, i.e., user with <span style="color: green">**DW&nbsp;Administrator**</span> privilege
- [Python version 3.8](https://www.python.org/downloads "Download") or higher

### 2.2 - Optional
- [Git (latest version)](https://git.com "Download")
- Access to an SAP HANA (on-prem or cloud) schema

### 2.3 - Development
- [Node (latest version)](https://nodejs.com/en/download)
- [SAP @sap/dwc_cli](https://www.npmjs.com/package/@sap/dwc-cli)

## <a href="#check"></a>3.0 Check the environment
To ensure success running this tool, please use the following steps to validate the software requirements.

### 3.1 - Python
The **provisioner** tool requires Python 3.8 (or higher) to be available.  Use the following command to verify the Python installation.

><span style="color: gray">_Note_: the latest versions of Python include both <span style="color: white">_python_</span> and <span style="color: white">_python3_</span> versions of the command to start Python.</span>

```
ubuntu@ip-17-1-3-11:~$ python --version
Python 3.10.4
ubuntu@ip-17-1-3-11:~$
```
### 3.2 - Git
To retrieve the **provisioner** from GitHub, the command line version of Git is an easy way to download the project to a local directory. The project may also be downloaded from GitHub as a zip file using a browser.

```
C:\>git --version
git version 2.37.0.windows.1
C:\>
```
## <a href="#download"></a>4.0 - Download
Clone or download this repository to a directory. In all the examples in this README, a sub-directory named "tools" will be used as the starting location for all operations.

The commands to download the project are similar for all major operating systems, i.e., Linux, Windows, and Mac OS X.

### 4.1 - Git Download
The **provisioner** is available on the SAP-samples Github repository: [DWC Provisioner](https://github.com/SAP-samples/dwc-provisioner).  The tool can be downloaded as a zip file from Github or the tool can be cloned directly from Github using one of the following commands.

_Ubuntu Linux_:

From the home directory of the user _ubuntu_:
```bash
ubuntu@myhostname:~$ mkdir tools
ubuntu@myhostname:~$ cd tools
ubuntu@myhostname:~/tools$ git clone https://github.com/SAP-samples/dwc-provisioner
```

_Windows_

Open a command window (cmd):
```bash
c:\> mkdir c:\tools
c:\> cd c:\tools
c:\> git clone https://github.com/SAP-samples/dwc-provisioner
Cloning into 'dwc-provisioner'...
```
_MacOS_

From a terminal session:
```bash
myuser@mymachine ~ % mkdir tools
myuser@mymachine ~ % cd tools
myuser@mymachine tools % git clone https://github.com/SAP-samples/dwc-provisioner
Cloning into 'dwc-provisioner'...
myuser@mymachine tools % 
```

### 4.2 - Browser Download
Using a browser, navigate to the SAP-samples/dwc-provisioner repository and click the "Download ZIP" button.  Save or move the ZIP file to the "tools" sub-directory and unzip the contents.

## <a href="#python-config"></a>5.0 - Optional Python setup
Python allows you to create "virtual environments" to help manage dependencies between installed packages and the versions of packages used in a specific project.  <span style="font-weight: bold; color: green">It is a best practice</span> to create a virtual environment for each project.  Without a virtual enviroment, all Python packages are installed in the "global" space and all projects share the same package versions.

> https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

### 5.1 - Install the Python virtual environment tool.
_Ubuntu_
```bash
sudo apt install python3-venv
```
_Windows/MacOS_
```
python -m pip install --user virtualenv
```
### 5.2 - Configure a virtual environment
Python virtual environments must be explicity created and activated.  The following command create a Python virtural environment in the dwc-provisioner directory.

<pre>
ubuntu@ip-17-1-83-11:~/tools$ cd dwc-provisioner
ubuntu@ip-17-1-83-11:~/tools/dwc-provisioner$ python3 -m venv .venv
</pre>

### 5.3 - Activate the virtual environment
Python virtual enviroments must be activated each time in a command/terminal window before using Python.

_Ubuntu / Linux / Mac OS_

Non-windows platforms activate the virtual enviroment by "sourcing in" the necessary enviroment to the current shell.

```bash
ubuntu@ip-17-1-83-11:~/tools/provisioner$ source .venv/bin/activate
(.venv) ubuntu@ip-17-1-83-11:~/tools/provisioner$ 
```

> **Note**: the the (.venv) prefix has been added to the command line prompt.

_Windows_

Windows activates the virtual enviroment by executing a batch script.

```bat
c:\devpath\dwc-provisioning> .venv\scripts\activate
```

If the environment is activated correctly, a previx (.venv) is shown in the command line:
```bat
(.venv) c:\devpath\dwc-provisioning>
```

## <a href="#python-install"></a>6.0 - Install Python packages
The **provisioner** requires publically available Python packages to be installed before running the tool.  The packages are quickly installed using the following command:

```bat
(.venv) c:\tools\dwc-provisioner> python -m pip install -r requirements/core.txt
```

## <a href="#config-hana"></a>7.0 - Configure HANA (optional)
To create and store information about SAP Data Warehouse Cloud in an SAP HANA Cloud instance, ensure the IP address where this tool runs is in the allow list for SAP HANA Cloud connections.  In the example below, an SAP Data Warehouse Cloud Data Access User (a.k.a., hash-tag (#) user) is the target, so in SAP Data Warehouse Cloud set the IP Allow list under the System / Configuration tab.

![SAP Data Warehouse Cloud - IP Allowlist](images/allowlist.png)

## <a href="#config"></a>8.0 - Provisioner Configuration
To start using the **provisioner**, a configuration file is created to identify the target SAP Data Warehouse Cloud tenant and set the username and password values.

Refer to the following sections on command syntax for additional information on the `config` command.

```
c:\> cd tools\dwc-provisioner

c:\> .venv\scripts\activate

(.venv) c:\tools\dwc-provisioner> provisioner config
  --dwc-url https://{your-tenant}.{ds}.hcs.cloud.sap
  --dwc-user user.name@domain.com
  --dwc-password NotYourPassword!
```
> **Notes**:
> 
>1. Command options are listed on separate lines for clarity.
>2. The change directory and starting the Python virtual environment commands are included for completeness.

## <a href="command-syntax"></a>9.0 - Command Syntax
The provisioner tool accepts the following commands:
|Command|Description|
|-------|-----------|
|config|Set the **provisioner** environment configuration|
|users|User actions against the tenant, including list, create, and delete|
|spaces|Create, delete and list spaces.  This includes bulk loading and member assignment|
|shares|Create, delete and list objects shared to other space(s)|
|connections|Create, delete and list connections in one, or more spaces|
|script|Run a list of commands from a script file.|

|Parameter|Values|
|---------|------|
|--config|Configuration file name (optional)|
|--logging|Generate logging message, options: 'none', 'info', 'debug', 'warn', 'error'

### 9.1 Command: `config`
This command saves connection information for both an SAP Data Warehouse Cloud tenant and optionally an SAP HANA Cloud (or on-premise) database.  After running this command, a new configuration file named `config.ini` is created in the current working directory.

> Note: the `config` command does not validate the tenant or SAP HANA configuration values.

|Parameter|Values|
|---------|------|
|--dwc-url|Target SAP Data Warehouse Cloud tenant|
|--dwc-user|User name with administrative privileges on the tenant|
|--dwc-password|Password for the user specified in the --dwc-user parameter|
|--hana-host|HANA host name|
|--hana-port|HANA port|
|--hana-user|HANA username|
|--hana-password|HANA password|
|--hana-encrypt|Include the option to encrypt SAP HANA communications (default=False)|
|--hana-sslverify|Validate the HANA certificate (default=False)|

**Examples**:
1. Set the configuration for the SAP Data Warehouse Cloud tenant:

```
(.venv) c:\tools\dwc-provisioner> provisioner config 
    --dwc-url https://notarealtenant.us10.hcs.cloud.sap
    --dwc-user not.a.real.user@dummy.sap
    --dwc-password NotARealPassword!
```

After running this command, the `config.ini` file has the following content:

```
(.venv) c:\tools\dwc-provisioner> type config.ini

[dwc]
dwc_url = https://mytenant.us10.hcs.cloud.sap
dwc_user = not.a.real.user@dummy.sap
dwc_password = eJwLz8vxDDT0M04xMDFKzPE0BQAqfgTD
```

> Note: password values never appear in plain text.

2. Set both the SAP Data Warehouse Cloud and HANA Data Access user credentials.  This example connects to the SAP Data Warehouse Cloud tenant and a Data Access User named PROVISIONER defined in the space ADMINSPACE, i.e., ADMINSPACE#PROVISIONER.

```(.venv) c:\tools\provisioner> provisioner config
    --dwc-url https://notarealtenant.us10.hcs.cloud.sap
    --dwc-user not.a.real.user@dummy.sap
    --dwc-password NotARealPassword!
    --hana-host 9dc97f57.hana.prod-us10.hanacloud.ondemand.com
    --hana-port 443
    --hana-user ADMINSPACE#PROVISIONER
    --hana-password notMyPassword 
    --hana-encrypt
```

### 9.2 - Command: `users`
The `users` command lists, creates, and deletes users from an SAP Data Warehouse Cloud tenant.

#### 9.2.1 - Command: `users list`
The `users list` command retrieves user information from the SAP Data Warehouse Cloud tenant.

|Parameter|Description|
|---------|-----------|
|-f, --format|output style: 'hana', 'csv', 'json', 'text' - default=text|
|-p, --prefix|prefix for output, default="DWC_USERS"|
|-s, --search|seach user names or emails on substring (default = false)|
|-d, --directory|directory for output|
|-q, --query|query users as substring searches|
|userName|user name(s) to list, separated by spaces|

**Examples:**
1. List all the users in the tenant to the console.

```
provisioner users list
```

2. List all the user and output the information in CSV format to the specified output directory.  The output file names will be DWC_USERS.csv and DWC_USERS_role_members.csv.

```
provisioner users list -f csv -d c:\temp
```

3. Search the users in the tenant for users with "sap.com" appearing anywhere in their definition (including email), as well as any user with the word "greynolds" in their definition.

```
provisioner users list -S sap.com greynolds
```

#### 9.2.2 - Command: `users create`

*Work in progress*

#### 9.2.3 - Command: `users delete`

*Work in progress*

### 9.3 - Command: `spaces`
The spaces command can create, delete and list spaces in the tenant.

### 9.3.1 - Command: `spaces list`
The `spaces list` command queries the SAP Data Warehouse Cloud tenant for details for all spaces, specific spaces, or substring searches of available spaces.  If no space ids are provided, all spaces in the tenant will be included.  For instance, adding the `--query` flag with a space id of "TRAINING" finds spaces with names such as "TRAINING_LOB", "FINANCE_TRAINING", and "HRTRAINING".

|Parameter|Description|
|---------|-----------|
|-f, --format|output style: 'hana', 'csv', 'json', 'text'|
|-p, --prefix|prefix for output, default="DWC_SPACES"|
|-q, --query|seach space names on substring (default = false)|
|-d, --directory|filename for output|
|spaceID|space id(s) to list|

**Examples:**
1. List all spaces in the tenant to the console.

```
provisioner spaces list
```

2. List all spaces containing the word "TRAINING" and the space containing "FINANCE_DATA."

```
provisioner spaces list TRAINING FINANCE_DATA
```

3. List all the spaces to HANA tables.

```
provisioner spaces list --format hana
```

### 9.3.2 - Command: `spaces create`
The `spaces create` command creates a new space in  the SAP Data Warehouse Cloud tenant.  If the --template option is specified, the provided space ID is used to lookup an existing Space to use as a template.

|Parameter|Description|
|---------|-----------|
|-b, --businesss | optional business name to assign - defaults to spaceID|
|-t, --template | space id to use as a template|
|-d, --disk | disk allocated to space|
|-m, --memory | memory allocated to space|
|-f, --force | force the re-creation if space exists|
|spaceID | space id to create|
|users | users to add to the space|

**Examples:**

1. Create a new space using only command line options having 1 GB of disk storage and .5 GB of in-memory storage.

```
provisioner spaces create --disk 1 --memory .5 MYNEWSPACE
```

2. Create a new space from an existing template.  If the new space already exists, delete it before re-creating (--force).

```
provisioner spaces create --template FINANCE_DATA --force MYNEWSPACE
```

### 9.3.3 - Command: `spaces delete`
Delete one, or more spaces by listing their space IDs on the command line.

|Parameter|Description|
|---------|-----------|
| spaceID | space id(s) to create |

> **Note**: the --query option for space IDs is not supported for space delete operations.

**Examples:**

1. Delete a single space.

```
provisioner spaces delete MYSPACEID
```

2. Delete multiple spaces in a single operation.

```
provisioner spaces delete TRAINING_1 TRANING_2 RANDOMSPACE THEOTHERSPACE
```

### 9.3.4 - Command: `spaces bulk`
The `spaces bulk` command creates or deletes multiple spaces using a CSV file to provides the
list of spaces.  For `bulk create` operations, the CSV file must have the following columns:

```
Space Id, Business Name, Disk, Memory, Template, Force, User 1, User 2, User 3, etc
```

> **Note**: Any number of users for a space may be included as comma separated values.

For bulk delete operations, only the space ID column is required - all other values are ignored.

#### 9.3.4.1 - Command: `spaces bulk create`
Create spaces defined in a CSV file.

|Parameter|Description|
|---------|-----------|
|-s, --skip | header lines to skip in the CSV file, default="1" |
|-f, --force | force the re-creation if space exists |
|-t, --template | Space ID to use as a template if not specified per space |
|filename | CSV file containing spaces to create |

**Example:**

```
provisioner spaces bulk create c:\tools\new-spaces.csv
```

#### 9.3.4.2 - Command: `spaces bulk delete`
This command is similar to the `spaces delete` command and is intended to quickly delete the spaces created with the `spaces bulk create` command.  The CSV file requires only 1 column containing the space IDs to be deleted.

|Parameter|Description|
|---------|-----------|
| -s, --skip | header lines to skip in the CSV file, default="1" |
| filename | CSV file containing space names to delete |

**Example:**

```
provisioner spaces bulk create c:\tools\new-spaces.csv
```

### 9.3.5 Command: `spaces members`
The `space members` can command list existing space members, add members to a space, or remove members from a space.
#### 9.3.5.1 - Command: `spaces member list`
List the members in one or more spaces.

|Parameter|Description|
|---------|-----------|
|-q, --query|seach space names on substring (default = false)|
|-f, --format|output style: 'hana', 'csv', 'json', 'text'|
|-p, --prefix|prefix for output, default="DWC_SPACES"|
|-d, --directory|filename for output|
|spaceID|space id(s) to list|

**Example:**
1. List the members in all spaces in the tenant.

```
provisioner spaces members list
```

2. List the members for two spaces: MYSPACE and FINANCE_DATA.

```
provisioner spaces members list MYSPACE FINANCE_DATA
```

3. List the member of all spaces having the word TRAINING in the space ID and FINANCE_DATA.

```
provisioner spaces members list --query FINANCE_DATA TRAINING
```

#### 9.3.5.2 - Command: `spaces member add`
Add a tenant one, or more users to an existing space.  By default, this command expects "USER ID" values; the "USER ID" values are not email addresses.  To include users by either "USER ID" or email address, use the --query option to search for users based on the provided string.

|Parameter|Description|
|---------|-----------|
|-q, --query|seach space names on substring (default = false)|
|spaceID|space id(s) to list|
|user|one or more user names to add to the space|

**Examples:**

1. Add a user to a space.

```
provisioner spaces member add MYSPACE MGREYNOLDS
```

2. Add multiple users to a space.

```
provisioner spaces member add MYSPACE MGREYNOLDS BSMITH
```

3. Add multiple users have email addresses containing "mycompany.com" to a space.

```
provisioner spaces member add --query MYSPACE mycompany.com
```

#### 9.3.5.3 - Command: `spaces member remove`
Remove one, or more tenant users from an existing space.  By default, this command expects "USER ID" values; the "USER ID" values are not email addresses.  To users users by either "USER ID" or email address, use the --query option to search for users based on the provided string.

|Parameter|Description|
|---------|-----------|
|-q, --query|seach space names on substring (default = false)|
|spaceID|space id(s) to list|
|user|one or more user names to remove to the space|

**Examples:**

1. Remove a user from a space.

```
provisioner spaces member remove MYSPACE MGREYNOLDS
```

2. Remove multiple users from a space.

```
provisioner spaces member remove MYSPACE MGREYNOLDS BSMITH
```

3. Remove multiple users have email addresses containing "mycompany.com" to a space.

```
provisioner spaces member remove --query MYSPACE mycompany.com
```


### 9.4 - Command: `shares`
#### 9.4.1 - Command: `shares list`
#### 9.4.2 - Command: `shares create`
#### 9.4.3 - Command: `shares delete`

### 9.5 - Command: `connections`
The `connections` command can list, create, and delete connections from spaces.  Spaces may be explicitly identified by ID or searched for based on a search strings.

#### 9.5.1 - Command: `connections list`
List the connections from one, or more spaces.
|Parameter|Description|
|---------|-----------|
|-q, --query|seach space names on substring (default = false)|
|-c, --connection|connection name to list|
|-f, --format|output style: 'hana', 'csv', 'json', 'text' - default=text|
|-p, --prefix|output prefix, default=DWC_CONNECTIONS|
|-d, --directory|directory for output files|
|spaceID|space id(s) to list connections|

**Examples:**

1. List the connections from a single space.

```
provisioner connections list MYSPACE
```

2. List the connections from spaces having "TRAINING" in the space ID.

```
provisioner connections list --query TRAINING
```

3. List the specific connection "HANA on-premise" in all spaces.

```
provisioner connections list --connection "HANA on-premise"
```

#### 9.5.2 - Command: `connection create`
#### 9.5.2 - Command: `connection delete`

## 10.0 - Uninstall
To uninstall simply remove the dwc-provisioner directory, including all sub-directories

## <a href="#errata"></a>11.0 - Errata
### 11.1 - Known Issues
This example application is in an early stage of development, so
- don't store personal information because of missing access logging
- don't store sensitive information because there is no access control
- don't use the example application productively because users and passwords generated by the **config** command, while obfuscated, are not securely encrypted.
- don't expect always meaningful error messages in reaction to erroneous input.

### 11.2 - How to obtain support
This an example application not supported by SAP. However, you can 
[create an issue](https://github.com/SAP-samples/dwc-provisioner/issues) in this repository if you find a bug or have questions about the content.
 

### 11.3 - Contributing
If you wish to contribute code, offer fixes or improvements, please send a pull request. Due to legal reasons, contributors will be asked to accept a DCO when they create the first pull request to this project. This happens in an automated fashion during the submission process. SAP uses [the standard DCO text of the Linux Foundation](https://developercertificate.org/).

## 11.4 - Code of Conduct
see [here](CODE_OF_CONDUCT.md)

## 11.5 - License
Copyright (c) 2022 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0 except as noted otherwise in the [LICENSE](LICENSE) file.
