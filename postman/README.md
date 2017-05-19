#Pydio API Testing

##What is it ?
Pydio API Testing provides two files to test your Pydio's API (currently V2) with [Postman](https://www.getpostman.com/) or [Newman](https://www.npmjs.com/package/newman)

##Requirements
To run the test tool you first need to have of course a running instance Pydio version 7 at least (Here is an [install guide](https://pydio.com/en/docs/v6/install-pydio)).
Edit the Pydio.postman_environment.json and replace:

1 - __URL__ with your server url
2 - __ADMIN_LOGIN__ with the admin user login
3 - __ADMIN_PASSWORD__ with the admin user password


##Run it

#from command line with newman

First install it with npm like this
```
npm install newman [--global]
```

And then run the following command
```
newman run Pydio.postman_collection.json -e Pydio.postman_environment.json --export-environment output.Pydio.postman_environment.json
```
