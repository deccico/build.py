Goals:
=======

To provide a standard consistent interface to compile, test, package all developed software.

High level requirements:
------------------------

* Must be self-contained
* Must return exist codes
* Platform independent
* Must be in version control and sit in the root of the project
* All parts of the specification must be completely implemented, if it's not applicable it must be
mocked.
* Flags can be put together in any order as long as all the requirements are met.

All deploy-able files will be in a defined folder and the predefined structure.

Deployment folder specification
---------------------------------
At the end of every compile the following folder structure is required.

At the root of the checkout. which build.py exists, Structure:


[ROOT of checkout]
|—[SHIP]
    |—[target] (eg: debug)
        |—[product] (all binary files required for deployment,
can be multiple subfolders, must be target machine required structure.)
        |—[unit-test] (all unit test binaries)
        |—[configuration] (all run time configuration)
        |—[database] (all database scripts)

build.py CLI specifications
----------------------------

For the complete list of options, please run:

./build.py --help

