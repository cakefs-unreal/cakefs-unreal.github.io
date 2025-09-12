# Services
CakeServices is the low-level API that serves as a bridge between CakeFS and Unreal's low-level filesystem API. The service interfaces are not aware of CakeFS objects and operate entirely on lower level primitive types. CakeFS's objects and higher level APIs were all built on top of CakeFS's services interfaces. While users are free to leverage the CakeServices interfaces to accomplish their goals, be aware that these APIs are less forgiving and offer less convenience than the higher levels of CakeFS.

All of the source code in the CakeServices is fully documented, and one of the best ways to learn how to use CakeServices is to study the implementation of the associated CakeIO object. For instance, if you want to learn how to use the file services, studying the FCakeFile source code is the best place to start.

## Path Services
Path services contains the low-level operations involving filesystem paths. The API is defined in `CakeIO/Services/CakeServicesPath.h`. 

## File Extension Services
File extension services contains the API for all low-level operations involving file extensions. The API is defined in `CakeIO/Services/CakeServicesFileExt.h`. 

## File Services
File services contains the API for all IO operations involving files. The API is defined in `CakeIO/Services/CakeServicesFile.h`. 

## Directory Services
Directory services contains the API for all IO operations involving directories, as well as directory traverasal. The API is defined in `CakeIO/Services/CakeServicesDir.h`. 