# Notes on treehopper development


## Fixing the PGP signature error

Error message:

~~~~{.python}
(.. snip ..)

    self.author.name = self.author.name.decode(self.encoding)
LookupError: unknown encoding: -----BEGIN PGP SIGNATURE-----
~~~~

To fix the signed `gpg` commit errors, use
  [this codebase](https://github.com/sugi/GitPython/tree/gpg-sig-support)
  which has the patches required, but isn't merged with the main
  gitpython repository.

~~~~{.bash}
git clone git@github.com:sugi/GitPython.git Sugi-GitPython
cd Sugi-GitPython
#checkout the branch that has the fix
git checkout -b gpg-sig-support origin/gpg-sig-support
#uninstall the old library
pip uninstall gitpython
#install the library
python setup.py install
~~~~


## Code notes

## How to handle a new commit


1. Create a Commit node
  a. If the Repository node does not exist, create a Repository node.
  b. Create a relation BELONGS_to from Commit node to Repository node. 

2. Iterate over the list of Files belonging to this Commit
  a. If the File node does not exist, create it and add a CREATES relationship. add "added" atribute on the relationship with number of lines added during the commit. 
  b. If the File node exists, and the commit is NOT deleting it, add a MODIFIES relationship with "added" and "removed" attributes on the relationship denoting the number of lines added or deleted during the commit.
  c. -- do -- for DELETE
  d. Also create the Directory node and add the "BELONGS_TO" relationship betweeen the directory and the File node. 

2. If the Developer for that node does not exist, create the Developer node
3. Create the relation between Commit node and Developer node, which can be one of: AUTHORED or COMMITS (??possible to have to more than one Author??)
4. Create the CHILD_OF relation to each of the parent of the newly created Commit.
5. If the Commit Node has a Tag associated with it, create TAG node and create a TAGGED relationship between them. 


### On labels


### Commit node attributes

 * `hexsha` -- Hash key
 * `message` -- commit message
 * `commit_time` -- in UnixTime
 * 

### Repository node attributes

 * `name` -- https://bitbucket.org/btbytes/treehopper

### File node attributes

 * `name` 
 * `file_type` -- python file, css file, html file etc., (Derived attribute)


### Directory node attributes

 * `name`

### Developer node attributes

  * `name`
  * `email`


### How to create a new database in Neo4j?


## Command line

Use `neotool` -- python -m py2neo.tool

## References

-
  http://blog.safaribooksonline.com/2013/11/22/neo4j-2-0-a-giant-leap-for-graphkind/
