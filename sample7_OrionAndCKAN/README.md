# build and run
```
docker compose up -d
```

# control using GUI
## Access URL
Access the following URL using the Web browser.
```
http://localhost:5000/
```

# How to use
## First Setting
1. Click "Log In"
2. Input following
Username or Email   : ckan_admin
Password            : test1234

## Create organizations
1. Click "organizations"
2. Click "Add organizations"
3. Input following
Name        : sample-organizations
Description : (blank)

## Create dataset
1. Click "organizations"
2. Click "sample-organizations"
3. Click "Add Dataset"
4. Input following
Title       : sample-dataset1
Description : (blank)
Tags        : (blank)
License     : any
Organization: sample-organizations

others      : default...

5. Click "Upload"
6. Select "sample.csv", this csv exists in this git

## Create View
1. Click "Datasets"
2. Click "sample-dataset1"
3. Click "sample.csv"
4. Click "Manage"
5. Click "Views"
6. Click "New views"
7. Click "Data Exploer"
8. Input following
Title       : sample-view
9. Click "sample-view"
10. Scroll down

## Extensions
this sample include extension sample.
extension is located in the ./ckan/plagin/ckanext-sample.
Access the following URL using the Web browser.
```
http://localhost:5000/sample/page
```

# down
```
docker compose down
```
