# SAP Data Warehouse Cloud Provisioner

## Description
This example shows how to programatically create, update and delete SAP Data Warehouse Cloud artifacts. It is written in Python and demonstrates how to:
- create and remove spaces with a simple command line
- create and remove lists of spaces using a CSV file
- create and remove connections in one or many spaces
- create and remove shares from one space to another
- generate a set of HANA tables for analytics


## Requirements
- SAP Data Warehouse Cloud administrator access, i.e., user with <span style="color: green">**DW&nbsp;Administrator**</span> privilege
- [Python version 3.8](https://www.python.org/downloads/ "download") or higher
- [Git (latest version)](https://git.com "download")
- [Node (latest version)](https://nodejs.com/en/download)
- SAP @sap/dwc_cli
- Optional: SAP HANA command line interface (hdbcli)<br>
_Note_: there are compatiblility issues with hdbcli on Apple M1 hardware
- Optional: access to an SAP HANA (on-prem or cloud) schema

### Additional requirements for development
- [Visual Studio Code](https://code.visualstudio.com/download "download")
- Python linting as described [here](https://code.visualstudio.com/docs/python/linting)

## Check your environment
### Python
Ensure that you have a valid Python 3.8 (or higher) version installed and available at the command line.  Use one of the following command to verify.

<span style="color: gray">_Note_: the latest versions of Python include both <span style="color: white">_python_</span> and <span style="color: white">_python3_</span> commands.</span>


```python -version```
<br>or<br>
```python3 -version```

```
ubuntu@ip-17-1-3-11:~$ python3 --version
Python 3.10.4
ubuntu@ip-17-1-3-11:~$
```
### Git (local)
```git --version```

```
ubuntu@ip-17-1-3-11:~$ git --version
git version 2.34.1
ubuntu@ip-17-1-3-11:~$        
```
### Configure HANA allow list (optional)
Set allow list for Cloud HANA connection
![SAP Data Warehouse Cloud - IP Allowlist](images/allowlist.png)
## Download and Installation
Clone or download this repository to a directory.a for example to /users/c:\devpath\dwc-provisioning.  These commands are similar
for all major operating systems, i.e., Linux, Windows, and
Mac OS X.

### Ubuntu Linux
For this example, this is a Ubuntu image running in a micro-
### Windows
Then open a console and change to the download path:
```bat
c:\> cd c:\devpath\dwc-provisioning
```
Generate git key
$ ssh-keygen -t rsa -b 4096

curl 
Install the Python virtual environment tool.
```
sudo apt install python3.10-venv
```
ubuntu@ip-172-31-83-11:~/dwc-provisioning/.venv/bin$ cat activate
# This file must be used with "source bin/activate" *from bash*
# you cannot run it directly

ubuntu@ip-172-31-83-11:~/dwc-provisioning$ source .venv/bin/activate
(.venv) ubuntu@ip-172-31-83-11:~/dwc-provisioning$                            
 
Create a python virtual environment named .venv:
```bat
c:\devpath\dwc-provisioning> python -m venv .venv
```

Activate the python virtual environment:
```bat
c:\devpath\dwc-provisioning> .venv\scripts\activate
```

If the environment is activated correctly, a previx (.venv) is shown in the command line:
```bat
(.venv) c:\devpath\dwc-provisioning>
```


Install the required Python packages:
```bat
(.venv) c:\devpath\dwc-provisioning> python -m pip install -r requirements/core.txt
```
Install additional Python packages if this installation is used for development:
```bat
(.venv) c:\devpath\dwc-provisioning> python -m pip install -r requirements/development.txt
```


## Configuration
```
python dwc_tool.py config
  --dwc-url https://{tenant}.{ds}.hcs.cloud.sap
  --dwc-user user.name@domain.com
  --dwc-password NotYourPassword!
  --dwc-cli 
```
To use the provisioner, credentials for SAP Data Warehouse Cloud and optionally for a HANA schema.

python3 
An admin-user is needed with the following privileges:
- system privilege CREATE SCHEMA (grantable to other users and roles)
- system privilege USER ADMIN
- object privilege ESH_CONFIG execute (grantable to others)

Configuration is done with the config.py script using the following parameters
- --action install
- --db-host: The HANA host name
- --db-port: The HANA port number
- --db-setup-user: The HANA user name used for setup
- --db-setup-password: The HANA user password for the seup-user. Note: This user-name and passwords are not stored
- --db-schema-prefix: The prefix which is used for the schemas of this installation. To avoid conflicts, there must not be any other schemas on the database starting with this schema prefix.

```bat
c:\devpath\hana-search> python src/config.py --action install --db-host <<your_hana_host>> --db-port <<your_hana_port>> --db-setup-user <<your HANA admin user>> --db-setup-password <<your HANA admin password>> --db-schema-prefix <<your HANA >>

```
## Creating SAP Data Warehouse Cloud artificats ##
Commands:
- config
- script {filename}
- users list 

- spaces create
- spaces delete
- spaces list
- spaces bulk create
- spaces bulk delete

- connections list
- connections create
- connections delete

- shares create


The configuration will create some HANA DB users and the src/.config.json file which contains configuration information and users and passwords created for the installation (needed e.g. for debugging purposes). Please do not change the src/.config.json file.

The default settings for the web-server (host 127.0.0.1 and port 8000) can be changed using parameters srv-host and srv-port.


To uninstall run the following command:

```bat
c:\devpath\hana-search> python src/config.py --action delete --db-setup-user <<your HANA admin user>> --db-setup-password <<your HANA admin password>>
```
Attention: This will delete ALL data of this installation!

### Start server
Start the server in the console with the activated virtual environment:
```bat
c:\ cd c:\devpath\hana-search
c:\devpath\hana-search> .venv\scripts\activate
(.venv) c:\devpath\hana-search> python src\server.py
```

The message "Application startup complete" indicates a successful server startup.

### Run end-to-end test

```bat
(.venv) c:\devpath\hana-search> python tests\packages\run_tests.py
```
The test script prints a success-message in the last output line if all tests are executed successfully.


## Known Issues
This is an example application in an early stage of development, so
- don't store personal information because of missing access logging
- don't store sensitive information because there is no access control
- don't use the example application productively because users and passwords generated by the **config** command, while obfuscated, are not securely encrypted.
- don't expect always meaningful error messages in reaction to erroneous input.


## How to obtain support
This is an example application and not supported by SAP. However, you can 
[create an issue](https://github.com/SAP-samples/<repository-name>/issues) in this repository if you find a bug or have questions about the content.
 
For additional support, [ask a question in SAP Community](https://answers.sap.com/questions/ask.html).

## Contributing
If you wish to contribute code, offer fixes or improvements, please send a pull request. Due to legal reasons, contributors will be asked to accept a DCO when they create the first pull request to this project. This happens in an automated fashion during the submission process. SAP uses [the standard DCO text of the Linux Foundation](https://developercertificate.org/).

## Code of Conduct
see [here](CODE_OF_CONDUCT.md)
## License
Copyright (c) 2022 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0 except as noted otherwise in the [LICENSE](LICENSE) file.
