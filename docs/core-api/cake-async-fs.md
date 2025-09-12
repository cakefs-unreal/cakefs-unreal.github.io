## CakeAsyncFS Overview
CakeFS offers asynchronous versions for most of the core filesystem operations, including CakeMix operations. The usage of these asynchronous functions is similar to the synchronous functions, but with a few changes. This documentation will not exhaustively cover each function, since the functions behave identically to their synchronous counterparts, with the exception that they are executed in an asynchronous context. Instead, this documentation will focus on the differences between the synchronous / asynchronous interfaces and provide a few examples involving them. Finally, there are a few special interfaces unique to CakeFS Async which will be covered.

--8<-- "warning-lib-advanced.md"

### Accessing CakeAsyncFS Interfaces
=== "C++"

    The C++ interfaces for asynchronous IO are contained within the `CakeFS Async` namespace.
    !!! note
        All CakeFS Async interfaces can be found in the following header:
        ```c++
        #include "CakeFS/Async/CakeFS Async.h"
        ```

    It is important to understand that CakeFS Async is not meant to be the single solution for any asynchronous code involving CakeFS objects and interfaces. This is a key difference between the C++ and Blueprint APIs for CakeFS Async. Blueprint offers much less options to its users for asynchronous interactions, whereas asynchronous code in C++ is complicated and Unreal Engine offers many different approaches for multithreaded execution. Being a general purpose API it cannot meet every requirement for every user and thus developing your own implementation often can be the correct solution since it will give more control over error handling, performance, and other characteristics. Using the core CakeFS objects and interfaces in an asynchronous context is quite straightforward since the objects are lightweight and easy to pass by value. The source code for CakeAsyncFS can also be viewed as a reference point when developing your own async implementations.

=== "Blueprint"
    CakeFS provides async functionality in the form of latent Blueprint nodes. As with any Blueprint latent node we can only use these nodes in event graphs:
	
    {{ bp_img_async('Async Node Example') }}
	
	Typing "CakeAsync" in an action window will show us every async function available to us:

    {{ bp_img_async('Async Suite Keyword') }}
	
	A more precise way to filter is to drag off the node of a relevant Cake object, such as a CakeFile, and then type "Async" to find all the async nodes related to that object:

    {{ bp_img_async('CakeFile Async Suite Example') }}

### Key API Differences
While much of the asynchronous interfaces mirror their synchronous counterparts, there are some key differences. It is important to learn these differences before we look at specific usage examples.

=== "C++"
    >Async Function Return Type

    All Async functions return an `FCakeAsyncTask`, which is just a minimal type wrapper that contains the Unreal `TTask` type utilized by CakeFS Async:

    ```c++
    struct FCakeAsyncTask
    {
        UE::Tasks::TTask<void> Task{};

        FORCEINLINE operator bool() { return Task.IsValid(); }
    };
    ```

    Sometimes callers might want to cache the Task, but often we just need to know whether the task launched successfully. To check this, we just need to ensure that the inner `TTask`'s IsValid() member function returns true. Operator bool has been defined to return this so that we can use simple code forms like: 

    ```c++

    if (!AsyncCakeFS::SomeAsyncFunction()) 
	{  
		UE_LOG(LogTemp, Error, TEXT("Some function failed to launch!")); 
	}

	// Equivalent to
	FCakeAsyncTask Task{ AsyncCakeFS::SomeAsyncFunction() };
	if (!Task.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("Some function failed to launch!")); 
	}
    ```

    !!! note
        `TTask` is defined in `Tasks/Task.h`

    >Async Function Signatures

    The function signatures for async IO operations follow a regular pattern. As mentioned earlier, all functions return `FCakeAsyncTasks`. Any types that the synchronous IO operation would return instead will be supplied via parameters to a callback that is invoked when the async operation is done. 
    
    The parameter lists will follow a standard ordering: if there is a target object (e.g., the file for a move operation), the target object is the first parameter. Next, all non-optional parameters used by the IO operation will be listed. The last non-optional parameter will always be the async specific callback invoked when the async operation is done. Generally this callback will also pass back the results of the operation, which will vary in type based upon the operation being used. The first _optional_ parameter in an asynchronous function signature will be an [FCakeSettingsAsyncTask](/core-api/special-types/settings/#fcakesettingsasynctask). We can use this to customize the behavior of the asynchronous operation. Finally, if there are any remaining _optional_ parameters that the IO operation takes they will be listed after the settings struct.

    Let's look at an example by comparing CakeDir's `CreateDir` signature versus the CakeFS Async `CreateDir` signature: 

    ```c++
	// CakeDir 
	[[nodiscard]] FCakeResultDirIO  CreateDir(
		ECakePolicyMissingParents MissingParentPolicy = CakePolicies::MissingParentsDefault
	) const;

	// CakeFS Async 
	[[nodiscard]] FCakeAsyncTask CreateDir(
		FCakeDir SourceDir, 
		FCakeAsyncDoneDirIO TaskDoneCallback, 
		FCakeSettingsAsyncTask TaskSettings = {},
		ECakePolicyMissingParents MissingParentPolicy =
			CakePolicies::MissingParentsDefault
	);
    ```

    Let's compare the differences of the parameter lists. Since `CreateDir` is a member function on an `FCakeDir` object, the async variant needs the object it should call `CreateDir` on as the first parameter. Secondly, we need to provide a callback, which is a delegate that will receive the `FCakeResultDirIO` returned from the `CreateDir` operation. There are no required parameters for CakeDir's `CreateDir` function, and so the first optional parameter in CakeFS Async's `CreateDir` function is the async settings struct. The last parameter is the optional missing parents policy parameter used by CakeDir's `CreateDir`.

    Let's try calling both the synchronous and asynchronous versions using the same FCakeDir object. For this example, we will assume that the default values for all optional parameters are acceptable.

    ```c++
	FCakeDir GameDir{ FCakePath{TEXTVIEW("X:/cake-arena")} };

	auto ReportCreateDirResult = [](FCakeResultDirIO DirResult)
	{
		UE_LOG(LogTemp, Warning, 
			TEXT("CreateDir Result: [%s]"), *DirResult.ToString());
	};

	// Synchronous Version
	ReportCreateDirResult(GameDir.CreateDir());

	// Asynchronous Version
	if (!CakeFS Async::Dir::CreateDir(
		GameDir,
		FCakeAsyncDoneDirIO::CreateLambda(ReportCreateDirResult)))
	{
		UE_LOG(LogTemp, Warning,
			TEXT("AsyncCreateDir failed to launch!"));
	}

    ```

=== "Blueprint"
	>Task Priority

	Every CakeFS async node has a Task Priority parameter. This is an `ECakeTaskPriority`, which is an enum that partially mirrors a native Unreal enum:

    {{ bp_img_async('Cake Task Priority') }}
	
	This priority helps the Unreal Task system scheduler select when the task should be run. In many situations, you probably won't have to change this from the default value of Normal. If you have a task that isn't a high priority, you can use one of the `Background` settings to defer the task to a lower priority. Use profiling to help inform and guide your decisions about which priority works best for your situation.

	The priority order from highest to lowest is as follows:

	1. High
	1. Normal
	1. Background High
	1. Background Normal
	1. Background Low

	> Failure to Launch

	Every async node can fail to properly launch its async task due to some form of invalid arguments. Usually this occurs when a user sends in an invalid reference or forgets to submit a valid callback. When an async node fails to launch, the OnTaskLaunchFailure path will be taken. Assuming the task launches successfully, the associated Complete path will be taken when the async operation resolves:

    {{ bp_img_async('Async Task Launch Failure') }}
	
	!!! tip
		If you have CakeFS logging enabled, you will get a warning that gives more context regarding why the task could not be launched.

## Safely using CakeAsyncFS
The following two sections are provided to ensure that users who are unfamiliar with asynchronous code can get a general idea about how to safely consider and leverage the CakeAsyncFS. If you are an advanced C++ programmer, these are sections that likely can be skimmed over quickly. If you are a Blueprint programmer, please pay careful attention. CakeFS's goal is to provide as much parity with the C++ interfaces as possible, and as such it offers some powerful constructs for Blueprint programmers; however, these constructs can easily get you into trouble if you don't wield them carefully, so it is critical to understand the general expectations upon which the API was designed.

### Understanding the costs of asynchronous code
Asynchronous code can offer better performance and the appealing prospect of non-blocking calls, but it comes at a cost of code complexity and introduces a class of bugs that are incredibly hard to identify and fix. Because of this, you must carefully assess the benefits that an asynchronous interface are offering you before you commit to using them. Once you are certain you want to use an asynchronous interface, always choose the simplest and safest way to express the problem, and only pursue a more complicated solution if profiling results demand it. Being clever here can get you into far more trouble than you imagined; keep it simple and as easy as possible to reason about. Finally, do not assume that asynchronous code will outperform synchronous code. Always profile and measure! Your intuition is rarely right.

### General safety guidelines
In general, the lifetimes of any parameters do not have be carefully considered, since the CakeAsyncFS interfaces always take their own copies. However, in any async operation that involves a user-supplied callback, **it is the user's responsibility to ensure that any data captured or used by that callback is used in a threadsafe manner**. This is especially important when using the async Blueprint interfaces, as Blueprint users will have fewer options to ensure thread safety. It is vital to ensure that nothing else can read or write to any variables that are being used while the asynchronous operation is occurring. 

The following async interfaces include user supplied callbacks that are invoked in an asynchronous context:
	* Directory Traversal callbacks
	* Gather Custom callbacks
	* Batch Operation callbacks

### Async callback guidelines
Async callbacks have a few constraints that must be considered in both C++ and Blueprint:
1) UObjects cannot be created within the async callback. UObjects can only be created on the Game Thread.
2) Many common functions must be called from the game thread -- this is especially true for gameplay related code and anything involving widgets / Slate. If you invoke these functions from another thread you will likely trigger a crash. In general, avoid any gameplay related updates from async callbacks, and also do not update the UI from within the async callbacks. When CakeFS offers progress updates (such as Batch Operations), you can configure them to be called from the game thread to enable easy UI updates. Blueprint progress updates only are called from the game thread for the sake of simplicity.
3) Always check the validity of any UObjects before using them from the async callback.

There are a few basic guidelines that can dramatically improve the safety and reliability of async operations. 

1) Whenever possible, favor using Gather operations in conjunction with Batch operations. This relieves the caller of doing any container maintenance or upkeep, and reduces the amount of areas where asynchronous code must occur. Furthermore, batch operations offer a version that includes a progress report, which will default to sending its reports to the Game thread, which makes displaying the progress of a batch operation seamless and feel much like a synchronous call.

2) When writing asynchronous callbacks, keep as much data local to the callback function as possible. This reduces the amount of variables you have to keep threadsafe.

3) When writing to data outside of an asynchronous callback (e.g., the calling class), ensure that this data is private and the callback's owner can safely keep others from viewing / writing to that data. 

4) When writing asynchronous Directory Traversal, try to ensure that the traversal callback requires no external state to accomplish its goals.


## Async Examples
### File IO
Let's examine async file IO using the async version of CakeFile's `DeleteFile`. Since we are using the asynchronous function which is not a member function, we need to pass the CakeFile object as the first argument to the async version.
=== "C++"
    The namespace CakeFS Async::File contains asynchronous versions of all the [FCakeFile IO Operations](/core-api/files/#io-operations).

    The result callback signature for file IO requires one parameter: an [FCakeResultFileIO](/core-api/special-types/results/#fcakeresultfileio) that the IO operation returned.

    ```c++ hl_lines="11-13"
	FCakeFile FileItemsDb{ 
		FCakePath{ TEXTVIEW("X:/cake-arena/items/potions.db") } 
	};

	auto ReportDetails = [](FCakeResultFileIO DeleteResult) -> void
	{
		UE_LOG(LogTemp, Warning, TEXT("Result of the file deletion operation: [%s]"),
			*DeleteResult.ToString())
	};

	if (!CakeFS Async::File::DeleteFile(
		FileItemsDb,
		FCakeAsyncDoneFileIO::CreateLambda(ReportDetails)))
	{
		UE_LOG(LogTemp, Warning,
			TEXT("AsyncCreateDir failed to launch!"));
	}
    ```

	Before moving on, we should also note that reading file data is slightly different with CakeFS Async.
    To keep lifetime management simple, only the read interfaces which return [TCakeOrderFile](special-types/cake-orders.md#tcakeorder) types are supported.

    Let's look at a brief example using `ReadTextFile`:

    ```c++
    FCakeFile FileReadme{ 
		FCakePath{ TEXTVIEW("X:/cake-arena/readme.txt") } 
	};

	auto OnReadTextComplete = [](TCakeOrderFile<FString> ReadText) -> void 
	{
		if (ReadText)
		{
			UE_LOG(LogTemp, Warning, TEXT("Readme file data: [%s]"),
				*ReadText.Order);
		}
	};

	CakeFS Async::File::ReadTextFile(
		FileReadme, 
		FCakeAsyncDoneFileReadText::CreateLambda(OnReadTextComplete)
	);
    ```

=== "Blueprint"
    {{ bp_img_async('Async Example File DeleteFile') }}

### Directory IO
In this example, we'll use an async version of `DeleteDir` to delete the directory our CakeDir object references.

=== "C++"
    The namespace `CakeFS Async::Dir` contains asynchronous versions of all the [FCakeDir IO Operations](/core-api/directories/#io-operations).

    The result callback signature for directory IO requires one parameter: an [FCakeResultDirIO](../core-api/special-types/results.md#fcakeresultdirio) that the IO operation returned.

    ```c++
	FCakeDir DirItems{ 
		FCakePath{ TEXTVIEW("X:/cake-arena/items") } 
	};

	auto OnDeleteDirComplete = [](FCakeResultDirIO DeleteResult) -> void
	{
		if (DeleteResult)
		{
			UE_LOG(LogTemp, Warning, TEXT("The directory was successfully deleted!"));
		}
		else
		{
			UE_LOG(LogTemp, Error, TEXT("Failed deleting directory: [%s]"),
				*DeleteResult.ToString())
		}
	};

	if (!CakeFS Async::Dir::DeleteDir(
		DirItems,
		FCakeAsyncDoneDirIO::CreateLambda(OnDeleteDirComplete)))
	{
		UE_LOG(LogTemp, Error,
			TEXT("AsyncCreateDir failed to launch!"));
	}
    ```

=== "Blueprint"	
    {{ bp_img_async('Async Example Dir DeleteDir') }}

### File / Directory IO Pitfalls
CakeFS Async interfaces use their own private copy of source objects in order to eliminate many potential lifetime problems, and this has important implications in IO operations that change the path information on file or directory objects. Normally, when a move or change name operation (e.g., `MoveFile` or `ChangeDirName`) succeeds, the associated object automatically updates its path information. However, since a copy of the source object is used in asynchronous contexts, this means that your source object will __not__ update itself when the operation occurs. __Therefore, if you plan on using an object after an async move / change name operation, you must update the path information manually.__

!!! info
	Remember to check the move result via `IsOkStrict` instead of just `IsOk`, since a move operation can return a `NoOp` in certain situations, and we only want to update the path information if a move actually occurred.


=== "C++"

    ```c++ hl_lines="11-14"
	FCakeFile FileItemsDb{ 
		FCakePath{ TEXTVIEW("X:/cake-arena/items/items.db") } 
	};
	FCakePath DestDir{ TEXTVIEW("Y:/cake-archive/items/") };

	auto OnAsyncMoveComplete = 
		[FileItemsDb, DestDir] (FCakeResultFileIO MoveResult) mutable -> void
	{
		if (MoveResult.IsOkStrict())
		{
			FCakePath NewPath{ 
				FileItemsDb.GetPath().CloneWithNewParent(DestDir) 
			};
			FileItemsDb.SetPath(NewPath);

			UE_LOG(LogTemp, Warning, TEXT("New file path is: [%s]"),
				*FileItemsDb.GetPathString());
		}
		else
		{
			UE_LOG(LogTemp, Error, TEXT("Failed moving file: [%s]"),
				*MoveResult.ToString())
		}
	};

	if (!CakeFS Async::File::MoveFile(
		FileItemsDb,
		DestDir,
		FCakeAsyncDoneFileIO::CreateLambda(OnAsyncMoveComplete)))
	{
		UE_LOG(LogTemp, Warning,
			TEXT("AsyncMoveFile failed to launch!"));
	}
    ```
=== "Blueprint"
    {{ bp_img_async('Async Pitfalls Path') }}

### Directory Traversal
Asynchronous directory traversal is quite similar to synchronous traversal, but we must always remain cognizant of the fact that our traversal callback is being invoked on a different thread. This means that all sorts of wonderful thread-related nightmares can befall upon us, so we must be vigilant when we choose to use this asynchronous traversal.

If you need a refresher on how to safely write async callbacks, refer back to the [async callback guidelines](#async-callback-guidelines) section of this documentation.

We'll now look at two examples, one involving unguarded traversal and the other involving search traversal. Our unguarded traversal will simply print the directory names it encounters, and our search traversal will look for a readme file and stop immediately once the first file that matches our criteria is found. 

=== "C++"
    All async traversal operations are contained in namespace CakeFS Async::Dir.


    As with our File / Directory IO result callbacks, traversal callbacks just require one parameter, which is the associated result type for that traversal style. This means [FCakeResultTraversal](../core-api/special-types/results.md#fcakeresulttraversal) for unguarded / guarded traversals, and [FCakeResultSearch](../core-api/special-types/results.md#fcakeresultsearch) for search traversals.

    ```c++
	FCakeDir DirItems{ 
		FCakePath{ TEXTVIEW("X:/cake-arena/items") } 
	};

	auto OnTraversalComplete = [](FCakeResultTraversal ResultTraversal) -> void 
	{
		UE_LOG(LogTemp, Warning, TEXT("Traversal Result: [%s]"), *ResultTraversal.ToString());
	};

	CakeFS Async::Dir::TraverseSubdirs(
		DirItems, ECakePolicyOpDepth::Deep,
		[](FCakeDir NextDir) -> void {
			UE_LOG(LogTemp, Warning, TEXT("Found subdir: [%s]"), *NextDir.CloneDirName())
		},
		FCakeAsyncDoneTraversal::CreateLambda(OnTraversalComplete)
	);


	auto OnSearchComplete = [](FCakeResultSearch ResultSearch) -> void 
	{
		UE_LOG(LogTemp, Warning, TEXT("Search Result: [%s]"), *ResultSearch.ToString());
	};

	CakeFS Async::Dir::TraverseSearchFiles(
		DirItems, ECakePolicyOpDepth::Deep,
		[](FCakeFile NextFile) -> ECakeSignalSearch {

			FString FileName{ NextFile.CloneFileName() };
			if (FileName.Contains(TEXT("readme")))
			{
				UE_LOG(LogTemp, Warning, TEXT("Readme File found at: [%s]"),
					*NextFile.GetPathString());
				return ECakeSignalSearch::Success;
			}
			return ECakeSignalSearch::Continue;
		},
		FCakeAsyncDoneSearch::CreateLambda(OnSearchComplete)
	);
    ```

=== "Blueprint"
	First we'll look at the guarded traversal. This is the callback we'll be using:

    {{ bp_img_async('Async Traversal Guarded Callback') }}

	And here is how we would execute this traversal:

    {{ bp_img_async('Async Traversal Guarded Launch') }}

	Now, let's look at our search traversal callback:

    {{ bp_img_async('Async Traversal Search Callback') }}

	And this is how we would launch the search:

    {{ bp_img_async('Async Traversal Search Launch') }}

### CakeMix
CakeFS Async provides asynchronous versions of all of the [CakeMix](/core-api/cake-mix/) IO functions. For our example, we'll use the async version of `CountSubdirs`.

=== "C++"
    Async versions of CakeMixLibrary functions are located under the namespace `CakeFS Async::CakeMix`. The CakeMixLibrary namespace is mirrored underneath, so if a function is located in `CakeMixLibrary::Dir`, then the async function is found in `CakeFS Async::CakeMix::Dir`.

    Since the `Count` interfaces return an `FCakeMixCount` our callback's parameter will need to be of the same type.

    ```c++
	FCakeDir DirCakeArena{ FCakePath{TEXTVIEW("X:/cake-arena/")} };

	auto OnCountSubdirsComplete = [](FCakeMixCount CountSubdirs) -> void 
	{
		if (CountSubdirs)
		{
			UE_LOG(LogTemp, Warning, TEXT("We have [%d] subdirectories in our main directory!"),
				CountSubdirs.Count);
		}
	};

	CakeFS Async::CakeMix::Dir::CountSubdirs(
		DirCakeArena, ECakePolicyOpDepth::Deep,
		FCakeAsyncDoneDirCount::CreateLambda(OnCountSubdirsComplete)
	);
    ```

=== "Blueprint"
    {{ bp_img_async('Async CakeMix CountSubdirs') }}


## Unique Interfaces

### Batch Operations
A batch operation runs a user-supplied callback on an array of CakeFiles or CakeDirs in an asynchronous context. There are two styles of batch operations supported: one style that reports the overall progress of the operation at each step via an extra callback, and one that does not report any progress.

!!! tip
    By combining some form of Gather/GatherCustom operation with batch processing, one can achieve a wide variety of complex async IO operations in a simple and safe way.

The batch operation callback has the same signature as a traversal callback, except that it returns a [BatchOp](../core-api/special-types/signals.md#ecakesignalbatchop) signal, which allows the caller to halt batch operations early if errors are encountered.

If you want to get progress updates as the batch operation proceeds, use the WithProgress variants of the batch operations. These require the caller supply an extra callback which will receive the operation updates. This callback will receive the following information: an integer representing the number of items already processed, an integer representing the total number of items to process, and a float representing the percentage complete the operation is.

Now let's take a look at a concrete example in order to strengthen our understanding.

=== "C++"
    The batch operation API is defined in the namespace `CakeAsyncFS::BatchOp`.

    We have four functions in this namespace: `RunBatchOpFile`, `RunBatchOpDir`, `RunBatchOpFileWithProgress`, and `RunBatchOpDirWithProgress`. 

=== "Blueprint"
	There are four async nodes we can use to run a batch operation: `RunBatchOpFile`, `RunBatchOpDir`, `RunBatchOpFileWithProgress`, and `RunBatchOpDirWithProgress`.

    {{ bp_img_async('Async Batch Op Node Suite') }}

#### Batch Operation Example
For our example we'll make a simple action callback used on a batch of files. We'll keep things simple and just read the text data from each file, and we'll halt the batch early if any of the read operations fail.

Let's first start by defining our callback:
=== "C++"
	```c++
	auto FileBatchAction = [](FCakeFile NextFile) -> ECakeSignalBatchOp
	{
		if (TCakeOrderFile<FString> ReadText = NextFile.ReadTextFile())
		{
			UE_LOG(LogTemp, Warning, TEXT("[%s] data: [%s]"), *NextFile.CloneFileName(), *ReadText.Order);
			return ECakeSignalBatchOp::Continue; 
		}
		else 
		{ 
			return ECakeSignalBatchOp::Abort; 
		}
	};
	```	
=== "Blueprint"
    {{ bp_img_async('Async Batch Op Callback') }}

With our callback ready, let's launch a batch operation. To start a batch operation, we need to have an array filled with the target CakeFS objects that we want to to be processed. In our case, we need an array of CakeFile objects. Let's pretend we've already gathered a selection of relevant files. Remember, CakeMix's Gather/GatherCustom functions pair exceptionally well with batch operations because they generate an array of CakeFiles or CakeDirs.

When a batch operation completes, we will receive an [FCakeResultBatchOp](../core-api/special-types/results.md#fcakeresultbatchop). This is a simple result type that wraps an [ECakeOutcomeBatchOp](../core-api/special-types/outcomes.md#ecakeoutcomebatchop) and also includes a field that indicates the total number of batch elements that were processed.

=== "C++"
	First we need to make the done callback for this operation. As mentioned earlier, this needs to receive an FCakeResultBatchOp as a parameter. 

	```c++
	auto OnBatchOpComplete = [](FCakeResultBatchOp BatchOpResult) -> void
	{
		if (BatchOpResult)
		{
			UE_LOG(LogTemp, Warning, 
				TEXT("Successfully processed [%d] file(s)."),
				BatchOpResult.TotalProcessed
			);
		}
	};
	```	

	All that's left is to get an array of CakeFile objects, and launch our operation:

	```c++
	FCakeMixBatchFiles Files{
		CakeMixLibrary::Dir::GatherFiles(DirCakeArena, ECakePolicyOpDepth::Deep)
	};

	if (Files)
	{
		CakeFS Async::BatchOp::RunBatchOpFile(
			Files.Batch,
			FCakeAsyncBatchActionFile::CreateLambda(FileBatchAction),
			FCakeAsyncDoneBatchOp::CreateLambda(OnBatchOpComplete)
		);
	}
	```

	Finally, here's all the required code in one block:

	```c++
	FCakeDir DirCakeArena{ 
		FCakePath{ TEXTVIEW("X:/cake-arena/") } 
	};

	auto OnBatchOpComplete = [](FCakeResultBatchOp BatchOpResult) -> void
	{
		if (BatchOpResult)
		{
			UE_LOG(LogTemp, Warning, 
				TEXT("Successfully processed [%d] file(s)."),
				BatchOpResult.TotalProcessed
			);
		}
	};

	auto FileBatchAction = [](FCakeFile NextFile) -> ECakeSignalBatchOp
	{
		if (TCakeOrderFile<FString> ReadText = NextFile.ReadTextFile())
		{
			UE_LOG(LogTemp, Warning, TEXT("[%s] data: [%s]"), *NextFile.CloneFileName(), *ReadText.Order);
			return ECakeSignalBatchOp::Continue; 
		}
		else 
		{ 
			return ECakeSignalBatchOp::Abort; 
		}
	};

	FCakeMixBatchFiles Files{
		CakeMixLibrary::Dir::GatherFiles(DirCakeArena, ECakePolicyOpDepth::Deep)
	};

	if (Files)
	{
		CakeFS Async::BatchOp::RunBatchOpFile(
			Files.Batch,
			FCakeAsyncBatchActionFile::CreateLambda(FileBatchAction),
			FCakeAsyncDoneBatchOp::CreateLambda(OnBatchOpComplete)
		);
	}
	```
=== "Blueprint"
    {{ bp_img_async('Async Batch Op Launch') }}

Great! We've successfully run our first batch operation! But what if we want updates that can be used to inform us and other users about the progress of these batch operations? The WithProgress versions of batch operations have us covered. Let's adjust our last example so that it can support progress updates. 

All we need to do is add another callback that takes the following signature: an integer representing the current step of the operation, an integer representing the total total steps, and finally a float that represents the overall progress of the batch operation.

Let's make our progress update callback. For now, we'll just print the progress out to a log.

=== "C++"
	```c++
	auto BatchProgressHandler = [](
		int32 CurrentStep, int32 MaxStep, float PercentComplete) -> void
	{
			UE_LOG(LogTemp, Warning, 
				TEXT("File Batch Progress: %d/%d (%2f)"), 
				CurrentStep, MaxStep, PercentComplete
			);
	};
	```
=== "Blueprint"
    {{ bp_img_async('Async Batch Op Progress Callback') }}

	!!! tip
		The Blueprint progress callbacks are always called from the game thread. This means you can safely update any Slate / UserWidget directly from this callback.

Now, all we need to do is launch the WithProgress version of `RunBatchOpFile`.

=== "C++"
	The C++ version has an extra parameter that allows the caller to choose whether the progress callback is invoked from the same thread as the batch operation or from the game thread. 

    Using the game thread can dramatically simplify the receiving code, especially if you are using that information to inform GUI changes. However, sending progress reports via the game thread incurs extra overhead -- be sure to profile in any performance sensitive contexts.

    ```c++
	enum struct EProgressCbThread : uint8
	{
		/** Use the thread used by the current async process (NEVER guaranteed to be the game thread). */
		AsyncThread,
		/** Use the game thread to report progress. */
		GameThread,

		MAX
	};
    ```

	Here's the code that would launch our progress version of the batch operation:

	```c++
	FCakeMixBatchFiles Files{
		CakeMixLibrary::Dir::GatherFiles(DirCakeArena, ECakePolicyOpDepth::Deep)
	};

	if (Files)
	{
		CakeFS Async::BatchOp::RunBatchOpFileWithProgress(
			Files.Batch,
			FCakeAsyncBatchActionFile::CreateLambda(FileBatchAction),
			FCakeAsyncOpProgress::CreateLambda(BatchProgressHandler),
			CakeFS Async::EProgressCbThread::GameThread,
			FCakeAsyncDoneBatchOp::CreateLambda(OnBatchOpComplete)
		);
	}
	```

	Finally, here's all the code required in a single block:

    ```c++
	FCakeDir DirCakeArena{ FCakePath{TEXTVIEW("X:/cake-arena/")} };

	auto OnBatchOpComplete = [](FCakeResultBatchOp BatchOpResult) -> void
	{
		if (BatchOpResult)
		{
			UE_LOG(LogTemp, Warning, 
				TEXT("Successfully processed [%d] file(s)."),
				BatchOpResult.TotalProcessed
			);
		}
	};

	auto BatchProgressHandler = [](
		int32 CurrentStep, int32 MaxStep, float PercentComplete) -> void
	{
			UE_LOG(LogTemp, Warning, 
				TEXT("File Batch Progress: %d/%d (%2f)"), 
				CurrentStep, MaxStep, PercentComplete
			);
	};

	auto FileBatchAction = [](FCakeFile NextFile) -> ECakeSignalBatchOp
	{
		if (TCakeOrderFile<FString> ReadText = NextFile.ReadTextFile())
		{
			UE_LOG(LogTemp, Warning, TEXT("[%s] data: [%s]"), 
				*NextFile.CloneFileName(), 
				*ReadText.Order
			);
			return ECakeSignalBatchOp::Continue; 
		}
		else 
		{ 
			return ECakeSignalBatchOp::Abort; 
		}
	};

	FCakeMixBatchFiles Files{
		CakeMixLibrary::Dir::GatherFiles(DirCakeArena, ECakePolicyOpDepth::Deep)
	};

	if (Files)
	{
		CakeFS Async::BatchOp::RunBatchOpFileWithProgress(
			Files.Batch,
			FCakeAsyncBatchActionFile::CreateLambda(FileBatchAction),
			FCakeAsyncOpProgress::CreateLambda(BatchProgressHandler),
			CakeFS Async::EProgressCbThread::GameThread,
			FCakeAsyncDoneBatchOp::CreateLambda(OnBatchOpComplete)
		);
	}
    ```
=== "Blueprint"
	{{ bp_img_async('Async Batch Op Progress Launch') }}

And that's it! We now can run async processing of CakeFiles with progress! The process for running batch operations on CakeDirs is exactly the same, with the exception that we use CakeDirs instead of CakeFiles. Remember, Gather / GatherCustom + Batch Processing makes async operations easy and (relatively) painless! Good luck!