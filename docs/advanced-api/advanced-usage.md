# Advanced CakeFS
Welcome to the advanced section of CakeFS! All of the sections in this area will assume that users are comfortable and familiar with fundamental principles established in the [Core API](/core-api) section.

## Utility Libraries 
There are two higher level library implementations that are built on CakeFS's core objects: CakeMix and Async CakeFS. 

### CakeMix 
{{ link_cakemix() }} is a utility library that offers a variety of high level operations on CakeDir, CakeFile, and CakePath objects. This library is meant to serve as a starting point for users who are seeking a prebuilt solution to some common, complex IO operations. It also serves as an experimental grounds where CakeFS can test out designs and interfaces that might some day be promoted to the Core API. 

### Async CakeFS
{{ link_cake_async() }} is a library that offers asynchronous versions of CakeFS and CakeMix operations.  

## CakeFS Services
The {{ link_cakeservices() }} are the lowest level of CakeFS. They are the interfaces that wrap the underlying Unreal IO operations, and they are what the core CakeFS objects are built upon. C++ users of CakeFS can also take advantage of this API when they desire to build their own solutions if the core objects are insufficient for their needs. Be warned, though, the service APIs are much lower level and error-prone than using the Core API!

