## pgit (PeeGit)

**pgit** ('pee-git') is a git command-line interface written in python. It aims to fix shortcomings and convenience issues arising with the traditional c-git implementation, but does for now not strive to be feature-complete.

At the current stage, its just meant to expose special features, namely submodul handling, of git-python to the command-line, but at some point it might start driving git-python into new directions.

At this point, there is no guarantee that pgit will ever be as full-featured as the cgit command-line suite, but it will definitely expose some useful features.

### REQUIREMENTS
* [git-python](https://github.com/gitpython-developers/GitPython)
* [bcore](https://github.com/Byron/bcore)

Both frameworks are contained in the ext/ directory and are setup as git-submodule.

### Install

For installation, please have a look at the [pgit distribution repository](https://github.com/Byron/pgit-distro).

### Development Status

This project currently evolves only when I need a special purpose command that isn't easily achieved through the git commandline.

### MAILING LIST
http://groups.google.com/group/git-python

### ISSUE TRACKER
https://github.com/Byron/pgit/issues

### LICENSE

GNU LESSER GENERAL PUBLIC LICENSE, see LICENSE file for details.
