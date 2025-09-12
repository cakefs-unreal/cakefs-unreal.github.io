--8<-- "note-native-only.md"

## TCakeOrder
{{ src_loc_single('TCakeOrder', 'CakeOrders') }}

CakeFS uses the template struct TCakeOrder for IO operations that need to return additional data in addition to the IO operation result. It holds just two member fields: a result type of the operation and the data produced by the operation. The type of data produced will vary based on the operation.

```c++
template<CakeConcepts::CCakeOpResult ResultType, CakeConcepts::CNotPtrOrRef OrderType>
struct CakeFS_API TCakeOrder
{
	ResultType Result{ ResultType::BuildNoOp() };
	OrderType Order{};

	FORCEINLINE operator bool() const { return Result.IsOkStrict(); }

	OrderType& operator*() { return Order; }
};

```

We won't use `TCakeOrder` directly, but instead we will use the alias templates TCakeOrderFile and TCakeOrderDir:

```c++
template<CakeConcepts::CNotPtrOrRef PayloadType>
using TCakeOrderFile = TCakeOrder<FCakeResultFileIO, PayloadType>;

template<CakeConcepts::CNotPtrOrRef PayloadType>
using TCakeOrderDir = TCakeOrder<FCakeResultDirIO, PayloadType>;
```

As we can see from the above declarations, we use `TCakeOrderFile` for any order that wishes to get data from an `FCakeFile`, and we use `TCakeOrderDir` for any order that wishes to get data from an `FCakeDir`.

As a convenience, `TCakeOrder` has an `operator bool` member function defined that returns the result of calling `IsOkStrict` on its result field. This means that with a single check we can confirm that the IO operation occurred, was successful, and that the `Order` member field is valid and holds the desired data.  

```c++ hl_lines="1"
if (TCakeOrderFile<int64> Query = TestFile.QueryFileSizeInBytes())
{
    UE_LOG(LogTemp, Warning, TEXT("File size: [%d] bytes."), Query.Order);
}
```

`operator*` returns a mutable reference to the payload, so we could also write this instead:

```c++ hl_lines="3"
if (TCakeOrderFile<int64> Query = TestFile.QueryFileSizeInBytes())
{
    UE_LOG(LogTemp, Warning, TEXT("File size: [%d] bytes."), *Query);
}
```