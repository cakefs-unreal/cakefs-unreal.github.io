## CakeFS API Patterns

### Struct Parameter Packs
#### Default Settings

### Naming Patterns
There are some general naming patterns that have been established for CakeFS in order to establish greater regularity across interfaces and enhance API discoverability. 

#### Reserved IO Function Verbs
The following verbs are only used in functions that involve IO operations: Create, Read, Write, Append, Delete, Copy, Move, Change, and Query. If a function name includes any of these verbs, it is safe to assume that it involves an IO operation. 

#### Common Function Verbs
Build / Clone

Steal instead of Move