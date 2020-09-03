# Python to C
Calling a C shared library from Python.

It's common for open source projects to have a mix of Python and C.  There are a
number of reasons to do this, and a number of ways to implement it.  The goal of
this example is to show what it takes to bring a mixed Python/C application from
a Linux environment on x86 to z/OS.

We'll look at two interfaces for calling from Python to C - the ctypes api that
is part of the Python standard library, and the C Foreign Function Interface
(CFFI).  CFFI is not part of the standard library, but it is generally well supported
by most Python implementations.  There are other Python packages to do this that
have been tailored to specific environments, but we don't cover them in this example.

## The Sample Application
The application that we'll use for this example implements the Taylor Series method
for estimating Pi.  It's a simple algorithm that we'll implement in C:

- ```pi/4 = 1 - 1/3 + 1/5 - 1/7 + 1/9 - ...```

The Python portion of this application will pass in an ```int``` specifying the number
of stable digits of required, the C routine will pass back a ```double``` value for
the result.  The C routine will be built into a shared library (dll).

## What's the Same, and What's Different?
Much of the core infrastructure needed to build Linux applications natively for
z/OS exists today.  The compilers, interpreters, and runtime libraries are generally
present.  The most apparent differences between the development environments of
Linux and z/OS is in how they operate.

A relevant example of a difference is the C compiler.  Linux applications generally
are built with the _gcc_ or _clang_ compilers, and use the _glibc/LLVM_ libraries.
z/OS has the **XL C** compiler, and **Language Environment (LE)** runtime, and
understanding how the Linux-based CLIs map to the XL C command line interface is
a significant challenge. While the source code for C applications generally does
not have to change when it's brought to z/OS, the makefiles and other build recipes
often need re-engineering.

Another important difference is the default addressing mode of z/OS vs most Linux
environments.  There is a large body of 31-bit code that runs on z/OS, and this is
the addressing mode you get by default.  Python is built as a 64-bit application,
so you need to explicitly specify 64-bit mode.  If your code isn't interfacing with
a z/OS callable service, this is probably something you don't have to think about.

The z/OS LE runtime environment supports two different kinds of call linkage -
OS Linkage (OSLINK), and eXtra Performance linkage (XPLINK).  OSLINK is the legacy
linkage mechanism

In this project we'll use a simple makefile that captures all of the compile and
link arguments for each platform.  This is where the differences and similarities
should be easiest to see.

## The ctypes Interface

## The CFFI Interface

## References
[How is pi (TT) calculated?](https://stackoverflow.com/questions/2654749/how-is-pi-%CF%80-calculated) on Stack Overflow
