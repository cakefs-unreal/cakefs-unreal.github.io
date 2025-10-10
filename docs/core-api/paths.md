## Overview
CakePath objects provide an ergonomic and standardized way to work with filesystem paths in Unreal Engine. 

### Source Code Information
{{ cpp_impl_source('FCakePath', 'CakePath') }}

## Basic Usage
In this section we will cover the fundamental CakePath operations. Once you are comfortable using CakePaths, consider looking at the advanced usage section for examples of more complex operations.

### Building CakePath Objects
Making a CakePath object is simple, we just need to pass a string that represents our desired filesystem path:

=== "C++"

    ```c++
    FCakePath DataDir{ TEXTVIEW("X:\\game\\data") };
    ```
=== "Blueprint"
    {{ bp_img_path('Make Cake Path Back Slash') }}

CakePath objects ensure that path separators are standardized, so it doesn't matter if we use UNIX or Windows-style path separators.

=== "C++"

    ```c++
    FCakePath DataDir{ TEXTVIEW("X:/game/data") };
    ```
=== "Blueprint"
    {{ bp_img_path('Make Cake Path Forward Slash') }}

To build a single path by combining multiple path strings, we can use `BuildPathCombined`:

=== "C++"

    ```c++ hl_lines="4"
    FString GameDir{ TEXT("X:/game") };

    FCakePath DataDir{ 
        FCakePath::BuildPathCombined( GameDir, TEXTVIEW("data") ) 
    };
    ```
=== "Blueprint"
    {{ bp_img_path('Build Path Combined') }}

In the example above, the path of the object returned would be `X:/game/data`.


To get an independent copy of an existing CakePath, we use `Clone`:
=== "C++"

    ```c++ hl_lines="3"
    FCakePath SourcePath{ TEXTVIEW("/x/game/data") };

    FCakePath ClonedPath{ SourcePath.Clone() };
    ```

=== "Blueprint"
    {{ bp_img_path('Clone') }}

### Reading the Path String
To read a CakePath's path string we use `GetPathString`:

=== "C++"

    ```c++ hl_lines="7-8"
    auto PrintPath = [](const FString& Path) { 
        UE_LOG(LogTemp, Warning, TEXT("Path: [%s]"), *Path) 
    };

    FCakePath SourcePath{ TEXT("/x/game/data") };

    PrintPath(SourcePath.GetPathString()); // => "/x/game/data"
    PrintPath(*SourcePath); // => "/x/game/data"
    ```

    !!! note
        `operator*` achieves the same effect.

=== "Blueprint"
    {{ bp_img_path('Get Path String') }}

We can get an independent copy of the path string via `ClonePathString`:

=== "C++"

    ```c++ hl_lines="3"
    FCakePath SourcePath{ TEXT("/x/game/data") };

    FString PathString{ SourcePath.ClonePathString() };
    ```

=== "Blueprint"
    {{ bp_img_path('Clone Path String') }}

### Modifying Paths

We can change the path of an existing CakePath via `SetPath`, sending either a string or another CakePath object that holds the new path.

=== "C++"

    ```c++ hl_lines="4"
    FCakePath SourcePath{ TEXTVIEW("/x/game/data") };

    // FStringView overload
    SourcePath.SetPath(TEXTVIEW("Y:/network/profiling/"));
    ```
    ```c++ hl_lines="5"
    FCakePath SourcePath{ TEXTVIEW("/x/game/data") };
	FCakePath MapPath   { TEXTVIEW("/x/game/maps") };

    // FCakePath overload
    SourcePath.SetPath(MapPath);
    ```

    If we want to employ move semantics, we can use `StealPath`:

    ```c++ hl_lines="4"
    FCakePath SourcePath{ TEXTVIEW("/x/game/data") };
	FCakePath MapPath   { TEXTVIEW("/x/game/maps") };

    SourcePath.StealPath( MoveTemp(MapPath) );
    ```

    !!! note
        We could have used the move constructor instead of `StealPath`. Use whichever you prefer.

=== "Blueprint"
    {{ bp_img_path('Set Path String') }}
    {{ bp_img_path('Set Path Cake Path') }}


To check if a CakePath's path is empty, we use `IsEmpty`:
=== "C++"

    ```c++ hl_lines="3"
    FCakePath SourcePath{ TEXTVIEW("/x/game/data") };

    const bool bPathIsEmpty{ SourcePath.IsEmpty() }; // => false
    ```

=== "Blueprint"
    {{ bp_img_path('Is Empty') }}


To reset a CakePath's path back to an empty string, we use `Reset`:
=== "C++"

    ```c++ hl_lines="3"
    FCakePath SourcePath{ TEXTVIEW("/x/game/data") };

    SourcePath.Reset();
    const bool bPathIsEmpty{ SourcePath.IsEmpty() }; // => true
    ```

=== "Blueprint"
    {{ bp_img_path('Reset') }}

!!! note
    `Reset` takes an optional size parameter that will ensure the path string's buffer is at least as large as the size argument. If you don't need a specific size, just leave this at zero.


### Combining Paths
To combine a CakePath object's path with another, we use `Combine`. We can use `Combine` with a string or another CakePath object.

=== "C++"

    !!! note
        `operator/` can be used for an equivalent effect.

    ```c++ hl_lines="4 5"
    // FStringView overload
	FCakePath PathGame{ TEXTVIEW("/x/game/") };

	FCakePath FullHeroPath  { PathGame.Combine(TEXTVIEW("hero/hero.fbx")) };
	FCakePath FullHeroPathOp{ PathGame / TEXTVIEW("hero/hero.fbx")        };
    ```

    ```c++ hl_lines="5 6"
    // CakePath overload
	FCakePath PathGame    { TEXTVIEW("/x/game/")       };
	FCakePath PathHeroFile{ TEXTVIEW("hero/hero.fbx")  };

	FCakePath FullHeroPath  { PathGame.Combine(PathHeroFile) };
	FCakePath FullHeroPathOp{ PathGame / PathHeroFile        };
    ```

=== "Blueprint"
    {{ bp_img_path('Combine String') }}
    {{ bp_img_path('Combine Cake Path') }}

In the example above, the returned CakePath object's path will be `/x/game/hero/hero.fbx`.

To perform the combination directly on the source CakePath object, we can use `CombineInline`:
=== "C++"

    ```c++ hl_lines="6 9"
    // FStringView overload
    FCakePath PathMisc   { TEXTVIEW("/y/misc")         };
    FCakePath PathItemsDb{ TEXTVIEW("items/items.db") };

    FCakePath PathCombineInline{ PathMisc };
    PathCombineInline.CombineInline( TEXTVIEW("items/items.db") ); // => "/y/misc/items/items.db"

    FCakePath PathCombineOperator{ PathMisc };
    PathCombineOperator /= TEXTVIEW("items/items.db"); // => "/y/misc/items/items.db"
    ```

    ```c++ hl_lines="6 9"
    // CakePath overload
    FCakePath PathMisc   { TEXTVIEW("/y/misc")         };
    FCakePath PathItemsDb{ TEXTVIEW("items/items.db") };

    FCakePath PathCombineInline{ PathMisc };
    PathCombineInline.CombineInline(PathItemsDb); // => "/y/misc/items/items.db"

    FCakePath PathCombineOperator{ PathMisc };
    PathCombineOperator /= PathItemsDb; // => "/y/misc/items/items.db"
    ```

=== "Blueprint"
    {{ bp_img_path('Combine Inline String') }}
    {{ bp_img_path('Combine Inline Cake Path') }}

In the example above, the target CakePath object's path will be `/y/misc/items/items.db`.

### Path Equality
Path equality in CakeFS is simple: two CakePath objects are equal if they refer to the same location on the filesystem. We use `operator==` and `operator!=` for equality comparisons.
=== "C++"

    ```c++ hl_lines="5 6"
    FCakePath PathData{ TEXTVIEW("/x/game/data") };
    FCakePath PathMisc{ TEXTVIEW("/y/game/misc") };

    bool bPathsAreEqual{ false };
    bPathsAreEqual = PathData == PathMisc;      // => false
    bPathsAreEqual = PathData != PathMisc;      // => true
    ```

=== "Blueprint"
    {{ bp_img_path('Is Equal To') }}
    {{ bp_img_path('Is Not Equal To') }}

## Advanced Usage

### Path Leaf Manipulation
The leaf of the path is its rightmost component. Given the path `x/game/data`, the leaf is `data`.

#### Leaf Extraction
To extract the leaf of a CakePath object as another CakePath object, we use `CloneLeaf`:
=== "C++"

    ```cpp hl_lines="3"
    FCakePath SourcePath{ TEXTVIEW("/x/game/data") };

    FCakePath PathLeaf{ SourcePath.CloneLeaf() }; // => "data"
    ```

=== "Blueprint"
    {{ bp_img_path('Clone Leaf') }}

To get the leaf of a CakePath object as a string, we use `CloneLeafString`:
=== "C++"

    ```cpp hl_lines="3"
    FCakePath SourcePath{ TEXTVIEW("/x/game/data") };

    FString LeafString{ SourcePath.CloneLeafString() }; // => "data"
    ```

=== "Blueprint"
    {{ bp_img_path('Clone Leaf String') }}

!!! note
    The leaf can be empty, so don't forget to check in the situations where that matters.

#### Modifying the Leaf
We can change the leaf of a CakePath via `SetLeaf`, passing either a string or CakePath that contains the new leaf.
=== "C++"

    ```c++ hl_lines="4"
    // FStringView overload
    FCakePath SourcePath{ TEXTVIEW("/x/game/data") };

    SourcePath.SetLeaf( TEXTVIEW("items") ); // path is now "/x/game/items"
    ```

    ```c++ hl_lines="5"
    // FCakePath overload
    FCakePath SourcePath{ TEXTVIEW("/x/game/data") };
    FCakePath Leaf      { TEXTVIEW("items")        };

    SourcePath.SetLeaf(Leaf); // path is now "/x/game/items"
    ```
=== "Blueprint"
    {{ bp_img_path('Set Leaf') }}

In the example above, the path is `/x/game/items` after the leaf has been changed.

We can get a copy of the CakePath with a new leaf via `CloneWithNewLeaf`, submitting a string or CakePath argument that holds the new leaf:
=== "C++"

    ```c++ hl_lines="5"
    // FStringView overload
	FCakePath SourcePath{ TEXTVIEW("/x/game/data") };

	FCakePath WithNewLeaf{ 
		SourcePath.CloneWithNewLeaf(TEXTVIEW("items")) 
	};// path is "/x/game/items"
    ```

    ```c++ hl_lines="6"
    // FCakePath overload
    FCakePath SourcePath{ TEXTVIEW("/x/game/data") };
    FCakePath NewLeaf   { TEXTVIEW("items")        };

    FCakePath WithNewLeaf{ 
        SourcePath.CloneWithNewLeaf(NewLeaf) 
    };// path is "/x/game/items"
    ```
=== "Blueprint"
    {{ bp_img_path('Clone With New Leaf') }}

In the example above, the path is `/x/game/items` after the leaf has been changed.

!!! note 
    Even though the examples show changing the leaf with single-component paths, leaf manipulation methods can also change the leaf with a multi-component path as well. 

### Parent Path Manipulation
The parent path of a given path is all path components to the left of the path leaf; the parent path of `/x/game/data` is `/x/game/`.

#### Parent Path Extraction
To clone a CakePath's parent path as a new CakePath object, we use `CloneParentPath`:
=== "C++"

    ```cpp hl_lines="3"
    FCakePath SourcePath{ TEXTVIEW("/x/game/data") };

    FCakePath ParentPath{ SourcePath.CloneParentPath() };
    ```

=== "Blueprint"
    {{ bp_img_path('Clone Parent Path') }}

In the example above, the cloned parent path is `/x/game`.

When we want the parent path as a string, we can use `CloneParentPathString`:

=== "C++"

    ```cpp hl_lines="3"
    FCakePath SourcePath{ TEXTVIEW("/x/game/data") };

    FString ParentPathString{ SourcePath.CloneParentPathString() };
    ```

=== "Blueprint"
    {{ bp_img_path('Clone Parent Path String') }}

In the example above, the cloned parent path string is `/x/game`.

!!! note
    The parent path can always be empty, so don't forget to check in the situations where that matters.

#### Modifying the Parent Path
We can modify the parent path of an existing CakePath object via `SetParentPath`, submitting a string or CakePath that holds the new parent path.

=== "C++"

    ```c++ hl_lines="5"
    // FStringView overload
    FCakePath ParentSourcePath{ TEXTVIEW("/x/game/data")      };
    FString   NewParent       { TEXTVIEW("/z/network/remote") };

    ParentSourcePath.SetParentPath(NewParent); // Path is now "/z/network/remote/data"
    ```
    ```c++ hl_lines="5"
    // FCakePath overload
    FCakePath ParentSourcePath{ TEXTVIEW("/x/game/data")      };
    FCakePath NewParent       { TEXTVIEW("/z/network/remote") };

    ParentSourcePath.SetParentPath(NewParent); // Path is now "/z/network/remote/data"
    ```

=== "Blueprint"
    {{ bp_img_path('Set Parent Path') }}

In the example above, the path is `/z/network/remote/data` after changing the parent.

To get a copy of a CakePath with a new parent path, we use `CloneWithNewParent`, submitting a string or CakePath argument holds the new parent path:
=== "C++"

    ```c++ hl_lines="6"
    // FStringView overload
    FCakePath SourcePath{ TEXTVIEW("/x/game/data")          };
    FString   NewParent { TEXTVIEW("/z/network/remote")     };

    FCakePath WithNewParent{ 
        SourcePath.CloneWithNewParent(NewParent) 
    };// path is "/z/network/remote/data"
    ```
    ```c++ hl_lines="6"
    // FCakePath overload
    FCakePath SourcePath{ TEXTVIEW("/x/game/data")          };
    FCakePath NewParent { TEXTVIEW("/z/network/remote")     };

    FCakePath WithNewParent{ 
        SourcePath.CloneWithNewParent(NewParent) 
    };// path is "/z/network/remote/data"
    ```
=== "Blueprint"
    {{ bp_img_path('Clone With New Parent') }}

In the example above, the final path will be: `/z/network/remote/data`.

### Absolute Paths
CakePath objects can convert from relative paths into absolute paths. When converting relative paths into absolute paths, the location of the executable will be used as the anchor point for expansion. Thus, if we have a relative path `game/data` and our executable resides on `/x/other/game.exe`, converting `game/data` into absolute form will result in the path `/x/other/game/data/`.
However, if a path is already in absolute form then any absolute conversion will have no effect -- this means that __absolute paths not relative to the executable's location will not be changed if an absolute conversion is attempted on them__.

!!! hint
    The executable location used for absolute path conversion will be different when you are running the Unreal Editor versus running a packaged project. Make sure you know the context in which your absolute conversions will be executed to avoid any surprises.

To build an absolute path explicitly, we use `BuildPathAbsolute`:
=== "C++"

    ```c++ hl_lines="2"
    FCakePath AbsolutePath{ 
        FCakePath::BuildPathAbsolute( TEXTVIEW("game/data") ) 
    };
    ```
=== "Blueprint"
    {{ bp_img_path('Build Path Absolute') }}

To build an absolute path from two or more path strings, we use `BuildPathCombinedAbsolute`:
=== "C++"

    ```c++ hl_lines="2-5"
    FCakePath CombinedAbsPath{ 
		FCakePath::BuildPathCombinedAbsolute( 
			TEXTVIEW("misc/data"), 
			TEXTVIEW("animations/hero") 
		)
	};
    ```
=== "Blueprint"
    {{ bp_img_path('Build Path Combined Absolute') }}

Using a pre-existing CakePath as the base path, we can create combined absolute paths via `CombineAbsolute`:

=== "C++"

    ```c++ hl_lines="6"
    // FStringView overload
    FCakePath SourceRelative{ TEXTVIEW("src/systems")  };
    FString   NetworkDir    { TEXTVIEW("network/main") };

    FCakePath NetworkingPath{ 
        SourceRelative.CombineAbsolute( NetworkDir ) 
    };
    ```
    ```c++ hl_lines="6"
    // FCakePath overload
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

    ```c++ hl_lines="4"
    FCakePath SourcePath{ TEXTVIEW("other/misc") };

    FString ClonedAbsPathString{ 
        SourcePath.ClonePathStringAbsolute() 
    };
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

    ```c++ hl_lines="5-9"
    FCakePath    SourcePath{ TEXTVIEW("/x/game/data/misc/saves") };
    FCakePath HostDirectory{ TEXTVIEW("/x/game/data")            };
    FCakePath DestDirectory{ TEXTVIEW("/y/archive/data")         };

    FCakePath FinalPath  = SourcePath.CloneWithSubpathReplaced({ 
        .OriginalSubpath = HostDirectory, 
        .NewSubpath      = DestDirectory 
    });

    // FinalPath: "/y/archive/data/misc/saves"
    UE_LOG(LogTemp, Warning, TEXT("ReplaceSubpath path: [%s]"), **FinalPath);
    ```
=== "Blueprint"
    {{ bp_img_path('Clone With Subpath Replaced') }}

In the example above, by using `CloneWithSubpathReplaced` we were able to replace the subpath `/x/game/data` with `/y/archive/data` while maintaining the rest of the relative tree `misc/saves`. The resultant path is `/y/archive/data/misc/saves`.

If we want to change a subpath of an existing CakePath object instead of generating a copy, we can use `SubpathReplaceInline`:

=== "C++"

    ```c++ hl_lines="5-8"
	FCakePath    SourcePath{ TEXTVIEW("x/game/data/misc/saves") };
	FCakePath HostDirectory{ TEXTVIEW("x/game/data")            };
	FCakePath DestDirectory{ TEXTVIEW("y/archive/data")         };

	SourcePath.SubpathReplaceInline({ 
        .OriginalSubpath = HostDirectory,
        .NewSubpath      = DestDirectory 
    });

	// SourcePath is now: "/y/archive/data/misc/saves"
	UE_LOG(LogTemp, Warning, TEXT("SubpathReplaceInline path: [%s]"), **SourcePath); 
    ```

=== "Blueprint"
    {{ bp_img_path('Subpath Replace Inline') }}

As with the previous example, the resultant path is `/y/archive/data/misc/saves`.