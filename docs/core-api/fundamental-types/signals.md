## Overview
{{ src_loc_group('Signals', 'CakeSignals')}}

Signals are a special enum type that are used by various operations that use callbacks. Signals are returned by the callbacks and allow the callbacks to influence the control flow of the associated operation.

## Directory Traversal Signals
These signals are used in [directory traversal](../directories.md#directory-traversal) operations.

### ECakeSignalGuarded
This signal is used to control guarded traversals.

{{ read_csv(open_csv_by_typename('ECakeSignalGuarded')) }}

### ECakeSignalSearch
This signal is used to control search traversals.

{{ read_csv(open_csv_by_typename('ECakeSignalSearch')) }}

## Advanced Signals
These are specialized signals used in higher level, advanced operations.

### ECakeSignalGather
This signal is used in the CakeMix [GatherCustom](/core-api/cake-mix/#gathering-elements-via-custom-predicate) family of functions.

{{ read_csv(open_csv_by_typename('ECakeSignalGather')) }}

### ECakeSignalBatchOp
This signal is used in the CakeFS Async exclusive [Batch Operation](/core-api/async-io/#batch-operations) functions.

{{ read_csv(open_csv_by_typename('ECakeSignalBatchOp')) }}