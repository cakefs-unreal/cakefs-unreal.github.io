## Overview
CakeFS offers FileExtension objects provide a type-safe way to extract, examine, classify, and manipulate file extensions. 

### Source Code Information
{{ cpp_impl_source('FCakeFileExt', 'CakeFileExt') }}

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
We build an FCakeFileExt object by supplying a string that represents the file extension we want to store.

!!! note
    It doesn't matter if we include the leading `.` character for our file extension input arguments.

=== "C++"

    ```c++
	FCakeFileExt TextExt  { TEXTVIEW(".txt") };
	FCakeFileExt BinaryExt{ TEXTVIEW("bin")  };
    ```
=== "Blueprint"
    {{ bp_img_file_ext('Make Cake File Ext') }}

To create an FCakeFileExt by extracting the file extension from a file name, we can use the static function `BuildFileExtFromFilePath`:

=== "C++"

    ```c++ hl_lines="3"
	FCakePath    SourceFile { TEXTVIEW("data/example_file.txt")                  };

	FCakeFileExt ExtFromFile{ FCakeFileExt::BuildFileExtFromFilePath(SourceFile) };
    ```

=== "Blueprint"
    {{ bp_img_file_ext('Build Cake File Ext From File Path') }}

--8<-- "warn-file-ext-extractions.md"

We can use `Clone` to make an independent copy of a CakeFileExt object:

=== "C++"

    ```c++ hl_lines="3 4"
	FCakeFileExt TextExt  { TEXTVIEW(".txt") };
	FCakeFileExt TextClone{ TextExt.Clone()  };
    ```

=== "Blueprint"
    {{ bp_img_file_ext('Clone') }}

### Reading the File Extension String
To read the file extension string we use `GetFileExtString`:
=== "C++"

    ```c++ hl_lines="6-7"
	auto LogExt = [](const FString& ExtStr) 
		{ UE_LOG(LogTemp, Warning, TEXT("Extension String: [%s]"), *ExtStr); };

	FCakeFileExt TextExt  { TEXTVIEW(".txt") };

	LogExt( TextExt.GetFileExtString() );
	LogExt(*TextExt);
    ```

    !!! note
        `operator*` can be used to achieve the same effect.

=== "Blueprint"
    {{ bp_img_file_ext('Get File Ext String') }}

To get an independent copy of the file extension string, we use `CloneFileExtString`:
=== "C++"

    ```c++ hl_lines="6-7"
	FCakeFileExt TextExt   { TEXTVIEW(".txt")             };
    FString      TextExtStr{ TextExt.CloneFileExtString() };
    ```
=== "Blueprint"
    {{ bp_img_file_ext('Clone File Ext String') }}

### Modifying the File Extension
To change the extension string to another string that represents a file extension, we can use the member function `SetFileExt`, submitting either a string or an FCakeFileExt object.

=== "C++"

    ```c++ hl_lines="3"
	FCakeFileExt SourceExt{ TEXTVIEW(".txt") };

	SourceExt.SetFileExt( TEXTVIEW("bin.dat") ); // => ".bin.dat"
    ```

=== "Blueprint"
    {{ bp_img_file_ext('Set File Ext') }}


--8<-- "warn-file-ext-set-versus-extract.md"

To set the file extension using a file path, we can use the member function `SetFileExtFromFilePath`:

=== "C++"

    ```c++ hl_lines="4"
	FCakeFileExt SourceExt{ TEXTVIEW(".txt")                    };
	FCakePath    ItemsDb  { TEXTVIEW("/y/data/assets/items.db") };

	SourceExt.SetFileExtFromFilePath(ItemsDb); // => ".db"
    ```

=== "Blueprint"
    {{ bp_img_file_ext('Set File Ext From File Path') }}

We can check if a CakeFileExt holds any file extension via the member function `IsEmpty`:

=== "C++"

    ```c++ hl_lines="3"
	FCakeFileExt SourceExt{ TEXTVIEW(".txt")     };

	const bool IsEmpty{ SourceExt.IsEmpty() }; // => false
    ```
=== "Blueprint"
    {{ bp_img_file_ext('Is Empty') }}

To clear any existing file extension, we can use the member function `Reset`:

=== "C++"

    ```c++ hl_lines="3"
	FCakeFileExt SourceExt{ TEXTVIEW(".txt")     };

	SourceExt.Reset();
	const bool IsEmpty{ SourceExt.IsEmpty() }; // => true
    ```

=== "Blueprint"
    {{ bp_img_file_ext('Reset') }}

!!! note
    `Reset` takes an optional parameter that can reserve a new size for the internal `FString` that will hold the file extension string. Leave this at zero if you don't require a specific reserved size.

### Combining File Extensions
To create a CakeFileExt object that combines two other file extensions together, we use `Combine`: 
=== "C++"

    ```c++ hl_lines="4"
	FCakeFileExt ExtTxt{ TEXTVIEW(".txt") };
	FCakeFileExt ExtCdr{ TEXTVIEW(".cdr") };

	FCakeFileExt ExtCdrTxt{ ExtCdr.Combine(ExtTxt) }; // => ".cdr.txt"
    ```
    We can also use `operator+` to achieve the same effect:

    ```c++ hl_lines="4"
	FCakeFileExt ExtTxt{ TEXTVIEW(".txt") };
	FCakeFileExt ExtCdr{ TEXTVIEW(".cdr") };

	FCakeFileExt ExtCdrTxt{ ExtCdr + ExtTxt }; // => ".cdr.txt"
    ```

=== "Blueprint"
    {{ bp_img_file_ext('Combine') }}

We can append another file extension onto a preexisting CakeFileExt object with CombineInline:

=== "C++"

    ```cpp
    FCakeFileExt ExtSrc   { TEXTVIEW(".txt")     };
    FCakeFileExt ExtCdr   { TEXTVIEW(".cdr")     };
    FCakeFileExt ExtBinDat{ TEXTVIEW(".bin.dat") };

    ExtSrc += ExtCdr; // => ".txt.cdr"
    ExtSrc.CombineInline(ExtBinDat); // => ".txt.cdr.bin.dat"
    ```

=== "Blueprint"
    {{ bp_img_file_ext('Combine Inline') }}

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

### File Extension Equality
We check file extension equality using `operator==` and `operator!=`:

=== "C++"

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


## Advanced Usage
### Viewing a File Extension in Single form
Sometimes we might want to only take into account the last component of a file extension. To do this, we can use `CloneSingle`, which will return a CakeFileExt object that contains the final component of its source file extension.

=== "C++"

    ```c++ hl_lines="4-5"
    FCakeFileExt ExtSingle{ TEXTVIEW(".txt")     };
	FCakeFileExt ExtMulti { TEXTVIEW(".cdr.txt") };

	FCakeFileExt ClonedSingle{ ExtSingle.CloneSingle() }; // => ".txt"
	ClonedSingle = ExtMulti.CloneSingle(); // => ".txt"
    ```

=== "Blueprint"
    {{ bp_img_file_ext('Clone Single') }}

In the example above, each cloned CakeFileExt will have the extension `.txt`.

!!! note
    As the examples show, `CloneSingle` will always return the trailing component on a file extension (assuming there is one), so it is safe to use on both single and multi extensions. This means that `CloneSingle` is a valuable tool when you are processing file extensions and only care about examining the trailing extension component regardless as to how many actual extensions the file might have.

### Extracting a File Extension in Single Form
There are functions that allow us to extract only the trailing file extension component from a given file path.

We can extract just the trailing extension component from a file name using `BuildFileExtFromFilePathSingle`:
=== "C++"

    ```c++ hl_lines="4"
	FCakePath SecretItemsDb{ TEXTVIEW("/x/game/data/secret/items.bin.db") };

	FCakeFileExt SingleFromFilePath{ 
		FCakeFileExt::BuildFileExtFromFilePathSingle(SecretItemsDb) 
	}; // => ".db"
    ```
=== "Blueprint"
    {{ bp_img_file_ext('Build Cake File Ext From File Path Single') }}

In the example above, the CakeFileExt will have the extension `.db`.