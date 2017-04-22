puppetboard-rpm
===============

WARNING: this is a pre-release ! alpha quality ! 

Builds a rpm for puppetboard with all dependencies included 
in a virtualenv.

Only used on EL7 so far.

Nice to know:

* The WSGI process runs as user `puppetboard`
* Puppetboard settings are to be found in `/etc/opt/voxpupuli/puppetboard/settings.conf`
* Apache config is placed here: `/etc/httpd/conf.d/puppetboard.conf`
* Binaries and python blobs in `/opt/voxpupuli/puppetboard`


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
