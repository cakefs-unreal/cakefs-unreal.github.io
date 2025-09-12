## Overview
--8<-- "note-native-only.md"

{{ src_loc_group('Settings', 'CakeSettings')}}

CakeFS uses lightweight structs called Settings to group associated function parameters that are used across multiple functions. These structs help enforce regular argument ordering, reduce the length of function signatures, and provide a single location in source code where defaults can be set. Furthermore, because CakeFS takes advantage of C++20, we can use designated initializer syntax in order to allow for a much more ergonomic handling of optional parameters. 

## Designated Initializers
!!! hint
	For all the gory details about designated initializers and more, please see [this reference](https://en.cppreference.com/w/cpp/language/aggregate_initialization).

Since CakeFS uses C++20, we have access to designated initializers. Designated initializers are a compact and expressive way to create structs, initializing some or all of its members. When we group function parameters into structs, we can use designated initializers at function callsites. There are many benefits to this approach: We can more safely consume parameter lists with consecutive parameters of the same type, we can add clarity to function callsites via more self-documenting code, and we can eliminate much of the tedious boilerplate that can result from default parameters in C++. For these reasons and more, CakeFS uses structs to group parameters whenever possible.     

Let's take a look at some quick examples using designated initalizer syntax to get familiar with it. We'll use FCakeFile's `CreateTextFile` function as our example. Let's look at the function signature:
```c++
[[nodiscard]] FCakeResultFileIO CreateTextFile(
	FStringView FileContent = TEXTVIEW(""),
	FCakeSettingsCreateTextFile CreateSettings = {}
) const;
```

`CreateTextFile` uses a settings struct, CreateTextFile. As we can see, it is given a default value, which is a cryptic `{}` value. This is simply aggregate initialization where the default values of every member field are used. If we look at the definition of FCakeSettingsCreateTextFile, we can see what those would be:

```c++
/** Settings struct used in text file creation IO operations. */
CakeFS_API struct FCakeSettingsCreateTextFile
{
	/** Determines if any missing parents in the file path should be created. */
	ECakePolicyMissingParents MissingParentPolicy{ CakePolicies::MissingParentsDefault };

	/** Determines the character encoding that should be used when writing text data to the file. */
	ECakePolicyCharEncoding CharEncodingPolicy{ CakePolicies::CharEncodingDefault };

};
```

In this case, we can see that `{}` is equivalent to setting `MissingParentPolicy` to `MissingParentsDefault` and `CharEncodingPolicy` to `CharEncodingDefault`.

!!! hint
	Remember, you can change the defaults at both the struct settings definition and the CakePolicies namespace, so you can configure the defaults to whatever best works for your project.


The important thing to remember is that if we just want to use the default settings for a parameter struct, we just need to use `{}`. This can be helpful in situations where we have multiple settings structs and just need to get to a settings struct further down the parameter list. 

Let's use a designated initalizer to specify all of the FCakeSettingsCreateTextFile values explicitly:

```c++ hl_lines="7 8"
FCakeFile ReadmeFile{ FCakePath{TEXTVIEW("X:/cake-arena/readme.md")} };

FCakeResultFileIO CreateTextFile{ 
	ReadmeFile.CreateTextFile(
		TEXTVIEW("This is the readme file!"),
		{
			.MissingParentPolicy = ECakePolicyMissingParents::CreateMissing,
			.CharEncodingPolicy  = ECakePolicyCharEncoding::UTF8
		}
	)
};
```
Designated initializer syntax looks much like an initializer list, except that we explicitly name each member field, prefixed by the `.` character. It should be noted that designated initializers in C++ are supposed to list the members in the same order as their declaration. 

The advantage of designated initializers becomes apparent when we only want to change a single default parameter, leaving the rest to their default values. This time, let's say we want to write a text file and the only thing we want to change is the character encoding. With designated initializers, we can just omit the MissingParentPolicy member field and fill in the CharEncodingPolicy:
```c++
FCakeFile ReadmeFile{ FCakePath{TEXTVIEW("X:/cake-arena/readme.md")} };

FCakeResultFileIO CreateTextFile{ 
	ReadmeFile.CreateTextFile(
		TEXTVIEW("This is the readme file!"),
		{
			.CharEncodingPolicy = ECakePolicyCharEncoding::ANSI
		}
	)
};
```
Now we have a close approximation to keyword arguments in other programming languages. If the two policies contained within our settings struct were just independent parameters, we would have been forced to specify a value for the MissingParentsPolicy even though we just wanted it to maintain its default setting.

One important detail to keep in mind when using designated initializers is that we must keep the order of the members the same as their declaration. If one member is declared before another, we must preserve that order. We can skip members, but we just have to make sure that the members we list maintain the same relative declaration order. Let's look at a quick example:
```c++
struct UserData
{
	int32 WarpCubes   { 0  };
	int32 GoldenKeys  { 3  };
	int32 SilverCoins { 55 };
};

UserData Data = {
	.WarpCubes   =  5,
	.SilverCoins = 33
};
```

Here we skipped specifying a value for GoldenKey, and so its default value of 3 will be used. However, this initializer is still valid, because WarpCubes is declared before SilverCoins.

```c++
UserData Data = {
	.SilverCoins = 33,
	.WarpCubes   =  5
};
```

The example above is not valid, because SilverCoins is not declared before WarpCubes in the definition of the UserData struct. 

## FCakeSettingsNewItem
This settings struct allows users to configure the overwrite and missing parent behavior desired when a new file or directory is created. It contains two Cake Policies as member fields: [OverwriteItems](/core-api/special-types/policies/#overwriteitems) and [MissingParents](/core-api/special-types/policies/#missingparents). 

```c++
struct FCakeSettingsNewItem
{
	/** Determines if the new item can overwrite a prexisting item. */
	ECakePolicyOverwriteItems OverwritePolicy{ CakePolicies::OverwriteItemsDefault };

	/** Determines if any parent directories that don't exist in the new item's destination 
	 path can be created. */
	ECakePolicyMissingParents MissingParentPolicy{ CakePolicies::MissingParentsDefault };

};
```

An example of explicitly setting the CopyItem values using designated initializer syntax:
```c++ hl_lines="12 13"
FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")} };
FCakeDir DirectoryArchive{ FCakePath{TEXTVIEW("Z:/archive")} };

FCakeFile ReadmeFile{ 
	DirectoryGame.BuildChildPath(
		FCakePath{ TEXTVIEW("info/readme.md") })
};

if (!ReadmeFile.CopyFile(
	*DirectoryArchive,
	{
		.OverwritePolicy     = ECakePolicyOverwriteItems::DoNotOverwriteExistingItems,
		.MissingParentPolicy = ECakePolicyMissingParents::CreateMissing
	})
)
{
	UE_LOG(LogTemp, Error, TEXT("Failed copying readme file!"))
}
```

## FCakeSettingsFileHandle
This settings struct contains two fields, one describing the read/write permissions for a file handle, and the other specifying how data should be written to the file. 

```c++
CakeFS_API struct FCakeSettingsFileHandle
{
	ECakeFileOpenMode  OpenMode { ECakeFileOpenMode::Read           };
	ECakeFileWriteMode WriteMode{ ECakeFileWriteMode::OverwriteData };
};
```

### ECakeFileOpenMode
This enum determines how the file should be opened via the file handle.

{{ read_csv(open_csv_by_typename('ECakeFileOpenMode')) }}

### ECakeFileWriteMode
This enum determines how data should be written by the file handle.

{{ read_csv(open_csv_by_typename('ECakeFileWriteMode')) }}

When opening a file handle in read-only mode, the write mode is completely ignored. The easiest way to open a file handle this way is via a [designated initializer](#designated-initializers):
```c++
	TUniquePtr<IFileHandle> ReadOnlyHandle{ 
		SrcOrc.OpenFileHandleUnique({ .OpenMode = ECakeFileOpenMode::Read })
	};
```

## FCakeSettingsExtFilter
This settings struct is utilized by {{ link_cakedir('filtered directory traversals', 'filtered-traversals') }}. It contains two Cake Policies: {{ policy_link('ExtFilterMode') }} and {{ policy_link('ExtMatchMode') }}. 

```c++
struct FCakeSettingsExtFilter
{
	ECakePolicyExtFilterMode FilterMode{ CakePolicies::ExtFilterModeDefault };
	ECakePolicyExtMatchMode  MatchMode { CakePolicies::ExtMatchModeDefault  };
};

```

## Advanced Settings 

### FCakeSettingsAsyncTask
This struct is used whenever we launch an {{ link_cake_async('async') }} task. It lets us set the task priority, task flags, and which thread the completion callback should be called from.

```c++
struct FCakeSettingsAsyncTask 
{
	UE::Tasks::ETaskPriority Priority    { UE::Tasks::ETaskPriority::Normal              };
	UE::Tasks::ETaskFlags    TaskFlags   { UE::Tasks::ETaskFlags::DoNotRunInsideBusyWait };

	//...
};
```

!!! note
	The priority and task flags are types defined by Unreal Engine. ETaskPriority is defined in `Tasks.h`, and `ETaskFlags` is defined in `TaskPrivate.h`.

By default, the task priority will be normal and the flags indicate that the task should not be run in a busy-wait context. Considering these are all IO operations, it is difficult to imagine a scenario where a busy-wait context could be appropriate, but the option remains for callers to set their own flags. General advice here is to use the default settings and only consider changing them if profiling shows a benefit. 

The final member is of type `ECallbackThread`, which is a custom enum defined directly in the FCakeSettingsAsyncTask struct:

```c++
	enum struct ECallbackThread : uint8 
	{
		/** The completion callback should be called in the game thread. */
		CallbackInGameThread,

		/** The completion callback should be called in the thread used by the Async Task. */
		CallbackInAsyncThread
	};
```

Every Cake Async IO operation will require the caller to provide a callback that is invoked when the async IO operation has completed. We can choose to have the completion callback occur in the game thread or in the thread that the async IO operation was run in. 

```c++
struct FCakeSettingsAsyncTask 
{
	ECallbackThread CallbackThread{ ECallbackThread::CallbackInGameThread };
};
```

The default value is to call the completion callback in the game thread, as this can eliminate many complications that arise from callbacks being invoked on a different thread. We can freely update any Slate / Widget GUI without first waiting to return to the game thread, for instance. Use whichever callback style works best for your current context.

There are a variety of convenience static functions that create FCakeSettingsAsyncTask objects with various settings. It is not an exhaustive set of functions, but it covers some common settings you might desire:

```c++
static constexpr FCakeSettingsAsyncTask PriorityNormal_CallbackGameThread() 
{
	return FCakeSettingsAsyncTask(
		UE::Tasks::ETaskPriority::Normal, ECallbackThread::CallbackInGameThread);
}

static constexpr FCakeSettingsAsyncTask PriorityHigh_CallbackGameThread() 
{
	return FCakeSettingsAsyncTask(
		UE::Tasks::ETaskPriority::High, ECallbackThread::CallbackInGameThread);
}

static constexpr FCakeSettingsAsyncTask PriorityNormal_CallbackAsyncThread()
{
	return FCakeSettingsAsyncTask(
		UE::Tasks::ETaskPriority::Normal, ECallbackThread::CallbackInAsyncThread);
}

static constexpr FCakeSettingsAsyncTask PriorityHigh_CallbackAsyncThread() 
{
	return FCakeSettingsAsyncTask(
		UE::Tasks::ETaskPriority::High, ECallbackThread::CallbackInAsyncThread);
}
```