% Treehopper -- a graph database enabled analytics tool for understanding Distributed Version Control Systems
% Pradeep Gowda and Mehmet Kilicarslan
% December 9, 2013

# Introduction


# Related work


# Approach


## Design considerations

## Technology choice

  * Neo4J
  * Python 
  * Django
  * Zurb Foundation
  * Git-Python

## Usage 

### Loading repository data

Command line interface 

~~~~{.bash}
python manage.py load_git --url /Users/pradeep/src/requests --name requests
#TBD: capture output
~~~~

### Visualising graph nodes

... insert screenshot from neo4j browser...

### Analytical dashboard

... screenshots ...

###

# Results

# Conclusion

# Future work

  * Support other distributed version control systems like `mercurial`. 
  * Handle more than one branch 
  * Create a public online webservice (say, `https://treehopper.com/`) 
    which can be used by the developers of popular code hosting websites like 
    `github.com` and `bitbucket.org`.
