# User Definition and Setup


## Common Profiles to Make Life Easier
Shells like the default USS Korn shell (```/bin/sh```) or the Bash shell run a
common profile (```/etc/profile``` or ```/etc/bashrc```) for a user when they log
on.  This creates a runtime environment that contains either required or default
settings.  Each user can supplement or override these settings in ```.profile```
or ```.bashrc``` in their home directory.

Here is a set of recommended profiles that illustrate some best practices for USS
users:

- [General default shell profile](./profiles/general_sh_profile.txt)
-
