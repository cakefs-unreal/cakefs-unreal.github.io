
## Overview
CakeFS provides CakeFile objects to allow file manipulation in a type-safe and ergonomic manner.

### Source Code Information
=== "C++"
    {{ cpp_impl_source('file', 'FCakeFile', 'CakeFile') }}

=== "Blueprint"
    {{ bp_impl_source('file', 'UCakeFile', 'CakeFile_BP') }}

## Basic Usage
The following covers some of the core interfaces required to utilize and manipulate CakeFile objects.

### Building CakeFile Objects
=== "C++"
	The simplest way to create an **FCakeFile** object is via its constructor, which accepts a single **FCakePath** that holds the path the file.

	```c++ hl_lines="1 5"
	FCakeFile PlayerFile{ FCakePath{ TEXTVIEW("/x/game/data/profiles/player_1.dat") } };

	FCakePath EnemiesDbPath{ TEXTVIEW("C:\\Game\\Data\\Enemies\\enemies_full.db") };

	FCakeFile EnemiesDbFile{ EnemiesDbPath };
	```
=== "Blueprint"
	We can create a new CakeFile object via `BuildCakeFile`, passing a [CakePath](paths.md) that holds the file path the CakeFile should target:

	{{ bp_img_file('Build Cake File') }}

	If we need to make an empty CakeFile object whose path will be determined later, we can use `Build Cake File Empty`:

	{{ bp_img_file('Build Cake File Empty') }}

	!!! tip
		CakeFS offers automatic string to [CakePath](paths.md) conversions. You can pass a string to any function that expects a CakePath argument and it will automatically create a CakePath object from the string for you: 

		{{ bp_img_file('Auto Str Conv') }}

### Accessing the File Path
=== "C++"
	**FCakeFile** stores its full file path internally as an **FCakePath**. We can gain access to that **FCakePath** object via  `operator*` and `GetPath`:


	```c++ hl_lines="7-8"
	auto PrintPath = [](const FCakePath& Path) 
		{ UE_LOG(LogTemp, Warning, TEXT("Path String: [%s]"), **Path); };

	FCakePath EnemiesDbPath{ TEXTVIEW("C:\\Game\\Data\\Enemies\\enemies_full.db") };
	FCakeFile EnemiesDbFile{ EnemiesDbPath };

	PrintPath(*EnemiesDbFile);
	PrintPath(EnemiesDbFile.GetPath());
	```

	If we just need to access the path string itself, we can use the convenience member function `GetPathString`:

	```c++ hl_lines="7"
	auto PrintPathStr = [](const FString& PathStr) 
		{ UE_LOG(LogTemp, Warning, TEXT("Path String: [%s]"), *ExtStr); };

	FCakePath EnemiesDbPath{ TEXTVIEW("C:\\Game\\Data\\Enemies\\enemies_full.db") };
	FCakeFile EnemiesDbFile{ EnemiesDbPath };

	PrintPath(EnemiesDbFile.GetPathString());
	```

	We can check if an **FCakeFile** object's file path is empty via  `PathIsEmpty`:

	```c++ hl_lines="5-6"
	FCakePath EnemiesDbPath{ TEXTVIEW("C:/Game/Data/Enemies/enemies_full.db") };
	FCakeFile EnemiesDbFile{ EnemiesDbPath };
	FCakeFile EmptyFile{};

	const bool bDbFileIsEmpty{ EnemiesDbFile.PathIsEmpty() }; // => false
	const bool bEmptyFile   { EmptyFile.PathIsEmpty()     }; // => true
	```
=== "Blueprint"
	When we need to read a CakeFile's path as a string, we can use `GetPathString`:

	{{ bp_img_file('Get Path String') }}

	If we want a copy of a CakeFile's path as a CakePath, we can use `ClonePath`:

	{{ bp_img_file('Clone Path') }}

	To check if a CakeFile's path is empty, we can use `PathIsEmpty`:

	{{ bp_img_file('Path is Empty') }}

### Modifying the File Path
=== "C++"
	We can change the file path an FCakeFile object represents via `SetPath`, which takes an FCakePath to copy its path.

	```c++ hl_lines="6"
	FCakePath EnemiesDbPath{ TEXTVIEW("C:\\Game\\Data\\Enemies\\enemies_full.db") };
	FCakeFile EnemiesDbFile{ EnemiesDbPath };

	FCakePath NewEnemiesDb{ TEXTVIEW("X:\\Extra\\Enemies\\enemies_new.db") };

	EnemiesDbFile.SetPath(NewEnemiesDb);
	```

	To use move semantics, we can use `StealPath`:

	```c++ hl_lines="6"
	FCakePath EnemiesDbPath{ TEXTVIEW("C:\\Game\\Data\\Enemies\\enemies_full.db") };
	FCakeFile EnemiesDbFile{ EnemiesDbPath };

	FCakePath NewEnemiesDb{ TEXTVIEW("X:\\Extra\\Enemies\\enemies_new.db") };

	EnemiesDbFile.StealPath(MoveTemp(NewEnemiesDb));
	```

	--8<-- "ad-copymove-ctor.md"

	When we want to clear the file path contents of an FCakePath, we can call `ResetPath`:

	```c++ hl_lines="4"
	FCakePath EnemiesDbPath{ TEXTVIEW("C:/Game/Data/Enemies/enemies_full.db") };
	FCakeFile EnemiesDbFile{ EnemiesDbPath };

	EnemiesDbFile.ResetPath();
	const bool bFileIsEmpty{ EnemiesDbFile.PathIsEmpty() }; // => true
	```
	We can pass an optional parameter that can will ensure the internal path buffer is at least as large as the size submitted:

	```c++ hl_lines="5"
	FCakePath EnemiesDbPath{ TEXTVIEW("C:/Game/Data/Enemies/enemies_full.db") };
	FCakePath NewEnemiesDb { TEXTVIEW("X:/Extra/Enemies/enemies_new.db")      };
	FCakeFile EnemiesDbFile{ EnemiesDbPath };

	EnemiesDbFile.ResetPath(NewEnemiesDb.QueryPathString().Len());
	const bool bFileIsEmpty{ EnemiesDbFile.PathIsEmpty() }; // => true
	```
=== "Blueprint"
	To change the file path of an existing CakeFile object, we use `SetPath`:

	{{ bp_img_file('Set Path') }}

	To clear any path in an existing CakeFile object, we use `ResetPath`:

	{{ bp_img_file('Reset Path') }}

    --8<-- "note-bp-newreservedsize.md"

### Accessing the File Name
To get the file name of a CakeFile object as a string, we use `CloneFileName`:
=== "C++"
	```c++ hl_lines="7"
	auto PrintFileName = [](const FString& FileName) 
		{ UE_LOG(LogTemp, Warning, TEXT("File Name: [%s]"), *FileName); };

	FCakePath EnemiesDbPath{ TEXTVIEW("C:\\Game\\Data\\Enemies\\enemies_full.db") };
	FCakeFile EnemiesDbFile{ EnemiesDbPath };

	FString FileName{ EnemiesDbFile.CloneFileName() };
	PrintFileName(FileName);
	```

=== "Blueprint"
	{{ bp_img_file('Clone File Name') }}

!!! info
	There are other functions for generating different versions of a filename (e.g., one without its file extension data). For more information, please see the [File Name Types](#file-name-types) section.

### Accessing the File Extension
To get the file extension from a CakeFile's file path we use `CloneFileExt`, which returns a [CakeFileExt](file-extensions.md) object:
=== "C++"
	```c++ hl_lines="7"
	auto PrintFileExt = [](const FString& FileExt) 
		{ UE_LOG(LogTemp, Warning, TEXT("File Ext: [%s]"), *FileExt); };

	FCakePath EnemiesDbPath{ TEXTVIEW("C:\\Game\\Data\\Enemies\\enemies_full.db") };
	FCakeFile EnemiesDbFile{ EnemiesDbPath };

	FCakeFileExt DbExt{ EnemiesDbFile.CloneFileExt() };
	PrintFileExt(*DbExt);
	```
=== "Blueprint"
	{{ bp_img_file('Clone File Ext') }}

To get the file extension as a string, we can use `CloneFileExtString`:
=== "C++"
	```c++ hl_lines="7"
	auto PrintFileExt = [](const FString& FileExt) 
		{ UE_LOG(LogTemp, Warning, TEXT("File Ext: [%s]"), *FileExt); };

	FCakePath EnemiesDbPath{ TEXTVIEW("C:\\Game\\Data\\Enemies\\enemies_full.db") };
	FCakeFile EnemiesDbFile{ EnemiesDbPath };

	FString DbExt{ EnemiesDbFile.CloneFileExtString() };
	PrintFileExt(DbExt);
	```
=== "Blueprint"
	{{ bp_img_file('Clone File Ext String') }}

### File Equality
File equality mirrors Path equality: two File objects are equal if they refer to the same file on the filesystem.

=== "C++"
	FCakeFile uses `operator==` and `operator!=` for equality comparisons.

	```c++ hl_lines="11-12"
	FCakePath EnemiesDbPath{ TEXTVIEW("C:\\Game\\Data\\Enemies\\enemies_full.db") };
	FCakeFile EnemiesDbFile{ EnemiesDbPath };

	FCakePath ItemsDbPath{ TEXTVIEW("C:/Game/Data/Items/items_full.db") };
	FCakeFile ItemsDbFile{ ItemsDbPath };

	const bool bAreEqual  { ItemsDbFile == EnemiesDbFile }; // => false
	const bool bAreNotEqual{ ItemsDbFile != EnemiesDbFile }; // => true
	```

=== "Blueprint"
	To check if two CakeFile objects are equal, we use `IsEqualTo`:

	{{ bp_img_file('Is Equal To') }}

	To check if two CakeFile objects are not equal, we use `IsNotEqualTo`:

	{{ bp_img_file('Is Not Equal To') }}

## IO Operations
--8<-- "disclaimer-error-handling.md"

--8<-- "ad-policies.md"

### File Existence
To check if a CakeFile exists on the filesystem, we can use `Exists`:
=== "C++"
	```c++ hl_lines="5"
	FCakeFile ItemsDb{ 
		FCakePath{ TEXTVIEW("x/game/data/items.db") } 
	};

	const bool bExists{ ItemsDb.Exists() };
	```
=== "Blueprint"
	{{ bp_img_file('Exists') }}

### Creating Files
CakeFS makes a distinction between writing to a file that does not exist (file creation) and writing to a file that already exists (file writing). The following file creation interfaces are meant to be used when a file does not exist. __These functions will fail if the file already exists on the filesystem.__ If the file already exists, use one of the [Write](#writing-data-to-files) functions instead.

To create a text or binary file, we use `CreateTextFile` or `CreateBinaryFile` respectively.
=== "C++"
	```c++ hl_lines="9 14"
	FCakePath IntDir{ FPaths::ProjectIntermediateDir() };

	FCakeFile FileText  { IntDir / FCakePath{ TEXTVIEW("controls.txt") } };
	FCakeFile FileBinary{ IntDir / FCakePath{ TEXTVIEW("stats.bin")    } };

	FString      SourceDataText  { TEXT("This is the source data.") };
	TArray<uint8> SourceDataBytes{ 0x99, 0x98, 0x97, 0x96           };

	if (!FileText.CreateTextFile(SourceDataText))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed creating example text file."));
	}

	if (!FileBinary.CreateBinaryFile(SourceDataBytes))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed creating example binary file."));
	}
	```

	--8<-- "ad-settings-newitem.md"

=== "Blueprint"
	{{ bp_img_file('Create Text File') }}

	{{ bp_img_file('Create Binary File') }}

If a file already exists, we generally should use the WriteTextFile or WriteBinaryFile interfaces. However, there are convenience functions that will either create the file if it does not exist or overwrite the file if it does exist via `CreateOrWriteTextFile` and `CreateOrWriteBinaryFile`:
=== "C++"
	```c++ hl_lines="9 14"
	FCakePath IntDir{ FPaths::ProjectIntermediateDir() };

	FCakeFile FileText  { IntDir / FCakePath{ TEXTVIEW("controls.txt") } };
	FCakeFile FileBinary{ IntDir / FCakePath{ TEXTVIEW("stats.bin")    } };

	FString      SourceDataText  { TEXT("This is the source data.") };
	TArray<uint8> SourceDataBytes{ 0x99, 0x98, 0x97, 0x96           };

	if (!FileText.CreateOrWriteTextFile(SourceDataText))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed creating example text file."));
	}

	if (!FileBinary.CreateOrWriteBinaryFile(SourceDataBytes))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed creating example binary file."));
	}
	```
=== "Blueprint"
	{{ bp_img_file('Create Or Write Text File') }}

	{{ bp_img_file('Create Or Write Binary File') }}

### Deleting Files
To attempt to delete the file a CakeFile references, we use `DeleteFile`:
=== "C++"
	```c++ hl_lines="3"
	FCakeFile SpellsDb{ FCakePath{TEXTVIEW("abilities/magic/spells.db")} };

	if (!SpellsDb.DeleteFile())
	{
		UE_LOG(LogTemp, Warning, TEXT("Failed to delete [%s]!"), *SpellsDb.CloneFileName());
	}
	```

=== "Blueprint"
	{{ bp_img_file('Delete File') }}

This function has an {{ policy_link('DeleteFile') }} parameter (optional in C++) that determines if read only files can be deleted.

!!! note
	In the event that the file does not exist, `DeleteFile` will return a [No Op](special-types/outcomes.md#ok-and-no-op) outcome value.
   
### File Read/Write Operations
Cake Files provide interfaces for handling files as text files or binary files. Text files will use string-like objects for read/write operations, and binary files will use `TArray<uint8>`.

#### Reading File Data
=== "C++"
	There are two approaches to reading file data from an FCakeFile object. We will explore these approaches through examples of reading a text file. 

	The first approach we can use is reading the file data into a pre-existing buffer:

	```c++ hl_lines="5"
	FCakePath IntDir  { FPaths::ProjectIntermediateDir()               };
	FCakeFile FileText{ IntDir / FCakePath{ TEXTVIEW("controls.txt") } };

	FString TextData{};
	if (FileText.ReadTextFileToBuffer(TextData))
	{
		UE_LOG(LogTemp, Warning, TEXT("Text File Data: [%s]"), *TextData);
	}
	```
	The `ToBuffer` variants of reading file data will return an [FCakeResultFileIO](special-types/results.md#fcakeresultfileio), and the buffer will contain the file data assuming the read operation succeeds.

	!!! tip 
		Reading to a buffer is often the right strategy if you plan to re-use the buffer across multiple reads and want to minimize reallocations. The `ToBuffer` functions ensure that they never shrink the buffer or reset it via move semantics. 

	The other approach is to have the file data and operation result returned in a CakeOrder type via `ReadTextFile`:

	```c++ hl_lines="6"
	FCakePath IntDir  { FPaths::ProjectIntermediateDir()               };
	FCakeFile FileText{ IntDir / FCakePath{ TEXTVIEW("controls.txt") } };

	TCakeOrderFile<FString> ReadText{ FileText.ReadTextFile() };

	if (ReadText.Result.IsOk())
	{
		UE_LOG(LogTemp, Warning, TEXT("Text File Data: [%s]"), *ReadText.Order);
	}
	```
	CakeOrders are simple template structs that bundle a result type with a template type that represents the data we want to receive from an IO operation. In our case, we are using a `TCakeOrderFile` which sends back [FCakeResultFileIO](special-types/results.md#fcakeresultfileio) result types, and our template type is `FString` since we're trying to get the text data as a string. For more details on CakeOrders and how to use them, please see [this section](/core-api/special-types/cake-orders/).

	For completeness, here is the equivalent code for binary files:

	```c++ hl_lines="5 10"
	FCakePath IntDir     { FPaths::ProjectIntermediateDir()         };
	FCakeFile FileBinary { IntDir / FCakePath{TEXTVIEW("data.bin")} };

	TArray<uint8> BinaryDataBuffer{};
	if (FileBinary.ReadBinaryFileToBuffer(BinaryDataBuffer))
	{
		// ... Use the data
	}

	TCakeOrderFile<TArray<uint8>> ReadBinary{ FileBinary.ReadBinaryFile() };
	if (ReadBinary.Result.IsOk())
	{
		// ... Use the data
	}
	```
=== "Blueprint"
	To read a file's data as text, we use `Read Text File`:

	{{ bp_img_file('Read Text File') }}

	To read a file's data as binary data (an array of bytes), we use `Read Binary File`:

	{{ bp_img_file('Read Binary File') }}

#### Writing Data to Files
The writing interfaces are designed to be used on preexisting files whose contents we want to overwrite or append to. __These functions will fail if the file does not exist on the filesystem.__ If the file does not exist, use one of the [Create](#creating-files) functions instead.

To overwrite a file's contents, we can use `WriteTextFile` or `WriteBinaryFile`:
=== "C++"
	```c++ hl_lines="5 10"
	FCakePath IntDir     { FPaths::ProjectIntermediateDir()             };
	FCakeFile FileBinary { IntDir / FCakePath{TEXTVIEW("data.bin")}     };
	FCakeFile FileText   { IntDir / FCakePath{TEXTVIEW("controls.txt")} };

	if (!FileText.WriteTextFile(TEXTVIEW("This will fully overwrite any old data in FileText.")))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed overwriting text in FileText. Aborting.")) 
	}

	if (!FileBinary.WriteBinaryFile( { 0x80, 0x80, 0x80, 0x80 }))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed overwriting data in FileBinary. Aborting.")) 
	}
	```
=== "Blueprint"
	{{ bp_img_file('Write Text File') }}

	{{ bp_img_file('Write Binary File') }}

To append data to a file's contents instead of overwriting it, we can use `AppendTextFile` or `AppendBinaryFile`:
=== "C++"
	```c++ hl_lines="5 10"
	FCakePath IntDir     { FPaths::ProjectIntermediateDir()             };
	FCakeFile FileBinary { IntDir / FCakePath{TEXTVIEW("data.bin")}     };
	FCakeFile FileText   { IntDir / FCakePath{TEXTVIEW("controls.txt")} };

	if (!FileText.AppendTextFile(TEXTVIEW("This will be appended to the end of FileText's data.")))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed appending text to FileText. Aborting.")) 
	}

	if (!FileBinary.AppendBinaryFile( { 0xEA, 0xD }))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed appending data to FileBinary. Aborting.")) 
	}
	```
=== "Blueprint"
	{{ bp_img_file('Append Text File') }}

	{{ bp_img_file('Append Binary File') }}

### Copying Files
We can copy a CakeFile's referenced file to another location via `CopyFile`. This takes an CakePath argument that represents the source directory into which the file should be copied. 
=== "C++"
	```c++ hl_lines="4"
	FCakeFile SpellsDb { FCakePath{TEXTVIEW("abilities/magic/spells.db")} };
	FCakePath ArchiveDir{ FCakePath{TEXTVIEW("/y/archive/spells_backup")}  };

	if (!SpellsDb.CopyFile(ArchiveDir))
	{
		UE_LOG(LogTemp, Warning, TEXT("Failed copying spells database to archive dir."))
	}
	```
	--8<-- "ad-settings-copyitem.md"

=== "Blueprint"
	{{ bp_img_file('Copy File') }}

If we want the copied file to have a file name that differs from the source file, we can use `CopyFileAliased`:
=== "C++"
	```c++ hl_lines="4"
	FCakeFile SpellsDb { FCakePath{TEXTVIEW("abilities/magic/spells.db")} };
	FCakePath ArchiveDir{ FCakePath{TEXTVIEW("/y/archive/spells_backup")}  };

	if (!SpellsDb.CopyFileAliased(ArchiveDir, TEXTVIEW("spells_archive.db")))
	{
		UE_LOG(LogTemp, Warning, TEXT("Failed copying spells database to archive dir."))
	}
	```

	--8<-- "ad-settings-copyitem.md"

=== "Blueprint"
	{{ bp_img_file('Copy File Aliased') }}

In the example above, assuming the copy succeeds, the copied file's path will be `/y/archive/spells_backup/spells_archive.db`.

### Moving Files
It is important to understand that a move is actually a compound IO operation -- a source file is copied to the destination, and then the source file is deleted at its original location. This is important to keep in mind when assessing the outcome values returned by failed moves -- in terms of IO operations, a move could fail during the copy operation or the delete operation, but there is no dedicated outcome for a "move" failure. 

We can move a file to another location via `MoveFile`. This takes an CakePath argument that represents the source directory into which the file should be moved. 
=== "C++"
	```c++ hl_lines="4"
	FCakeFile SpellsDb { FCakePath{TEXTVIEW("abilities/magic/spells.db")} };
	FCakePath ArchiveDir{ FCakePath{TEXTVIEW("/y/archive/spells_backup")}  };

	if (!SpellsDb.MoveFile(ArchiveDir))
	{
		UE_LOG(LogTemp, Warning, TEXT("Failed moving spells database to archive dir."))
	}
	```
	--8<-- "ad-settings-copyitem.md"

=== "Blueprint"
	{{ bp_img_file('Move File') }}

Just like copy interface, we can also change the name of the moved file via `MoveFileAliased`:

=== "C++"
	```c++ hl_lines="4"
	FCakeFile SpellsDb { FCakePath{TEXTVIEW("abilities/magic/spells.db")} };
	FCakePath ArchiveDir{ FCakePath{TEXTVIEW("/y/archive/spells_backup")}  };

	if (!SpellsDb.MoveFileAliased(ArchiveDir, TEXTVIEW("spells_archive.db")))
	{
		UE_LOG(LogTemp, Warning, TEXT("Failed moving spells database to archive dir."))
	}
	```

	--8<-- "ad-settings-copyitem.md"

=== "Blueprint"
	{{ bp_img_file('Move File Aliased') }}

In the example above, assuming the move succeeds, the moved file's path will be `/y/archive/spells_backup/spells_archive.db`.

### Changing File Names
Cake File objects have various functions to aid us in changing their associated file's name on the filesystem.

!!! info 
	In all of the following functions, the second argument (optional in C++) is an [OverwriteItems](special-types/policies.md#overwriteitems) policy which controls whether or not we can overwrite an existing file if one with the desired name already exists in the same directory. 

We can change the entire file's name using `ChangeFileName`:
=== "C++"
	```c++ hl_lines="3"
	FCakeFile SpellsDb { FCakePath{TEXTVIEW("abilities/magic/spells.db")} };

	if (!SpellsDb.ChangeFileName( TEXTVIEW("spells_archive.db") ))
	{
		UE_LOG(LogTemp, Warning, TEXT("Failed changing the file name."))
	}
	```

=== "Blueprint"
	{{ bp_img_file('Change File Name') }}

We can change just the file extension using `ChangeFileExt`, passing a CakeFileExt object that holds the desired file extension:
=== "C++"
	```c++ hl_lines="3"
	FCakeFile SpellsDb { FCakePath{TEXTVIEW("abilities/magic/spells.db")} };

	if (!SpellsDb.ChangeFileExt( FCakeFileExt(TEXTVIEW("bin.db")) ))
	{
		UE_LOG(LogTemp, Warning, TEXT("Failed changing the full file extension."))
	}
	```
=== "Blueprint"
	{{ bp_img_file('Change File Ext') }}

In the example above, assuming the change succeeds, the final extension will be `.bin.db`.


Finally, we can change the trailing file extension component using `ChangeFileExtSingle`, passing a CakeFileExt object that holds the desired file extension:

=== "C++"
	```c++ hl_lines="3"
	FCakeFile MagicDetails { FCakePath{TEXTVIEW("abilities/magic/details.cdr.pdf")} };

	if (!MagicDetails.ChangeFileExtSingle( FCakeFileExt(TEXTVIEW("txt")) ))
	{
		UE_LOG(LogTemp, Warning, TEXT("Failed changing the trailing file extension component."))
	}
	```
=== "Blueprint"
	{{ bp_img_file('Change File Ext Single') }}

	In the example above, assuming the change succeeds, the final extension will be `.cdr.txt`.

!!! note
	For more details regarding file extensions and their classifications (multi / single), please see [this section](file-extensions.md#file-extension-classification).

### File OS Stat Information
The Query family of functions allows us to gain os information about a particular file, such as its size in bytes or its last modified timestamp.

!!! warning
	It is imperative that you ensure that a particular Query operation has succeeded without error before using any value returned by these functions. The values are only in a valid state when the associated Query function indicates success.

To get all OS stat info for a CakeFile object, we use `QueryStatData`
=== "C++"
	--8<-- "ad-order-file.md"

	`QueryStatData` returns a TCakeOrderFile whose payload is the Unreal type `FFileStatData`.

	```c++ hl_lines="3"
	FCakeFile SrcGoblin{ FCakePath{TEXTVIEW("enemies/ai/goblin.cpp")} };

	if (TCakeOrderFile<FFileStatData> StatData = SrcGoblin.QueryStatData())
	{
		FFileStatData& DataUnwrapped = *StatData;
		UE_LOG(LogTemp, Warning, TEXT("StatData file size: [%d] bytes."), DataUnwrapped.FileSize);
		UE_LOG(LogTemp, Warning, TEXT("StatData access time: [%s]"), *DataUnwrapped.AccessTime.ToString());
		UE_LOG(LogTemp, Warning, TEXT("StatData creation time: [%s]"), *DataUnwrapped.CreationTime.ToString());
	}
	```

=== "Blueprint"
	{{ bp_img_file('Query Stat Data')}}

	`QueryStatData` returns a boolean indicating whether or not the stat data was successfully retrieved, and a `CakeFileStatData` which holds the stat info. __It is imperative you check that the stat data is valid, otherwise you will be using incorrect information__. You can check via the `GotValidStatData` flag returned by the function or by the member field `IsValid` in the CakeFileStatData struct itself. 

	{{ bp_img_file('Cake File Stat Data') }}

	!!! note
		CakeFileStatData is just a Blueprint friendly version of Unreal's `FFileStatInfo`, which is not exposed to Blueprint.

We can also query individual stats if we don't need all the data that `QueryStatData` provides.

We can attempt to retrieve the size of a file via `QueryFileSizeInBytes`:
=== "C++"
	```c++ hl_lines="3"
	FCakeFile SrcGoblin{ FCakePath{TEXTVIEW("enemies/ai/goblin.cpp")} };

	if (TCakeOrderFile<int64> FileSize = SrcGoblin.QueryFileSizeInBytes())
	{
		UE_LOG(LogTemp, Warning, TEXT("QueryFileSizeInBytes file size: [%d] bytes."), *FileSize);
	}
	```

=== "Blueprint"
	{{ bp_img_file('Query File Size In Bytes') }}

We can attempt to retrieve the last modified timestamp via `QueryTimestampLastModified`, which gives us back an `FDateTime` indicating the time the file was last modified.
=== "C++"
	```c++ hl_lines="3"
	FCakeFile SrcGoblin{ FCakePath{TEXTVIEW("enemies/ai/goblin.cpp")} };

	if (TCakeOrderFile<FDateTime> ModStamp = SrcGoblin.QueryTimestampLastModified())
	{
		FString DateStr{ ModStamp.Payload.ToString() };
		UE_LOG(LogTemp, Warning, TEXT("QueryModifiedTimestamp: [%s]"), *DateStr);
	}
	```

=== "Blueprint"
	{{ bp_img_file('Query Timestamp Last Modified') }}
We can also try to change the last modified time to a custom value via `ChangeTimestampLastModified`.

=== "C++"
	```c++ hl_lines="5"
	FCakeFile SrcGoblin{ FCakePath{TEXTVIEW("enemies/ai/goblin.cpp")} };

	FDateTime NewMod{ FDateTime::Now() };
	NewMod -= FTimespan::FromDays(1.0);
	if (SrcGoblin.ChangeTimestampLastModified(NewMod))
	{
		UE_LOG(LogTemp, Warning, TEXT("New mod time: [%s]"), *NewMod.ToString())
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("Failed modifying the source file's modified timestamp."))
	}
	```
=== "Blueprint"
	{{ bp_img_file('Change Timestamp Last Modified') }}

We can attempt to retrieve the last accessed timestamp via `QueryTimestampLastAccessed`, which gives us back an `FDateTime` indicating the last time the file was accessed:

=== "C++"
	```c++ hl_lines="3"
	FCakeFile SrcGoblin{ FCakePath{TEXTVIEW("enemies/ai/goblin.cpp")} };

	if (TCakeOrderFile<FDateTime> AccessStamp = SrcGoblin.QueryTimestampLastAccessed())
	{
		FString DateStr{ AccessStamp.Payload.ToString() };
		UE_LOG(LogTemp, Warning, TEXT("Last Accessed: [%s]"), *DateStr);
	}
	```
=== "Blueprint"
	{{ bp_img_file('Query Timestamp Last Accessed') }}

### Changing File Permissions
We can change whether a file is marked as read-only via `ChangeFilePermissions`:
=== "C++"
	```c++ hl_lines="3"
	FCakeFile SrcGoblin{ FCakePath{TEXTVIEW("enemies/ai/goblin.cpp")} };

	if (!SrcGoblin.ChangeFilePermissions(ECakeFilePermissions::ReadOnly))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed setting goblin.cpp to read-only."))
	}
	```
=== "Blueprint"
	{{ bp_img_file('Change File Permissions') }}

This function takes an `ECakeFilePermissions` enum argument, which allows to specify between ReadOnly or ReadWrite:

=== "C++"
	```c++
	enum struct ECakeFilePermissions : uint8
	{
		/** File is marked as read-only. */
		ReadOnly		UMETA(DisplayName = "Read Only"),
		/** File is marked as read/write. */
		ReadWrite	    UMETA(DisplayName = "Read Write"),
		//...
	};
	```
=== "Blueprint"
	{{ bp_img_file('Cake File Permissions') }}


## Advanced Usage

### Advanced File Name Extraction
Cake File objects allow callers to clone its associated file name into three different forms. It is important to understand how CakeFS classifies file names before we examine the clone interfaces.

#### File Name Types
**CakeFS** classifies file names into three different categories. 

Using the file name `info.cdr.txt` as an example, we can view the file name according to three different categories:

1. **Full Name**: The file name with all of its extensions: `info.cdr.txt`
1. **Root Name**: The file name with its trailing extension removed: `info.cdr`
1. **Bare Name**: The file name without any extensions: `info`

!!! note
	When FileName is used by itself, **Full Name** is implied. Thus, `CloneFileName` will clone the full file name, whereas `CloneFileNameBare` will clone the bare file name.

#### Advanced File Name Interfaces
!!! hint
	CakeFile objects do not cache any data about themselves to keep them as lightweight and low-cost as possible. Thus, all functions that extract the file name return an FString. If you are going to reuse the file name in multiple locations, cache the result whenever possible for best performance.
When we want to get the full name of the file, we need to use `CloneFileName`:
=== "C++"
	```c++ hl_lines="3"
	FCakeFile SrcOrc{ FCakePath{TEXTVIEW("enemies/orc_warrior.gen.cpp")} };

	FString FullName{ SrcOrc.CloneFileName() };
	UE_LOG(LogTemp, Warning, TEXT("   CloneFileName: [%s]"), *FullName); // => "orc_warrior.gen.cpp"
	```
=== "Blueprint"
	{{ bp_img_file('Clone File Name Adv') }}

In the example above, the returned file name will be `orc_warrior.gen.cpp`.

To get the root file name, we need to use `CloneFileNameRoot`:

=== "C++"
	```c++ hl_lines="3"
	FCakeFile SrcOrc{ FCakePath{TEXTVIEW("enemies/orc_warrior.gen.cpp")} };

	FString RootName{ SrcOrc.CloneFileNameRoot() };
	UE_LOG(LogTemp, Warning, TEXT("CloneFileNameRoot: [%s]"), *RootName); // => "orc_warrior.gen"
	```
=== "Blueprint"
	{{ bp_img_file('Clone File Name Root') }}

In the example above, the returned file name will be `orc_warrior.gen`.

Finally, when we want the bare file name, we can use `CloneFileNameBare`:
=== "C++"
	```c++ hl_lines="3"
	FCakeFile SrcOrc{ FCakePath{TEXTVIEW("enemies/orc_warrior.gen.cpp")} };

	FString BareName{ SrcOrc.CloneFileNameBare() };
	UE_LOG(LogTemp, Warning, TEXT("CloneFileNameBare: [%s] "), *BareName); // => "orc_warrior"
	```
=== "Blueprint"
	{{ bp_img_file('Clone File Name Bare') }}

In the example above, the returned file name will be `orc_warrior`.

### Low-Level FileHandles
!!! note
	Only native Cake File objects can get access to low-level file handles.

There may be situations where you direct access to a low-level file handle. To get a unique pointer to an `IFileHandle`, use `OpenFileHandleUnique`. This function takes one parameter, an [FCakeSettingsFileHandle](special-types/settings.md#fcakesettingsfilehandle) settings struct that determines the open / write mode the file handle should use.
```c++ hl_lines="4"
	FCakeFile SrcOrc{ FCakePath{TEXTVIEW("enemies/orc_warrior.gen.cpp")} };

	TUniquePtr<IFileHandle> FileHandle{ 
		SrcOrc.OpenFileHandleUnique({ 
			.OpenMode = ECakeFileOpenMode::ReadAndWrite, 
			.WriteMode = ECakeFileWriteMode::OverwriteData })
	};

	if (FileHandle.IsValid())
	{
		// ...
	}
```

!!! warning 
	`OpenFileHandleUnique` will return an invalid pointer when the opening fails, so always check to ensure the pointer is valid before using it!


