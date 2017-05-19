# Pydio API Testing

## What is it ?
Pydio API Testing provides two files to test your Pydio's API (currently V2) with [Postman](https://www.getpostman.com/) or [Newman](https://www.npmjs.com/package/newman)

## Requirements
To run the test tool you first need to have of course a running instance Pydio version 7 at least (Here is an [install guide](https://pydio.com/en/docs/v6/install-pydio)).
Edit the Pydio.postman_environment.json and replace:

1. | __URL__ with your server url
2. | __ADMIN_LOGIN__ with the admin user login
3. | __ADMIN_PASSWORD__ with the admin user password


## Run it

### from command line with newman

First install it with npm like this
```
npm install newman [--global]
```

And then run the following command
```
newman run Pydio.postman_collection.json -e Pydio.postman_environment.json --export-environment output.Pydio.postman_environment.json
```


### with postman

First you need to import the `Pydio.postman_collection.json` file as a Collection.
Click to the `Import` button at the top left of Postman and choose the `Pydio.postman_collection.json` file.

![](img/importCollection.png)

After the import you must see the collection like this

![](img/collection.png)

This collection refers to a Postman environment. Click to the 'wheel' button to `Manage environments` at the top right of Postman and choose the `Pydio.postman_environment.json` file.

![](img/importEnvironment.png)

After the import you can see the environment if you click to the eye. If you did not manually edit the environment file, use "Edit" to setup the correct values for your server URL and credentials.

![](img/environment.png)

Collection and environment file are imported, we can test our Pydio's API. Click to the `Runner` button at the top left of Postman.

![](img/runner.png)

A second screen will appear and you need to select `Pydio API V2` as collection (in the 1) and `Pydio API V2` as an environment (in the 2).

![](img/runnerBefore.png)

If you do that you must see this.

![](img/runnerAfter.png)

You can now start the test