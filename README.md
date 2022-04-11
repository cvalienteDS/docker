Description:
Simple Python app that retrieves data from API and UPSERTS in sqlite

Usage:

Go to docker folder in whick Dockerfile is

Launch Docker daemon. For example by starting Docker desktop

Build docker image:
	docker build -t my-app .

Run application:
	docker run --rm my-app 1 pythonsqlite.db
	
	1 -> Employee id to retrieve
	pythonsqlite.db -> sqlite db path
