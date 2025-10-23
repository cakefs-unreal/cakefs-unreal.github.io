--8<-- "note-native-only.md"

## TCakeOrder
{{ src_loc_single('TCakeOrder', 'CakeOrders') }}

CakeFS uses the template struct TCakeOrder for IO operations that need to return additional data in addition to the IO operation result. It holds just two member fields: a result type named `Result` and the data produced by the operation named `Order`. 

We won't use `TCakeOrder` directly, but instead we will use the alias templates `TCakeOrderFile` and `TCakeOrderDir`, for file and directory operations respectively. These use their associated IO result (e.g., FCakeResultFileIO for TCakeOrderFile), and the `Order` field's type will vary based on the operation being performed.

Let's take a look at a simple CakeFile example.

```c++ hl_lines="4"
FCakeFile TestFile{ TEXTVIEW("X:/game/enemies/goblin.dat") };

TCakeOrderFile<int64> Query{
	TestFile.QueryFileSizeInBytes()
};

if ( Query.IsValid() )
{
	UE_LOG(LogTemp, Warning, 
		TEXT("File size: [%d] bytes."), 
		Query.Order
	);
}
```
Our template parameter needs to be `int64`, which will hold our file size in bytes. While we could directly check the result type held within Query, it's more convenient to use the function `IsValid` which will return true if the operation succeeded.

We can access the filesize data using the `Order` member field. Alternatively, we can use `operator*` to achieve the same effect.


```c++ hl_lines="4"
FCakeFile TestFile{ TEXTVIEW("X:/game/enemies/goblin.dat") };

TCakeOrderFile<int64> Query{
	TestFile.QueryFileSizeInBytes()
};

if ( Query.IsValid() )
{
	UE_LOG(LogTemp, Warning, 
		TEXT("File size: [%d] bytes."), 
		*Query
	);
}
```