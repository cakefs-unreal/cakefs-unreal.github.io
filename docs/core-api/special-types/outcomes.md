## Overview
{{ src_loc_group('Outcomes', 'CakeOutcomes')}}

Outcomes are special enums that represent the final outcome of a desired IO operation. They are used to give enhanced context about the final outcome of an IO operation.

## IO Outcomes
There are two outcome types for IO operations: one for file operations and one for directory operations. Before we examine each outcome type, we must first cover two common values that these outcome types share.

### Ok and No Op
Both file and directory outcome types have two values that do not indicate an actual error: `Ok` and `No Op`. It is important to understand the difference between these two outcomes.

> **Ok**: The IO operation was executed and encountered no errors.

> **No Op**: The IO operation was skipped because it would have resulted in no effect.

The primary reason `NoOp` exists is so that callers can know whether or not an IO operation _actually occurred_. It is up to the caller to determine whether or not distinguishing between `Ok` and `NoOp` is important. For example, if we want to delete a file, we might decide that we don't care whether or not the delete operation actually occurred, and all we actually care about is that the file does not exist on the filesystem. In this case, we can consider `Ok` and `NoOp` as identical. As another example, let's say that we are allowing users to append text data to a file via a GUI. In this situation, we might decide to check for `NoOp`, which is generated whenever an append operation is sent empty data. Not all IO operations will generate a `NoOp`. Refer to the {{ link_errormap() }} to know the possible outcomes each IO operation can generate.

### ECakeOutcomeFileIO
This is the outcome value that is dedicated to represent outcomes associated with IO operations involving an individual file.

{{ read_csv(open_csv_by_typename('ECakeOutcomeFileIO')) }}

### ECakeOutcomeDirIO
This is the outcome value that is dedicated to represent outcomes associated with IO operations involving an individual directory.

{{ read_csv(open_csv_by_typename('ECakeOutcomeDirIO')) }}

### File / Directory Name Sanitization
Both file and directory outcomes have a value that represents an invalid file or directory name. Right now this value is returned only in functions that involve changing the file or directory name, and it is returned when the new file/directory name is empty or contains only whitespace and/or path separators. __There is no platform specific validation that occurs regarding illegal characters in paths.__  

### FailedDeletingPreexisting
While most outcomes are self-explanatory, this particular outcome value could benefit from a little extra explanation. This outcome can occur when the user runs an IO operation that allows preexisting items to be overwritten by the IO operation. In the event that an item already exists at the destination path, the IO operation will attempt to first delete that item in order to ensure the main IO operation can proceed. If the item at the destination path cannot be deleted, this value is returned.

## Directory Traversal Outcomes
!!! note
    This section deals with directory traversal. If you are unfamiliar with this concept, please see [this section](/core-api/directories/#directory-traversal).

The following outcome enums are used to represent the result of directory traversal. 

### Did Not Launch
All traversal outcomes have a value to indicate that a traversal operation failed to start. It is important to understand the contexts that can cause a traversal to fail to start:

1. **The source directory does not exist.**
When a traversal is called on a CakeDir object, that traversal operation will first ensure that the directory it represents actually exists on the filesystem. If it does not, the traversal will fail to launch.

2. **A [filtered traversal](/core-api/directories/#filtered-traversals) is called on a CakeDir object when its extension filter is empty.** 
This would visit files in a way that the caller does not want, and so the traversal will fail to launch.

3. **A policy argument with an out of range value was submitted.**
All CakeFS policies are enums, so out of range issues should be quite rare. The only way these are able to occur is by casting integer values to the policy type. When an out of range policy argument is encountered, the traversal will fail to launch.

!!! tip
    If CakeFS logging is enabled, it will describe the error that prevented the traversal from launching.

### ECakeOutcomeTraversal
This outcome value is used by both unguarded and guarded traversal styles. 

{{ read_csv(open_csv_by_typename('ECakeOutcomeTraversal')) }}

### ECakeOutcomeSearch
This outcome value is used only by search traversals. 

{{ read_csv(open_csv_by_typename('ECakeOutcomeSearch')) }}

## Advanced Outcomes

### ECakeOutcomeDirWork
This outcome value that is used by higher level functions that perform some work on elements within a source directory. Used extensively in [CakeMix](/core-api/cake-mix/) functions.

{{ read_csv(open_csv_by_typename('ECakeOutcomeDirWork')) }}

### ECakeOutcomeBatchOp
This outcome value that is used by CakeFS Async's [batch operations](/core-api/async-io/#batch-operations).

{{ read_csv(open_csv_by_typename('ECakeOutcomeBatchOp')) }}