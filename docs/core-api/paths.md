## Overview
CakePath objects provide an ergonomic and standardized way to work with filesystem paths in Unreal Engine. 

### Source Code Information
=== "C++"
    {{ cpp_impl_source('path', 'FCakePath', 'CakePath') }}
    
=== "Blueprint"
    {{ bp_impl_source('path', 'UCakePath', 'CakePath_BP') }}

## Basic Usage
In this section we will cover the fundamental CakePath operations. Once you are comfortable using CakePaths, consider looking at the advanced usage section for examples of more complex operations.

### Building CakePath Objects
=== "C++"
    The most straightforward way to build a new FCakePath is via the constructor, which accepts an FStringView. 

    ```c++
    FCakePath FirstPath{ TEXTVIEW("x/game/data") };
    ```
    Remember, CakePath objects will ensure path representation is standardized, so we can also submit Windows-style paths to the constructor.

    ```c++
    FCakePath FirstPath{ TEXTVIEW("X:\\game\\data") };
    ```

    It also doesn't matter whether or not we include trailing path separators for directory paths. The following FCakePath objects hold the exact same path:

    ```c++
    FCakePath PathA{ TEXTVIEW("x/game/data") };
    FCakePath PathB{ TEXTVIEW("x/game/data/") };
    ```

    To build a combined path out of multiple string-like objects, we can use the static method `BuildPathCombined`.

    ```c++ hl_lines="3"
	FString PathComponentOne{ TEXT("x/game") };

	FCakePath CombinedPath{ FCakePath::BuildPathCombined(PathComponentOne, TEXTVIEW("data")) };
    ```
=== "Blueprint"
    When we want to make a new CakePath object, we can use `BuildCakePath`, supplying a string that represents the path that this CakePath object should hold.

    {{ bp_img_path('Build Cake Path') }}

    Sometimes we might want to make an empty CakePath object and set its path information later, and for that we can use `BuildCakePathEmpty`, which will give us a CakePath object whose path is empty:

    {{ bp_img_path('Build Cake Path Empty') }}

    We can build a combined path with `BuildCakePathCombined`, which will create a combined path out of the two strings we supply as inputs: 

    {{ bp_img_path('Build Cake Path Combined') }}

    In the example above, the path of the object returned would be `X:/game/data/assets`.

### Copying Paths
=== "C++"
    To get a copy of an existing FCakePath, we can use either the copy constructor directly or call the function `Clone` on the source path.

    ```c++ hl_lines="3-4"
    FCakePath SourcePath{ TEXTVIEW("x/game/data") };

    FCakePath CopyCtor  { SourcePath         };
    FCakePath ClonedPath{ SourcePath.Clone() };
    ```

    To copy just the path string, use `ClonePathString`:

    ```c++ hl_lines="3"
    FCakePath SourcePath{ TEXTVIEW("x/game/data") };

    FString ClonedPathString{ SourcePath.ClonePathString() };
    ```

=== "Blueprint"
    To duplicate a CakePath object, we use `Clone`:

    {{ bp_img_path('Clone') }}

    To duplicate just the path as a string, we use `ClonePathString`:

    {{ bp_img_path('Clone Path String') }}

### Reading the Path String
=== "C++"
    To read an FCakePath's path string, we can use `operator*` or `GetPathString`:

    ```c++ hl_lines="4 5"
    auto PrintPath = [](const FString& Path) { UE_LOG(LogTemp, Warning, TEXT("Path: [%s]"), *Path) };
    FCakePath SourcePath{ TEXT("x/game/data") };

    PrintPath(*SourcePath); // => "x/game/data"
    PrintPath(SourcePath.GetPathString()); // => "x/game/data"
    ```

=== "Blueprint"
    To read the path as a string, we can use `GetPathString`:

    {{ bp_img_path('Get Path String') }}

### Modifying Paths
=== "C++"
    We can change the path of an existing FCakePath via `SetPath`, which takes a string-like object just like the constructor:

    ```c++ hl_lines="3"
    FCakePath SourcePath{ TEXTVIEW("x/game/data") };

    SourcePath.SetPath(TEXTVIEW("y:/network/profiling/"));
    ```
    We can also set the path of an existing FCakePath to the path another FCakePath holds via `SetPathViaOther`:

    ```c++ hl_lines="4"
    FCakePath SourcePath{ TEXTVIEW("x/game/data") };
    FCakePath NewPath{ TEXTVIEW("Z:/misc/data") };

    SourcePath.SetPathViaOther(NewPath);
    ```

    If we want to use move semantics instead of copy semantics, we can use `StealPath`:

    ```c++ hl_lines="3"
    FCakePath SourcePath{ TEXTVIEW("x/game/data") };

    SourcePath.StealPath( FCakePath{ TEXTVIEW("Y:/netdb/player") } );
    ```
    --8<-- "ad-copymove-ctor.md"


    To check if an FCakePath's path is empty, we can use the `IsEmpty` member function:

    ```c++ hl_lines="3"
    FCakePath SourcePath{ TEXTVIEW("x/game/data") };

    const bool bPathIsEmpty{ SourcePath.IsEmpty() }; // => false
    ```
    To reset an FCakePath's path back to empty, we can use the `Reset` member function:

    ```c++ hl_lines="2"
    FCakePath SourcePath{ TEXTVIEW("x/game/data") };
    SourcePath.Reset();
    const bool bPathIsEmpty{ SourcePath.IsEmpty() }; // => true
    ```
    `Reset` takes an optional size parameter that will reserve a buffer size for the internal `FString` that holds the path string:

    ```c++ hl_lines="4"
    FCakePath SourcePath{ TEXTVIEW("x/game/data") };
    FCakePath NewPath{ TEXTVIEW("Z:/misc/data") };

    SourcePath.Reset(NewPath.GetPathString.Len());
    ```
    --8<-- "note-reset-forwarding.md"

=== "Blueprint"
    To change the path that a preexisting CakePath object holds, we use `SetPath`, submitting a string that represents the new path that the CakePath object should use:

    {{ bp_img_path('Set Path') }}

    !!! note
        In the example above, the path will be set to `y:/network/profiling/`.

    If we want to set the path using another CakePath object's path, we can use `SetPathViaOther`:

    {{ bp_img_path('Set Path Via Other') }}

    !!! note
        In the example above, the path will be `Z:/misc/data` after the call to Set Path resolves.

    To check if a path is empty, we can use `IsEmpty`:

    {{ bp_img_path('Is Empty') }}

    To clear any path a CakePath object holds, we use `Reset`:

    {{ bp_img_path('Reset') }}

    --8<-- "note-bp-newreservedsize.md"


### Combining Paths
=== "C++"
    To make a new FCakePath that combines other FCakePath objects, use `operator/` or `Combine`.

    ```c++ hl_lines="4 5"
	FCakePath PathGame    { TEXTVIEW("x/game/")       };
	FCakePath PathHeroFile{ TEXTVIEW("hero/hero.fbx") };

	FCakePath PathToHeroFileOperator{ PathGame / PathHeroFile        };
	FCakePath PathToHeroFileCombined{ PathGame.Combine(PathHeroFile) };
    ```
    Either function will produce the same result, but `operator/` can be especially ergonomic if you are combining more than two paths at once: 

    ```c++ hl_lines="5"
    FCakePath PathDrive   { TEXT("x")    };
    FCakePath PathGameOnly{ TEXT("game") };
    FCakePath PathDataOnly{ TEXT("data") };

    FCakePath PathDataCombined = PathDrive / PathGameOnly / PathDataOnly;
    ```
    Note that the combination interfaces only accept FCakePath objects as inputs in order to avoid implicit type conversions and surprising results. In other words, you can't mix string-like objects and FCakePath objects in combination chains. However, there are two ways to work around this. The simplest way is to explicitly convert any string-like objects into FCakePath objects within the combination expression:

    ```c++ hl_lines="4"
    FCakePath PathDrive     { TEXT("x")    };
    FString   PathGameString{ TEXT("game") };

    FCakePath CombinedMix{ PathDrive / FCakePath(PathGameString) };
    ```
    When combining multiple strings, you can use FString's `operator/`, which also supports path concatenation, and then feed the combined FString into the FCakePath constructor, which will guarantee the final result is well-formed:

    ```c++ hl_lines="4"
    FString PathDriveString { TEXT("x")    };
    FString PathGameString  { TEXT("game") };

    FCakePath CombinedFromStrings{ PathDriveString / PathGameString };
    ```

    To append another path onto a pre-existing FCakePath, we can use `operator/=` or `CombineInline`.

    ```c++ hl_lines="5 8"
    FCakePath PathMisc   { TEXTVIEW("y/misc")         };
    FCakePath PathItemsDb{ TEXTVIEW("items/items.db") };

    FCakePath PathCombineOperator{ PathMisc };
    PathCombineOperator /= PathItemsDb; // => "y/misc/items/items.db"

    FCakePath PathCombineInline{ PathMisc };
    PathCombineInline.CombineInline(PathItemsDb); // => "y/misc/items/items.db"
    ```

=== "Blueprint"
    To build a CakePath object whose path is the combination of two preexisting CakePath objects, we use `Combine`. 

    {{ bp_img_path('Combine') }}

    In the example above, the returned CakePath object's path will be `x/game/data/assets/models`.

    To append one CakePath object's path directly onto another CakePath object, we can use `CombineInline`. 

    {{ bp_img_path('Combine Inline') }}

    In the example above, the target CakePath object's path will be `x/game/data/assets/models`.

### Path Equality
Path equality in CakeFS is simple: two CakePath objects are equal if they refer to the same location on the filesystem.
=== "C++"
    FCakePath uses `operator==` and `operator!=` for equality comparisons.

    ```c++ hl_lines="6 7 9 10"
    FCakePath PathData{ TEXT("x/game/data") };
    FCakePath PathDataCopy{ TEXT("x/game/data") };
    FCakePath PathMisc{ TEXT("y/game/misc") };

    bool bPathsAreEqual{ false };
    bPathsAreEqual = PathData == PathMisc;      // => false
    bPathsAreEqual = PathData == PathDataCopy; // => true

    bPathsAreEqual = PathData != PathMisc;      // => true
    bPathsAreEqual = PathData != PathDataCopy; // => false
    ```
=== "Blueprint"
    To check if two CakePath objects are equal, we use `IsEqualTo`:

    {{ bp_img_path('Is Equal To') }}

    To check if two CakePath objects are not equal, we use `IsNotEqualTo`:

    {{ bp_img_path('Is Not Equal To') }}

## Advanced Usage

### Path Leaf Manipulation
The leaf of the path is its rightmost component. Given the path `x/game/data`, the leaf is `data`.

#### Leaf Extraction
To extract the leaf of a CakePath object as another CakePath object, we use `CloneLeaf`:
=== "C++"

    ```cpp hl_lines="3"
    FCakePath SourcePath{ TEXT("x/game/data") };

    FCakePath PathLeaf{ SourcePath.CloneLeaf() }; // => "data"
    ```

=== "Blueprint"
    {{ bp_img_path('Clone Leaf') }}

To get the leaf of a CakePath object as a string, we use `CloneLeafString`:
=== "C++"
    ```cpp hl_lines="3"
    FCakePath SourcePath{ TEXT("x/game/data") };

    FString LeafString{ SourcePath.CloneLeafString() }; // => "data"
    ```

=== "Blueprint"
    {{ bp_img_path('Clone Leaf String') }}

!!! note
    The leaf can always be empty, so don't forget to check in the situations where that matters.

#### Modifying the Leaf
We can modify the leaf of a CakePath via `SetLeaf`:
=== "C++"

    ```c++ hl_lines="3"
    FCakePath SourcePath{ TEXTVIEW("x/game/data") };

    SourcePath.SetLeaf(FCakePath{ TEXTVIEW("items") }); // path is now "x/game/items"
    ```

=== "Blueprint"
    {{ bp_img_path('Set Leaf') }}

We can get a copy of the CakePath with a new leaf via `CloneWithNewLeaf`, submitting a CakePath argument that is the leaf the cloned CakePath should use:
=== "C++"

    ```c++ hl_lines="4"
    FCakePath SourcePath{ TEXTVIEW("x/game/data") };
    FCakePath NewLeaf   { TEXTVIEW("items")     };

    FCakePath WithNewLeaf{ SourcePath.CloneWithNewLeaf(NewLeaf) };// path is "x/game/items"
    ```
=== "Blueprint"
    {{ bp_img_path('Clone With New Leaf') }}

!!! note 
    Even though the examples show changing the leaf with single-component paths, leaf manipulation methods can also change the leaf with a multi-component path as well. 

### Parent Path Manipulation
The parent path of a given path is all path components to the left of the path leaf; the parent path of `x/game/data` is `x/game/`.

#### Parent Path Extraction
To clone a CakePath's parent path as a new CakePath object, we use `CloneParentPath`:
=== "C++"

    ```cpp hl_lines="3"
    FCakePath SourcePath{ TEXT("x/game/data") };

    FCakePath ParentPath{ SourcePath.CloneParentPath() };
    ```

=== "Blueprint"
    {{ bp_img_path('Clone Parent Path') }}

When we want the parent path as a string, we can use `CloneParentPathString`:

=== "C++"

    ```cpp hl_lines="3"
    FCakePath SourcePath{ TEXT("x/game/data") };

    FString ParentPathString{ SourcePath.CloneParentPathString() };
    ```

=== "Blueprint"
    {{ bp_img_path('Clone Parent Path String') }}

!!! note
    The parent path can always be empty, so don't forget to check in the situations where that matters.

#### Modifying the Parent Path
We can modify the parent path of an existing CakePath object via `SetParentPath`:

=== "C++"

    ```c++ hl_lines="4"
    FCakePath ParentSourcePath{ TEXTVIEW("x/game/data")      };
    FCakePath NewParent       { TEXTVIEW("z/network/remote") };

    ParentSourcePath.SetParentPath(NewParent); // Path is now "z/network/remote/data"
    ```
=== "Blueprint"
    {{ bp_img_path('Set Parent Path') }}

To get a copy of a CakePath with a new parent path, we use `CloneWithNewParent`, submitting a CakePath argument that has the new parent path the cloned CakePath should use: 
=== "C++"

    ```c++ hl_lines="4"
    FCakePath SourcePath{ TEXTVIEW("x/game/data")          };
    FCakePath NewParent { TEXTVIEW("z/network/remote")     };

    FCakePath WithNewParent{ SourcePath.CloneWithNewParent(NewParent) };// path is "z/network/remote/data"
    ```
=== "Blueprint"
    {{ bp_img_path('Clone With New Parent') }}

In both examples, the final path will be: `z/network/remote/data`.

### Absolute Paths
CakePath objects can convert from relative paths into absolute paths. When converting relative paths into absolute paths, the location of the executable will be used as the anchor point for expansion. Thus, if we have a relative path `game/data` and our executable resides on `/x/other/game.exe`, converting `game/data` into absolute form will result in the path `/x/other/game/data/`.
However, if a path is already in absolute form then any absolute conversion will have no effect -- this means that __absolute paths not relative to the executable's location will not be changed if an absolute conversion is attempted on them__.

!!! hint
    The executable location used for absolute path conversion will be different when you are running the Unreal Editor versus running a packaged project. Make sure you know the context in which your absolute conversions will be executed to avoid any surprises.

=== "C++"
    We can build an absolute path explicitly from a relative path source with `BuildPathAbsolute`:

    ```c++
    FCakePath AbsolutePath{ FCakePath::BuildPathAbsolute(TEXTVIEW("game/data")) };
    ```
    To build an absolute path from multiple string-like objects, we use `BuildPathCombinedAbsolute`:

    ```c++ 
    FCakePath CombinedAbsPath{ FCakePath::BuildPathCombinedAbsolute( 
			TEXTVIEW("misc/data"), 
			TEXTVIEW("animations/hero") 
		)
	};
    ```
    !!! note
        This function is a variadic template and can accept an indefinite number of string-like arguments.

=== "Blueprint"
    To build a CakePath and ensure it is in absolute form, we use `BuildCakePathAbsolute`.
    {{ bp_img_path('Build Cake Path Absolute') }}

    To build an absolute CakePath combined from two source path strings, use `BuildCakePathCombinedAbsolute`:
    {{ bp_img_path('Build Cake Path Combined Absolute') }}

Using a pre-existing CakePath as the base path, we can create combined absolute paths via `CombineAbsolute`:
=== "C++"

    ```c++ hl_lines="4"
    FCakePath SourceRelative{ TEXTVIEW("src/systems")  };
    FCakePath NetworkDir    { TEXTVIEW("network/main") };

    FCakePath NetworkingPath{ 
        SourceRelative.CombineAbsolute( NetworkDir ) 
    };
    ```
=== "Blueprint"
    {{ bp_img_path('Combine Absolute') }}

To clone a CakePath object and ensure the cloned path is in absolute form use `CloneAbsolute`.
=== "C++"
    ```c++ hl_lines="3"
    FCakePath SourcePath{ TEXTVIEW("other/misc") };

    FCakePath ClonedAbsolutePath { SourcePath.CloneAbsolute() }; 
    ```

=== "Blueprint"
    {{ bp_img_path('Clone Absolute') }}


If we just need the absolute path as a string, we can use `ClonePathStringAbsolute`:

=== "C++"

    ```c++ hl_lines="3"
    FCakePath SourcePath{ TEXTVIEW("other/misc") };

    FString ClonedAbsPathString{ SourcePath.ClonePathStringAbsolute() };
    ```
=== "Blueprint"
    {{ bp_img_path('Clone Path String Absolute') }}

To convert an existing CakePath object to absolute form, we use `ToAbsoluteInline`:

=== "C++"

    ```c++ hl_lines="3"
    FCakePath SourcePath{ TEXTVIEW("other/misc") };

    SourcePath.ToAbsoluteInline();
    ```
=== "Blueprint"
    {{ bp_img_path('To Absolute Inline') }}

### Replacing Subpaths
CakePath objects have an interface to support changing a subpath within their path. A subpath here is defined as a subsection of path components contained in a larger path: e.g., `game/data` is a subpath of `/x/misc/game/data/other`.

As an example, let's say that we are attempting to move a directory tree into another directory, maintaining the relative tree.
=== "C++"
    --8<-- "ad-parampacks.md"

    ```c++ hl_lines="6-9"
    FCakePath    SourcePath{ TEXTVIEW("x/game/data/misc/saves") };
    FCakePath HostDirectory{ TEXTVIEW("x/game/data")            };
    FCakePath DestDirectory{ TEXTVIEW("y/archive/data")         };

    // FinalPath:  "y/archive/data/misc/saves"
    FCakePath FinalPath = SourcePath.CloneWithSubpathReplaced({ 
        .OriginalSubpath = HostDirectory, 
        .NewSubpath      = DestDirectory 
    });

    UE_LOG(LogTemp, Warning, TEXT("ReplaceSubpath path: [%s]"), **FinalPath);
    ```
=== "Blueprint"
    {{ bp_img_path('Clone With Subpath Replaced') }}

In the example above, by using `CloneWithSubpathReplaced` we were able to replace the subpath `x/game/data` with `y/archive/data` while maintaining the rest of the relative tree `misc/saves`. The resultant path is `y/archive/data/misc/saves`.

If we want to change a subpath of an existing CakePath object instead of generating a copy, we can use `SubpathReplaceInline`:

=== "C++"

    ```c++ hl_lines="6-8"
	FCakePath    SourcePath{ TEXTVIEW("x/game/data/misc/saves") };
	FCakePath HostDirectory{ TEXTVIEW("x/game/data")            };
	FCakePath DestDirectory{ TEXTVIEW("y/archive/data")         };

	// SourcePath is now:  "y/archive/data/misc/saves"
	SourcePath.SubpathReplaceInline({ 
        .OriginalSubpath = HostDirectory,
        .NewSubpath      = DestDirectory 
    });

	UE_LOG(LogTemp, Warning, TEXT("SubpathReplaceInline path: [%s]"), **SourcePath); 
    ```
=== "Blueprint"
    {{ bp_img_path('Subpath Replace Inline') }}

As with the previous example, the resultant path is `y/archive/data/misc/saves`.