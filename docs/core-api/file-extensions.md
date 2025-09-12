## Introduction
CakeFS offers FileExtension objects provide a type-safe way to extract, examine, classify, and manipulate file extensions. 

=== "C++"
    {{ cpp_impl_source('file extension', 'FCakeFileExt', 'CakeFileExt') }}

=== "Blueprint"
    {{ bp_impl_source('file extension', 'UCakeFileExt', 'CakeFileExt_BP') }}

## File Extension Classification
Before we look at the File Extension object interface, it is important to understand how CakeFS classifies file extensions. CakeFS defines two distinct types of file extension: **single** file extensions and **multi** file extensions.
> **Single File Extension**: A file extension that contains only one file extension component: e.g., `.txt` or `.bin`

> **Multi File Extension**: A file extension that contains more than one file extension component: e.g., `.cdr.txt` or `.bin.dat.zip`

CakeFS represents file extension types via the enum ECakeFileExtType. File extensions that are empty will have the value `None`, file extensions with one component will be assigned the value `Single`, and file extensions with more than one component will have the value `Multi`.


=== "C++"

    ```c++ 
    auto EmptyExt  = ECakeFileExtType::None;
    auto SingleExt = ECakeFileExtType::Single;
    auto MultiExt  = ECakeFileExtType::Multi;
    ```
=== "Blueprint"
    {{ bp_img_file_ext('File Ext Types') }}

## Basic Usage
### Building File Extension Objects
=== "C++"
    To build an FCakeFileExt object, we can use the constructor which takes an FStringView that represents the file extension we want to store.

    ```c++
	FCakeFileExt TextExt  { TEXTVIEW(".txt") };
	FCakeFileExt BinaryExt{ TEXTVIEW("bin")  };
    ```

    Because FCakeFileExt enforces a standard representation of file extensions, it doesn't matter if we supply the leading extension dot '.' when submitting an extension string.

    To create an FCakeFileExt by extracting the file extension from a file name, we can use the static function `BuildFileExtFromFilePath`:

    ```c++ hl_lines="3"
	FCakePath FileReadme{ TEXTVIEW("data/example_file.txt") };

	FCakeFileExt ExtFromFile{ FCakeFileExt::BuildFileExtFromFilePath(FileReadme) };
    ```
    --8<-- "warn-file-ext-extractions.md"

    We can create copies of a pre-existing FCakeFileExt through the copy constructor or the member function `Clone`:

    ```c++ hl_lines="3 4"
	FCakeFileExt TextExt{ TEXTVIEW(".txt") };

	FCakeFileExt TextCopy { TextExt         };
	FCakeFileExt TextClone{ TextExt.Clone() };
    ```

    If we want a clone of the FCakeFileExt's string only, we can use the member function `CloneFileExtString`:

    ```c++ hl_lines="3"
	FCakeFileExt TextExt{ TEXTVIEW(".txt") };

	FString TextString{ TextExt.CloneFileExtString() };
    ```

=== "Blueprint"
    To build a new CakeFileExt object, we use `BuildCakeFileExt`, submitting a string which represents the file extension the object should represent:

    {{ bp_img_file_ext('Build Cake File Ext') }}

    !!! note
        It doesn't matter if we include the leading `.` character for our file extension input arguments.

    If we want to build an empty File Extension object, we can use `BuildCakeFileExtEmpty`:

    {{ bp_img_file_ext('Build Cake File Ext Empty') }}

    When we have a file path, we can extract its extension into a File Extension object via `BuildCakeFileExt FromFilePath`:

    {{ bp_img_file_ext('Build Cake File Ext From File Path') }}

    --8<-- "warn-file-ext-extractions.md"


    To create a duplicate File Extension object, use `Clone`:

    {{ bp_img_file_ext('Clone') }}

    If we just need the file extension duplicated as a string, we can use `CloneFileExtString`:

    {{ bp_img_file_ext('Clone File Ext String') }}


### Reading the File Extension String
=== "C++"
    To read the file extension string, we can use either `operator*` or `GetFileExtString`:

    ```c++ hl_lines="6-7"
	auto LogExt = [](const FString& ExtStr) 
		{ UE_LOG(LogTemp, Warning, TEXT("Extension String: [%s]"), *ExtStr); };

	FCakeFileExt TextExt  { TEXTVIEW(".txt") };

	LogExt(*TextExt);
	LogExt( TextExt.GetFileExtString() );
    ```
=== "Blueprint"
    To read the file extension as a string, we use `GetFileExtString`:

    {{ bp_img_file_ext('Get File Ext String') }}

### Modifying the File Extension
=== "C++"
    We have many ways to change the file extension of a pre-existing FCakeFileExt. To change the extension string to another string that represents a file extension, we can use the member function `SetFileExt`.

    ```c++ hl_lines="3"
	FCakeFileExt SourceExt{ TEXTVIEW(".txt") };

	SourceExt.SetFileExt( TEXTVIEW("bin.dat") ); // => ".bin.dat"
    ```
    --8<-- "warn-file-ext-set-versus-extract.md"

    To copy the file extension from another FCakeFileExt object, we can use the member function `SetFileExtViaOther`:

    ```c++ hl_lines="4"
    FCakeFileExt SourceExt  { TEXTVIEW(".txt")     };
	FCakeFileExt GameSaveExt{ TEXTVIEW(".sav.dat") };

	SourceExt.SetFileExtViaOther(GameSaveExt);
    ```

    To steal the file extension from another FCakeFileExt object, we can use the member function `StealFileExt`:

    ```c++ hl_lines="4"
	FCakeFileExt SourceExt  { TEXTVIEW(".txt")     };
	FCakeFileExt GameSaveExt{ TEXTVIEW(".sav.dat") };

	SourceExt.StealFileExt(MoveTemp(GameSaveExt));
    ```

    To change the file extension to be the extraction result from a file path, we can use the member function `SetFileExtFromFilePath`:

    ```c++ hl_lines="4"
	FCakeFileExt SourceExt{ TEXTVIEW(".txt")                    };
	FCakePath    ItemsDb  { TEXTVIEW("/y/data/assets/items.db") };

	SourceExt.SetFileExtFromFilePath(ItemsDb); // => ".db"
    ```


    --8<-- "ad-copymove-ctor.md"

    We can check if an FCakeFileExt holds any file extension via the member function `IsEmpty`:

    ```c++ hl_lines="4"
	FCakeFileExt SourceExt{ TEXTVIEW(".txt")     };

	SourceExt.Reset();
	const bool IsEmpty{ SourceExt.IsEmpty() }; // => true
    ```

    To clear any existing file extension from an FCakeFileExt object, we can use the member function `Reset`:

    ```c++ hl_lines="3"
	FCakeFileExt SourceExt{ TEXTVIEW(".txt")     };

	SourceExt.Reset();
    ```

    `Reset` takes an optional parameter that can reserve a new size for the internal `FString` that will hold the file extension string:

    ```c++ hl_lines="4"
	FCakeFileExt SourceExt{ TEXTVIEW(".txt")     };
	FCakeFileExt ExtMulti { TEXTVIEW(".cdr.txt") };

	SourceExt.Reset( ExtMulti.GetExtString().Len() );

	SourceExt.SetFileExtViaOther(ExtMulti);
	const bool IsEmpty{ SourceExt.IsEmpty() }; // => false
    ```
    --8<-- "note-reset-forwarding.md"

=== "Blueprint"
    To change the file extension of an existing FileExtension object, we use `SetFileExt`:

    {{ bp_img_file_ext('Set File Ext') }}

    --8<-- "warn-file-ext-set-versus-extract.md"

    To change the file extension to another FileExtension object's extension, we use `SetFileExtViaOther`:

    {{ bp_img_file_ext('Set File Ext Via Other') }}

    To change the file extension to a file path's file extension, we use `SetFileExtFromFilePath`:

    {{ bp_img_file_ext('Set File Ext From File Path') }}

    --8<-- "warn-file-ext-extractions.md"

    To see if a FileExtension object's file extension is empty, we use `IsEmpty`:

    {{ bp_img_file_ext('is-empty') }}

    To clear an existing FileExtension object's file extension back to empty, we use `Reset`:

    {{ bp_img_file_ext('reset') }}

    --8<-- "note-bp-newreservedsize.md"

### Combining File Extensions
=== "C++"
    We can build combined extensions with the member function `operator+`:

    ```c++ hl_lines="4"
	FCakeFileExt ExtTxt{ TEXTVIEW(".txt") };
	FCakeFileExt ExtCdr{ TEXTVIEW(".cdr") };

	FCakeFileExt ExtCdrTxt{ ExtCdr + ExtTxt }; // => ".cdr.txt"
    ```
    We can also alternatively use the member function `Combine` if we prefer:

    ```c++ hl_lines="4"
	FCakeFileExt ExtTxt{ TEXTVIEW(".txt") };
	FCakeFileExt ExtCdr{ TEXTVIEW(".cdr") };

	FCakeFileExt ExtCdrTxt{ ExtCdr.Combine(ExtTxt) }; // => ".cdr.txt"
    ```

    To append a file extension onto a pre-existing FCakeFileExt object, we can use either member function `operator+=` or `CombineInline`:

    ```cpp
    FCakeFileExt ExtSrc   { TEXTVIEW(".txt")     };
    FCakeFileExt ExtCdr   { TEXTVIEW(".cdr")     };
    FCakeFileExt ExtBinDat{ TEXTVIEW(".bin.dat") };

    ExtSrc += ExtCdr; // => ".txt.cdr"
    ExtSrc.CombineInline(ExtBinDat); // => ".txt.cdr.bin.dat"
    ```

=== "Blueprint"
    To create a new FileExtension object that combines the extensions of two FileExtension objects, we use `Combine`:

    {{ bp_img_file_ext('Combine') }}

    To append one FileExtension object's extension directly to another FileExtension object, we use `CombineInline`:

    {{ bp_img_file_ext('Combine Inline') }}


### Comparing File Extensions
=== "C++"
    We can use equality comparison against FCakeFileExt objects via member functions `operator==` and `operator!=`. 

    ```c++ hl_lines="4-5"
	FCakeFileExt ExtA{ TEXTVIEW(".txt") };
	FCakeFileExt ExtB{ TEXTVIEW(".cdr") };

	const bool bIsEqual   { ExtA == ExtB }; // => false
	const bool bIsNotEqual{ ExtA != ExtB }; // => true
    ```

=== "Blueprint"
    To check if one FileExtension object is equal to another, we use `IsEqualTo`:

    {{ bp_img_file_ext('Is Equal To') }}

    To check if one FileExtension object is not equal to another, we use `IsNotEqualTo`:

    {{ bp_img_file_ext('Is Not Equal To') }}

### Classifying a File Extension
We can get the [file extension classification](#file-extension-classification) of a CakeFileExt via `ClassifyFileExt`, which returns the corresponding file extension type as an ECakeFileExtType enum value:
=== "C++"

    ```c++ hl_lines="5-7"
	FCakeFileExt ExtNone  {};
	FCakeFileExt ExtSingle{ TEXTVIEW(".txt")     };
	FCakeFileExt ExtMulti { TEXTVIEW(".cdr.txt") };

	ECakeFileExtType ExtType{ ExtNone.ClassifyFileExt() }; // => None
	ExtType = ExtSingle.ClassifyFileExt(); // => Single
	ExtType = ExtMulti.ClassifyFileExt(); // => Multi
    ```
=== "Blueprint"
    {{ bp_img_file_ext('Classify File Ext') }}

## Advanced Usage
### Viewing a File Extension in Single form
There are situations where it can be valuable to only assess a file extension's trailing component, regardless as to whether the actual file extension's type is multi or single. There are various utility methods to support this operation.

When we want to view the trailing extension of an existing FileExt object, we use `CloneSingle`:
=== "C++"

    ```c++ hl_lines="4-5"
    FCakeFileExt ExtSingle{ TEXTVIEW(".txt")     };
	FCakeFileExt ExtMulti { TEXTVIEW(".cdr.txt") };

	FCakeFileExt ClonedSingle{ ExtSingle.CloneSingle() }; // => ".txt"
	ClonedSingle = ExtMulti.CloneSingle(); // => ".txt"
    ```
=== "Blueprint"
    {{ bp_img_file_ext('Clone Single') }}

    In the example above, the cloned CakeFileExt will have the extension `.txt`.

!!! note
    `CloneAsSingle` will always return the trailing component on a file extension (assuming there is one), so it is safe to use on both single and multi extensions. This means that `CloneAsSingle` is a valuable tool when you are processing file extensions and only care about examining the trailing extension component, regardless of your source extension's actual number of extension components.

### Extracting a File Extension in Single Form
There are functions that allow us to extract only the trailing file extension component from a given file path.

=== "C++"
    We can extract just the trailing extension component from a file name via the static function `BuildFileExtFromFilePathSingle`:
    ```c++ hl_lines="4"
	FCakePath SecretItemsDb{ TEXTVIEW("/x/game/data/secret/items.bin.db") };

	FCakeFileExt SingleFromFilePath{ 
		FCakeFileExt::BuildFileExtFromFilePathSingle(SecretItemsDb) 
	}; // => ".db"
    ```
=== "Blueprint"
    To build a FileExt object that contains just the trailing component (assuming there is one) of a file extension, we use `BuildCakeFileExtFromFilePathSingle`:

    {{ bp_img_file_ext('Build Cake File Ext From File Path Single') }}

In the example above, the CakeFileExt will have the extension `.db`.