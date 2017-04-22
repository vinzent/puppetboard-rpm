puppetboard-rpm
===============

Builds a rpm for puppetboard with all dependencies included 
in a virtualenv.

Only used on EL7 so far.


Howto build
-----------

Prerequisites: 

```
yum install python-virtualenv rpm-build gcc rpmdevtools
```

Download sources:

```
cd SOURCES && spectool -g ../SPECS/puppetboard.spec
```

Build:

```
# Paths got too long when I built in my homedir
BUILDROOT=$(mktemp -d /tmp/rpmbuild.XXXXXXX)

QA_SKIP_BUILD_ROOT=1 rpmbuild -bb --define "_topdir $(pwd)" --define "_buildrootdir $BUILDROOT" SPECS/puppetboard.spec
```
