## pgit (PeeGit)


Besides the name being funny, pgit wants to become a fully usable git command-line implementation in python one day.

At the current stage, its just meant to expose special features of git-python to the command-line, but at some point it might start driving git-python into new directions.

At this point, there is no guarantee that pgit will ever be as full-featured as the cgit command-line suite, but it will definitely expose some useful features.

### REQUIREMENTS
* [git-python](https://github.com/gitpython-developers/GitPython)
* [bcore](https://github.com/Byron/bcore)

Both frameworks are contained in the ext/ directory and are setup as git-submodule.

### Install
Currently you can only use pgit directly from the code repository. The creation of a packaged redistributable is planned.

See the next section for how to get a copy of the source code.

### Source
The source is available at https://github.com/Byron/pgit.git and can be cloned using::
    
    git clone https://github.com/Byron/pgit.git
    cd pgit
    git submodule update --init --recursive

### MAILING LIST
http://groups.google.com/group/git-python

### ISSUE TRACKER
https://github.com/Byron/pgit/issues

### LICENSE

GNU LESSER GENERAL PUBLIC LICENSE, see LICENSE file for details.