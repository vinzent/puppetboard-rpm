# Don't provide python modules!
%global __provides_exclude ^python.*$

Name:           puppetboard        
Version:        0.2.2
Release:        0.0.1%{?dist}
Summary:        PuppetDB frontend

License:        Apache 2.0
URL:            https://github.com/voxpupuli/puppetboard
Source0:        https://github.com/voxpupuli/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        puppetboard-wsgi
Source2:        puppetboard-httpd.conf
Source3:        puppetboard-settings.conf

BuildRequires:  python-virtualenv
Requires:       mod_wsgi python-virtualenv

%description
PuppetDB frontend. Installs Apache config an provides /puppetboard alias.


%prep
%setup -q

%build
echo "BUILD $(pwd)"

%install
mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
mkdir -p $RPM_BUILD_ROOT/etc/opt/voxpupuli/puppetboard
mkdir -p $RPM_BUILD_ROOT/opt/voxpupuli/puppetboard

virtualenv $RPM_BUILD_ROOT/opt/voxpupuli/puppetboard
. $RPM_BUILD_ROOT/opt/voxpupuli/puppetboard/bin/activate
pip install -r requirements.txt

pip install ./

virtualenv --relocatable $RPM_BUILD_ROOT/opt/voxpupuli/puppetboard

cp %{SOURCE1} $RPM_BUILD_ROOT/opt/voxpupuli/puppetboard/bin/puppetboard-wsgi
chmod a+x $RPM_BUILD_ROOT/opt/voxpupuli/puppetboard/bin/puppetboard-wsgi

cp %{SOURCE2} $RPM_BUILD_ROOT/etc/httpd/conf.d/puppetboard.conf

# Named .conf because rpmbuild process will create .pyc/.pyo files in post-scripts
cp %{SOURCE3} $RPM_BUILD_ROOT/etc/opt/voxpupuli/puppetboard/settings.conf

find $RPM_BUILD_ROOT/ -name "*.debug" -delete

sed -i "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT/opt/voxpupuli/puppetboard/bin/activate \
  $RPM_BUILD_ROOT/opt/voxpupuli/puppetboard/bin/activate.csh \
  $RPM_BUILD_ROOT/opt/voxpupuli/puppetboard/bin/activate.fish


%pre
getent group puppetboard >/dev/null || groupadd -r puppetboard
getent passwd puppetboard >/dev/null || \
    useradd -r -g puppetboard -d /opt/voxpupuli/puppetboard -s /sbin/nologin \
      -c "Daemon user for Puppetboard" puppetboard

%files
/opt/voxpupuli/puppetboard
%attr(640, root, puppetboard) %config(noreplace) /etc/opt/voxpupuli/puppetboard/settings.conf
%config(noreplace) /etc/httpd/conf.d/puppetboard.conf
%doc README.rst
%doc CHANGELOG.rst
%doc LICENSE


%changelog
