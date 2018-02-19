# Don't provide python modules!
%global __provides_exclude ^python.*$

%define debug_package %{nil}

Name:           puppetboard        
Version:        0.3.0
Release:        0.3.0%{?dist}
Summary:        PuppetDB frontend

License:        Apache 2.0
URL:            https://github.com/voxpupuli/puppetboard
Source0:        https://github.com/voxpupuli/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        puppetboard-pymods-%{version}.tar.gz
Source2:        puppetboard-settings.conf
Source3:        puppetboard.service
Source4:        puppetboard.tmpfiles

BuildRequires: systemd
BuildRequires:  python-virtualenv
Requires:       python-virtualenv
%{?systemd_requires}

%description
PuppetDB frontend

%prep
%setup -q
tar xzf %{SOURCE1}

%build
echo "BUILD $(pwd)"

virtualenv venv
. venv/bin/activate
for mod in $(find ./puppetboard-pymods-%{version} -type f ! -name "*.txt"); do
  pip install --no-index --no-deps $mod
done
pip install ./ --no-index
virtualenv --relocatable venv/

# only supported by Python 3.6 - brp-python-bytecompile fails on this file
rm -f venv/lib/python2.7/site-packages/jinja2/{asyncfilters,asyncsupport}.py
rm -f venv/lib/python2.7/site-packages/gunicorn/workers/_gaiohttp.py

rm -f venv/bin/activate.csh
rm -f venv/bin/activate.fish

sed -i "s|$(pwd)/venv|/opt/voxpupuli/puppetboard|g" venv/bin/activate 

%install
mkdir -p $RPM_BUILD_ROOT/etc/opt/voxpupuli/puppetboard
mkdir -p $RPM_BUILD_ROOT/var/log/puppetboard

mkdir -p $RPM_BUILD_ROOT/opt/voxpupuli
mv venv/ $RPM_BUILD_ROOT/opt/voxpupuli/puppetboard

install -D -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}/puppetboard.service
install -D -m 0644 %{SOURCE4} $RPM_BUILD_ROOT%{_tmpfilesdir}/puppetboard.conf

mkdir -p $RPM_BUILD_ROOT/run/puppetboard

# Named .conf because rpmbuild process will create .pyc/.pyo files in post-scripts
cp %{SOURCE2} $RPM_BUILD_ROOT/etc/opt/voxpupuli/puppetboard/settings.conf


%pre
getent group puppetboard >/dev/null || groupadd -r puppetboard
getent passwd puppetboard >/dev/null || \
    useradd -r -g puppetboard -d /opt/voxpupuli/puppetboard -s /sbin/nologin \
      -c "Daemon user for Puppetboard" puppetboard

%post
CFG=/etc/opt/voxpupuli/puppetboard/settings.conf
if [ -f $CFG ] && ! grep -q '^SECRET_KEY' $CFG; then
  secret_key_generated=$(dd if=/dev/urandom bs=128 count=1 2>/dev/null |  base64 | grep -E -o '[a-zA-Z0-9]' | head -30 | tr -d '\n')
  echo "SECRET_KEY = '$secret_key_generated'" >>$CFG
fi

%systemd_post puppetboard.service

%preun
%systemd_preun puppetboard.service

%postun
%systemd_postun_with_restart puppetboard.service


%files
/opt/voxpupuli/puppetboard
%dir %attr(750, puppetboard, puppetboard) /run/puppetboard
%{_unitdir}/puppetboard.service
%{_tmpfilesdir}/puppetboard.conf
%attr(640, root, puppetboard) %config(noreplace) /etc/opt/voxpupuli/puppetboard/settings.conf
%attr(750, puppetboard, adm) /var/log/puppetboard
%doc README.rst
%doc CHANGELOG.rst
%license LICENSE


%changelog
* Fri Feb 16 2018 Thomas Mueller <thomas@chaschperli.ch> - 0.3.0-0.2.0
- Upgrade to puppetboard 0.3.0
- Remove mod_wsgi, use gunicorn instead
- Add puppetboard.service systemd file (listen: 127.0.0.1:9090)


