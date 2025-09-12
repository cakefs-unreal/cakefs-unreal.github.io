## Introduction
CakeFS has special policy types that allow users to customize various behaviors across the API. These policies are represented by UENUM types and they are the same in both Blueprint and C++ code. 

{{ src_loc_group('Policies', 'CakePolicies')}}

## Default Policy Values
Within the `CakePolicies.h` header file, the namespace `CakePolicies` defines default values for each Cake Policy enum. Any function parameter with a default value uses these default values, so if you wish to change the default CakeFS behavior for your project, you only have to change one place in the source code to accomplish this. (You will need to recompile the plugin, however.)

!!! note
    The `CakePolicies` namespace also contains some utility functions that can make working with the enums a bit more ergonomic. If you are curious, please browse the source code for more information.

## OpDepth
OpDepth determines the depth an IO operation is applied in relation to the target directory. 

> **ECakePolicyOpDepth**

{{ read_csv(csv_policy('OpDepth')) }}

Let's take a look at an example.
```
Example Directory Tree
📁 Game
    📄 read_me.md [Shallow]
    📁 Data [Shallow]
        📄 map-1.lv [Deep]
        📄 map-2.lv [Deep]
        📁 Tables [Deep]
            📄 items.db [Deep]
```

With `Game/` as our source directory, a `Shallow` items traversal will visit `read_me.md` and `Data/`. 

A `Deep` items traversal will visit `read_me.md`, `Data/`, `map-1.lv`, `map-2.lv`, `Tables/`, and `items.db`.

## OverwriteItems	
OverwriteItems determines whether an IO operation can overwrite an item (file or directory) that already exists. 

> **ECakePolicyOverwriteItems**

{{ read_csv(csv_policy('OverwriteItems')) }}

## MissingParents
MissingParents determines whether missing parent directories in a path should be created during file or directory operations. 

> **ECakePolicyMissingParents**

{{ read_csv(csv_policy('MissingParents')) }}

Let's consider a concrete example: 
Assume directory `x/game/data/models` exists, and that we want to create the following file: `x/game/data/models/hero/hero_main.obj`.

Assume the file does not exist, nor does its parent directory `hero`.

In this case, the subdirectory `hero` in `x/game/data/models/hero/` is classified as a missing parent. In order to successfully create `hero_main.obj`, we need to first create the parent directory `hero`. 

If we attempted to create `hero_main.obj` and we set the MissingParentsPolicy to `CreateMissing`, the final result would create both the subdirectory `hero` and the file `hero_main.obj`. 

If we set the MissingParents policy to `DoNotCreateMissing`, the entire operation will fail. 

## ExtFilterMode
ExtFilterMode determines how a {{ link_cakedir() }} object will utilize its {{ link_extfilter('file extension filter') }} to select files to visit during a traversal operation.

> **ECakePolicyExtFilterMode**

{{ read_csv(csv_policy('ExtFilterMode')) }}

## ExtMatchMode
ExtMatchMode determines how a {{ link_cakedir() }} object examines file extensions when selecting files during a filtered file iteration.

> **ECakePolicyExtMatchMode**

{{ read_csv(csv_policy('ExtMatchMode')) }}

--8<-- "ad-file-extension-classification.md"

In `Exact` mode, a file's extension is compared against every entry in the extension set and a match occurs only if the extension is exactly equal to an entry. 

```
Example: Exact (Failure)
    File Extension Set: [".json", ".cdr.txt", ".jpg"]
    File Extension: ".txt"
```
In the example above, `.txt` will fail to match because no entry in the set is exactly `".txt"`.

```
Example: Exact (Success)
    File Extension Set: [".json", ".cdr.txt", ".txt"]
    File Extension: ".txt"
```
In the example above, `".txt"` will match since `".txt"` is an entry in the set.

In `Relaxed` mode, a file's extension is compared in two passes:

1.  If the file's extension is a multi extension, the multi extension is compared against the set. If the multi extension is found in the extension set, the file is selected.
1.  Otherwise the the file's single extension is compared against the set. If the single extension matches an entry in the set, the file is selected.

```
Example: Relaxed (Failure)
File Extension Set: [".json", ".txt.dat", ".txt.bin"]
File Extension: ".bin.txt"
```
In the example above, step one will fail to match because `".bin.txt"` is not in the extension set.
On step two `".bin.txt"` will be converted into its single form `".txt"`. `.txt.` will fail to match since it does not exist in the set.

```
Example: Relaxed (Success)
File Extension Set: [".json", ".txt"]
File Extension: ".bin.txt"
```
In the example above, step one will fail to match because `".bin.txt"` is not in the extension set.
On step two `".bin.txt"` will be converted into its single form `".txt"`. `.txt.` will match since it is in the extension set and the file will be selected.

## DeleteFile
DeleteFile determines whether a file delete operation is allowed to delete a file marked as read-only.

> **ECakePolicyDeleteFile**

{{ read_csv(csv_policy('DeleteFile')) }}

## ExtFilterClone
ECakePolicyExtFilterClone is used in {{ link_cakedir() }} clone operations, and lets a user control whether or not the source directory's {{ link_extfilter('file extension filter') }} is also cloned. 

> **ECakePolicyExtFilterClone**

{{ read_csv(csv_policy('ExtFilterClone')) }}

## CharEncoding
Determines which character encoding to use when writing text data to files.

> **ECakePolicyCharEncoding**

{{ read_csv(csv_policy('CharEncoding')) }}