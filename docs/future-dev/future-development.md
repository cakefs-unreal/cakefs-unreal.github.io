# Future Development
CakeFS will continue to be refined and expanded throughout its lifetime. This section will detail some of the future designs planned for CakeFS. 

## Supported Platforms
CakeFS is launching with just one officially supported platform (Windows) in order to focus on initial stability and correctness. While internally CakeFS utilizes Unreal Engine's cross-platform IO API, we want to be absolutely sure that everything works correctly on each target platform before we give an official endorsement.

Expanding the supported platforms is one of the highest priorities for future improvements of CakeFS. CakeFS is being used in production by MakinaCube and we will be increasing the number of supported platforms as fast as possible. If there is a particular platform you want support for, please send us an email at makinacube@gmail.com, with the phrase "CakeFS Supported Platforms" somewhere in the subject line. Customer feedback can help us better prioritize which platforms to add next. 

## Cake Mix Library
Cake Mix library will continue to have utility functions added to it as the library matures. We plan to use feedback from our internal usage of CakeFS as well as customer suggestions / requests to help guide the expansions of Cake Mix. 

One of the major design goals of CakeFS is to keep the core object interfaces as lean as possible without comprimising their power. Cake Mix can help serve as an experimental ground where we add candidate functions that could potentially be added to the core object interface should it prove to be exceptionally useful. This approach will allow us to get production feedback from new functions before having to increase the surface area of a core object's API.

## Cake Async IO
The goals of Cake Async IO differ between the C++ and Blueprint APIs. 

For the C++ API, the goal is to provide a generic solution that is acceptable in a variety of situations. We cannot provide a single, "official" solution since async code is so complex on the C++ side and user contexts will greatly vary. We aim to provide an implementation either helps you get the job done in common situations or serves as a reference point for custom implementations.

For Blueprint the goal is to provide an official implementation since Blueprint's interaction with async code is much more constrained. Furthermore, Blueprint users are likely unable to create their own implementation, and thus we need to offer a solution that is as comprehensive as possible.

The most pressing issue with regard to future development of the Blueprint API is the lack of support for asynchronous directory traversal, batch operations, and custom gather operations. These cannot be achieved right now due to technical limitations of Blueprint / UObject, so the timeline for when (if ever) these features can be implemented is completely unknown. However, we will be monitoring the situation and looking for any opportunity to bring these features to Blueprint users.

Both APIs will continue to expand whenever new Cake Mix or core object interfaces are added that would benefit from an async version. If we discover more interfaces unique to async contexts like batch processing, we will also consider adding these as well.