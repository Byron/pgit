## Submodule

The submodule command allows you to interact with git-submodules, that is you may query data about them, as well as change them in a variety of ways.

The main benefit of this implementation is its ability to update submodules keeping the actual change in mind, which allows you to synchronize your submodules the same way as git synchronizes the rest of your working tree.

**Please use the `--dry-run (-n)` flag while testing operaitons that would change your repository, as it will only tell what it would do, without actually doing so.**

## Operations

The command supports a variety of operations. An operation is specified first on the commandline, followed by flags and command-specific arguments.

### Query

Querying the current intermediate submodules is the command's default action
    
    pgit submodule query

### Update

Update re-synchronizes all submodules recursively, assuring that your working- tree including all submodules corresponds to the state stored in the repository. This will properly deal with removed, added and changed submodules as well.

By default, all submodules will be updated, but you may specify one or more submodule names to restrict to update process to *their* submodules.

    # update only submodules of the submodule 'subm'
    pgit submodule update subm
    

The operation supports the following flags:

* `--to-latest-revision (-l)`

    - Instead of using the submodule's sha as hint to which revision to update the submodule's repository, update it the latest available revision in the remote repository.
 
* `--base-commit`

    - Specifies the commit rev-spec to use (e.g. HEAD~1, ORIG_HEAD, HEAD@{1}) as basis for the comparison with the currently checked-out commit in the root-repository. From the difference of the commits the command determines the changes.
    - **Note:** Its extremely important that the base-commit is correct, otherwise the computed differences might not accurately reflect the actual repository state. Although the end-point will be correct, the amount or the type of differences will be incorrect.
 
* `--non-recursive`

    - Explicitly force the command not to update the whole hierarchy of modules, but only the intermediate submodules found in this repository.

* `--dry-run (-n)`

    - If set, no change will be made. This allows to see in advance which steps would be performed during an update.

 
### Add

Use the *add* operation to create a new submodule.
    
The following flags may be specified:

* `--branch (-b)`

    - Specify the branch to checkout and track when cloning the repository
 
* `--no-checkout`

    - If set, the repository will be cloned, but not checked out, i.e. the working tree will be empty
 
 
### Move

The move operation allows you to move the submodule's repository to a different place in the repository. This effectively changes the path at which it resides:

    # move the submodule 'subm's  repository to destination/path
    pgit submodule move subm destination/path
    
The following flags alter the way the move operation is handled:

* `--skip-configuration`

    - If set, submodule's path will not be renamed in the configuration, only the possibly existing repository on disk. This is only valid if the configuration already points to the given destination directory
 
* `--skip-module`

    - If set, the module on disk will not be moved, the only adjustment will be made to the configuration.
 
 
### Remove

The operation removes an existing submodule. It will, by default, not remove the submodule's repository if it contains any user modifications:
    
    pgit submodule remove [flags] submodule.name[ ...]
    
    
The following options may be specified:
    
* `--force`

    - If set, the submodule's repository will be deleted despite of user modifications.
 
* `---dry-run (-n)`

    - If set, no change will be made. This allows to see in advance if there would be any problems if a deletion would be attempted.
    - *Note*: The first of the three dashes was just added to satisfy the documentation generator, the command needs only two of them.
 
* `---skip-configuration`

    - If set, the submodule's configuration will not be removed, only its repository
    - *Note*: The first of the three dashes was just added to satisfy the documentation generator, the command needs only two of them.
 
* `---skip-module`

    - If set, the submodule's repository will remain on disk, only its configuration will be removed.
    - *Note*: The first of the three dashes was just added to satisfy the documentation generator, the command needs only two of them.
