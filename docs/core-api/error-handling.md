## Introduction
One of the primary design goals of CakeFS is to provide enhanced error reporting from IO operations. CakeFS accomplishes this by using {{ link_outcomes('outcome types') }} which are defined for various types of IO operations. The following sections will showcase common usage patterns and idioms for error handling in CakeFS.

### Opt-In Error Handling
Exhaustive error handling is often complex and tedious, and there are many contexts in which exhaustive error handling is not actually necessary. Because CakeFS is intended for use in a variety of circumstances, from in-house editor tools to end-user interfaces, error handling has been designed so that callers are allowed to opt-in to the level of complexity that best suits their current context. There are three main levels of error complexity, ranging from simplest to most complex: **minimal**, **targeted**, and **exhaustive** error handling.

#### Minimal Error Handling
Minimal error handling views a particular IO operation outcome as a simple binary success or failure. This mirrors the original experience when using Unreal's built-in IO operations. In this strategy, we merely branch on a success flag and have two paths: one for the success state, and one for the error state.

#### Targeted Error Handling
While a particular IO operation might generate a large number of outcomes, there can be situations where a particular function is only equipped to handle a subset of those outcomes. In this strategy, we selectively target the possible outcome values that we want to handle.

#### Exhaustive Error Handling
As long as you know the complete list of outcomes a particular IO operation can generate, you can always implement exhaustive error handling whenever necessary. In this strategy, we provide a path for every possible outcome value a particular function can generate.

--8<-- "ad-error-map.md"

## File/Directory IO Error Handling Idioms
!!! note
	If you need a refresher regarding the differences between `Ok` and `NoOp`, please see {{ link_outcomes('this section', 'ok-and-no-op') }}.

For our examples, we are going to use a [CakeFile](files.md) object. However, all of the idioms presented will work with [CakeDir](directories.md) objects. Only the possible outcome values will be different, since directory IO operations are distinct from file IO operations in CakeFS.

File/Directory IO operations will return either an {{ link_results('FCakeResultFileIO', 'fcakeresultfileio') }} or an {{ link_results('FCakeResultDirIO', 'fcakeresultdirio') }} result type, respectively. If you are unfamiliar with result types, please glance over those sections and refer to them as necessary when viewing the following idioms.

The most simple way to deal with these results is to check if the operation succeeded by using the `IsOk` function on the result object. This style is highly ergonomic when we don't need to worry about specific details of failure and just want to know if the IO operation has succeeded. If we want to get a human friendly error string describing the error encountered, we can use the associated `ToString` operation for our result type.

=== "C++"

    ```c++
	FCakeFile FileReadme{ TEXTVIEW("X:/Game/readme.md") };

	FCakeResultFileIO ResultAppend{
		FileReadme.AppendTextFile(TEXTVIEW("--- Cake Arena Readme ---"))
	};

	if (ResultAppend.IsOk())
	{
		UE_LOG(LogTemp, Warning, TEXT("Append text successful!"))
	}
	else
	{
		UE_LOG(LogTemp, Error, TEXT("Append text failed: [%s]"), *ResultAppend.ToString())
	}
    ```

	In C++ we can also use the result types' operator bool which is equivalent to calling `IsOk`. We could achieve the same effect as the example above using this form:

    ```c++
	FCakeFile FileReadme{ TEXTVIEW("X:/Game/readme.md") };

	if (FileReadme.AppendTextFile(TEXTVIEW("--- Cake Arena Readme ---")))
	{
		UE_LOG(LogTemp, Warning, TEXT("Append text successful!"))
	}
	else
	{
		UE_LOG(LogTemp, Error, TEXT("Append text failed."))
	}
    ```

	We've achieved slightly more compact code, but we've lost the context that the result type can provide. Sometimes this might be fine, especially for exploratory / prototype code; however, don't forget that you can also use if-initialization forms to achieve a similar compactness without sacrificing the result type:

    ```c++
	FCakeFile FileReadme{ TEXTVIEW("X:/Game/readme.md") };

	if (FCakeResultFileIO ResultAppend =
		FileReadme.AppendTextFile(TEXTVIEW("--- Cake Arena Readme ---")))
	{
		UE_LOG(LogTemp, Warning, TEXT("Append text successful!"))
	}
	else
	{
		UE_LOG(LogTemp, Error, TEXT("Append text failed: [%s]"), *ResultAppend.ToString())
	}
    ```


=== "Blueprint"
	{{ bp_img_error_handling('Append Is Ok') }}

It's important to note that `IsOk` returns true if the result is either `Ok` or `NoOp`. We can view this as a guarantee that whether any actual IO operation occurred, the filesystem is in the desired state that we want. However, there might be times when we want to know if an IO operation actually did occur. For instance, AppendText can generate a NoOp if we send it an empty string to append to the file. For these situations, we can use `IsOkStrict`, which only returns true if the operation result is `Ok`. When this is true, we can be sure that some meaningful work was actually done. 

=== "C++"

	```c++
	FCakeFile FileReadme{ TEXTVIEW("X:/Game/readme.md") };

	FCakeResultFileIO ResultAppend{
		FileReadme.AppendTextFile(ExternalTextData)
	};

	if (ResultAppend.IsOkStrict())
	{
		UE_LOG(LogTemp, Warning, TEXT("Appended text successfully!"))
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("No text appended: [%s]", *ResultAppend.ToString()));
	}
	``` 
=== "Blueprint"
	{{ bp_img_error_handling('Append Is Ok Strict') }}

We can better understand the context of the Append Text operation if we switch to targeted error handling. In this verison, we'll explicitly handle the Ok and NoOp states, and we'll forward any other errors into a generic error reporting message. The benefit to this approach is that we can clearly identify the cases where the AppendText operation is being sent empty input strings.

=== "C++"
	```c++
	FCakeFile FileReadme{ TEXTVIEW("X:/Game/readme.md") };

	FCakeResultFileIO ResultAppend{
		FileReadme.AppendTextFile(ExternalTextData)
	};

	switch (ResultAppend.Outcome)
	{
		case ECakeOutcomeFileIO::Ok:
			UE_LOG(LogTemp, Warning, TEXT("Appended text successfully!"));
		break;

		case ECakeOutcomeFileIO::NoOp:
			UE_LOG(LogTemp, Warning, TEXT("Empty string submitted, no append necessary."));
		break;

		default:
			UE_LOG(LogTemp, Warning, TEXT("Append text error: [%s]"), *ResultAppend.ToString());
		break;
	}
	``` 

=== "Blueprint"
	{{ bp_img_error_handling('Append Targeted Error Handling') }}

In some situations we need to explicitly handle every possible error from a particular function. When using exhaustive error handling, it's important to check the [error map](../core-api/error-maps/#appendfile-text-binary) for the relevant function in order to avoid writing unnecessary code. Since we're using `AppendTextFile`, we only need to handle `DoesNotExist`, `FailedOpenWrite`, and `FailedWrite`:

=== "C++"

	```c++
	FCakeFile FileReadme{ TEXTVIEW("X:/Game/readme.md") };

	FCakeResultFileIO ResultAppend{
		FileReadme.AppendTextFile(ExternalTextData)
	};

	switch (ResultAppend.Outcome)
	{
		case ECakeOutcomeFileIO::Ok:
			UE_LOG(LogTemp, Warning, TEXT("Appended text successfully!"));
		break;

		case ECakeOutcomeFileIO::NoOp:
			UE_LOG(LogTemp, Warning, TEXT("Empty string submitted, no append necessary."));
		break;

		case ECakeOutcomeFileIO::DoesNotExist:
			UE_LOG(LogTemp, Warning, TEXT("Append failed -- the file does not exist."));
		break;

		case ECakeOutcomeFileIO::FailedOpenWrite:
			UE_LOG(LogTemp, Warning, TEXT("Append failed -- could not open file for writing."));
		break;

		case ECakeOutcomeFileIO::FailedWrite:
			UE_LOG(LogTemp, Warning, TEXT("Append failed -- could write to file."));
		break;

		default:
			UE_LOG(LogTemp, Warning, TEXT("This is a bug in CakeFS, please report it!"));
		break;
	}
	```

=== "Blueprint"
	{{ bp_img_error_handling('Append Exhaustive Error Handling') }}

And that concludes our tour through error handling with file and directory IO operations. Remember, the level of complexity for error handling depends entirely upon your use case. 

## Traversal Error Handling Idioms
--8<-- "ad-traversal.md"

For this section we'll use a search traversal since it is the most complex kind of traversal. Any idioms shown here will work with the other kinds of traversal, but they will just be simpler and have less options.

For our search, our goal is to collect three text files from a given directory. 

=== "C++"
    For our example, we are going to assume the following directory is declared: 

    ```c++
	FCakeDir DesignDocsDir{ FCakePath{TEXTVIEW("X:/cake-arena/design-docs")}, TEXTVIEW("txt") };
    ```

    Furthermore, we are also going to assume the following variables and our search callback are declared as:

    ```c++
	constexpr int32 DesiredFileCount{ 3 };

	TArray<FCakeFile> Files{};
	Files.Reserve(DesiredFileCount);

	auto FindThreeTextFiles =
		[&Files, CurrentCount = int32{ 0 }](FCakeFile NextFile) mutable -> ECakeSignalSearch 
	{
		Files.Emplace(MoveTemp(NextFile));
		++CurrentCount;
		if (CurrentCount >= DesiredFileCount) { return ECakeSignalSearch::Success; }
		return ECakeSignalSearch::Continue;
	};
    ```

	First we'll let the result implicitly convert to `bool` via its `operator bool`. [FCakeResultSearch](special-types/results.md#fcakeresultsearch) only is true if the search was successful, so we can branch on it and then safely use our expected files:

	```c++
	if (DesignDocsDir.TraverseSearchFilesWithFilter(ECakePolicyOpDepth::Deep, FindThreeTextFiles))
	{
		// We have the three files.
		check(Files.Num() == 3);
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("Couldn't get three files. Found [%d] file(s)."), Files.Num())
	}
	```

	Since we didn't store the result type, we can't be sure of what exactly happened with the traversal -- it could have failed to launch or the search itself could have failed. We know it wouldn't have aborted due to an error since we don't have an abort branch in our search callback.

	Let's try storing the result type returned by our traverse operation.

	```c++
	FCakeResultSearch ResultSearch{
		DesignDocsDir.TraverseSearchFilesWithFilter(ECakePolicyOpDepth::Deep, FindThreeTextFiles)
	};

	if (ResultSearch.WasSuccessful())
	{
		// We have the three files.
		check(Files.Num() == 3);
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("Couldn't find necessary files: [%s]."), *ResultSearch.ToString())
	}
	```

	Now that we have stored the result type, we can use its `ToString` function to help give the caller better insight into how the search traversal failed.

	Calling `WasSuccessful` is equivalent to using `operator bool`, so we could also use this equivalent form when checking for search success: 

	```c++
	if (ResultSearch)
	{
		// We have the three files.
		check(Files.Num() == 3);
	}
	```

    Since `WasSuccessful` and `operator bool` are equivalent, we can always use scoped variable declaration for a more compact style if we prefer:

	```c++
	if (FCakeResultSearch ResultSearch = 
		DesignDocsDir.TraverseSearchFilesWithFilter(ECakePolicyOpDepth::Deep, FindThreeTextFiles))
	{
		// We have the three files.
		check(Files.Num() == 3);
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("Couldn't find necessary files: [%s]."), *ResultSearch.ToString())
	}
	```


	It can be beneficial to distinguish between a search failure and the search traversal error states. Let's change our error handling so we know when the search fails, and thus can also identify when the traversal operation itself fails to launch.

	```c++
	if (FCakeResultSearch ResultSearch = 
		DesignDocsDir.TraverseSearchFilesWithFilter(ECakePolicyOpDepth::Deep, FindThreeTextFiles))
	{
		// We have the three files.
		check(Files.Num() == 3);
	}
	else
	{
		switch (ResultSearch.Outcome)
		{
		case ECakeOutcomeSearch::Failed:
			UE_LOG(LogTemp, Warning, 
				TEXT("The target directory does not have at least [%d] text file(s)!"), DesiredFileCount)
			break;
		default:
			UE_LOG(LogTemp, Warning, TEXT("Traversal error: [%s]"), *ResultSearch.ToString())
			break;
		}
	}
	```
	And, for completeness, we can always exhaustively handle every possible outcome:

	```c++
	if (FCakeResultSearch ResultSearch = 
		DesignDocsDir.TraverseSearchFilesWithFilter(ECakePolicyOpDepth::Deep, FindThreeTextFiles))
	{
		// We have the three files.
		check(Files.Num() == 3);
	}
	else
	{
		switch (ResultSearch.Outcome)
		{
		case ECakeOutcomeSearch::Failed:
			UE_LOG(LogTemp, Warning, 
				TEXT("The target directory does not have at least [%d] text file(s)!"), DesiredFileCount)
			break;
		case ECakeOutcomeSearch::DidNotLaunch:
			UE_LOG(LogTemp, Warning, TEXT("The traversal failed to launch."))
			break;
		case ECakeOutcomeSearch::Aborted:
			UE_LOG(LogTemp, Warning, TEXT("The traversal was aborted due to an error."))
			break;
		}
	}
	```

	The case statement for `Aborted` is useless in our scenario since we don't actually return it, but we have included it for completeness. 

=== "Blueprint"
    For our example, we are going to assume the following directory is declared: 

	{{ bp_img_error_handling('Design Doc Dir') }}

	This is the callback we will be using to gather the first three text files found in the target directory:

	{{ bp_img_error_handling('Search Callback Definition') }}

	First, let's look at a minimal error handling example. We can use the `WasSuccessful` function on the search result to see if our search was successful. Since we're trying to gather three text files, we can be certain that a true value for this outcome means we did indeed gather three text files from the target directory.

	{{ bp_img_error_handling('Minimal Error Handling Search') }}

	Just like with CakeFile / CakeDir IO operations, we can use a utility function from [CakeMixLibrary]/core-api/cake-mix/#error-handling) to get a human-readable string of the outcome:

	{{ bp_img_error_handling('Minimal Error Handling Search To String') }}

	By using the minimal error handling approach, we have lost some information. Namely, when a search does not succeed, we can't distinguish between a search failure (the directory doesn't meet the search requirements, i.e., it doesn't have at least three text files in our case) and a traversal error. Search traversal can abort due to IO errors, and furthermore all traversal operations can [fail to launch](special-types/outcomes.md#did-not-launch). 
	
	We'll start by using targeted error handling to allow us to easily distinguish between search failure and error results. First, we will switch on the search outcome value, providing special paths for success and failure. Then we will route the remaining paths back to the generic string error report we used in the prior example:

	{{ bp_img_error_handling('Targeted Error Handling Search') }}


	Finally, we can always use exhaustive error handling and provide an exclusive path for every possible outcome value. In our situation, our callback never returns an Abort signal, so this error path technically doesn't need to be handled. However, we will show a full handling of the outcomes for completeness, and as a reference for those callbacks that do return Abort signals:

	{{ bp_img_error_handling('Exhaustive Error Handling Search') }}

And that concludes a tour of error handling with a search traversal. Remember, the same strategies work for Unguarded and Guarded traversals, but you just have fewer outcome values to deal with since the traversal operations themselves are simpler.