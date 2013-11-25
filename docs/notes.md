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

### How to create a new database in Neo4j?


## Command line

Use `neotool` -- python -m py2neo.tool

## References

-
  http://blog.safaribooksonline.com/2013/11/22/neo4j-2-0-a-giant-leap-for-graphkind/
