# zos-native
Resources for using and porting code to the Unix environment of z/OS

## Introduction
z/OS has had a POSIX-compliant Unix environment called Unix System Services (USS)
since 1998. It contains the same basic infrastructure common to Unix platforms, like
a common runtime library, a tree-based file system (zfs), a shell, some key languages -
like C, Java, and Python, and an assortment of common Unix commands.

USS should be thought of as a base layer of enabling technology that other layers
build upon.  It shouldn't be thought of as a modern development environment.  One of
the primary opportunities for this project, and related projects like
[Zowe](https://www.zowe.org/) is to build out the pipelines, workflows, and
infrastructure configurations that enable modern DevOPs.

There are several similarities and differences between z/OS and Unix or Linux platforms.
Our [things to know](https://github.com/ambitus/ambitus/blob/master/things_to_know.md) page
lists several of these, and can be useful for new developers who need to understand the
USS environment better, as well as experienced system programmers who need to know
more about the open source world.

## Common Development and Operations Configuration
Getting started with open source in z/OS native (container-less) environment involves
some key definition and configuration steps:

- [Defining USS users](./user_definition_setup.md)
- [Allocating and mounting filesystems](./filesystem_setup.md)
- [Setting up a build environment](./build_setup.md)
