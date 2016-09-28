Tools for automatically testing various aspects of a deployed Pydio instance.

# Python SDK & Selenium

## Introduction

This package will use python Py.test utility, Pydio official python SDK and Selenium to perform a couple of operation on the server. It is currently mainly testing api version1, creating a workspace, uploading files / moving them / deleting them. It also tests share links by using the Selenium tool and loading the link in a headless browser, verifying it has the right properties.

## How to run

 - Install PyTest (see pytest.org)
 - Install Selenium, Firefox webdriver
 - Copy and configure server.sample.json and workspace.sample.json to server.0.json and workspace.0.json with proper values.

Now run py.test in root folder, or python main.py in root folder

# Postman / Newman

The files located in the postman/ folder can be imported in Postman and used to run automated tests on the pydio api version2 (pydio7 only). See the README inside this folder for more info.
