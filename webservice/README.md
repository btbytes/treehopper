Treehopper Webservice
======================

The TWS application serves two purposes:

1. present user interface showing important statistics about repository
2. expose a web service end point for updating the graph database with new commit information.


Installing libraries
--------------------

First install `virtualenvwrapper`

    pip install virtualenvwrapper

Create a virtualenv for the project:

    mkvirtualenv thdev

Install the dependencies:

    pip install -r requirements.txt


Running the application
-----------------------

Start the webservice with
	python app.py
