Name:           wakapp-client
Version:        1.0
Release:        1%{?dist}
Summary:        wakapp client package

License:        GPLv3+
Source0:        %{buildroot}/SOURCES/wakapp-client-1.0.tar.gz

BuildRequires:  gcc make
Requires:       bash sudo python libselinux-python

%description

%prep
%setup -q


%build
make %{?_smp_mflags}

%install
%make_install
mkdir -p %{buildroot}/etc/yum.repos.d
cp /root/rpmbuild/SOURCES/wakapp-client-1.0/wakapp.repo %{buildroot}/etc/yum.repos.d/wakapp.repo

%post
/usr/bin/wakapp-client

%postun
userdel -r wakausr >/dev/null 2>&1
sed -i '/wakausr/d' /etc/sudoers 2>&1>/dev/null
rm -f /etc/yum.repos.d/wakapp.repo
rm -f /etc/ansible/facts.d/setuphost.fact
rm -f /etc/sudoers.d/wakausr

%files
%{_bindir}/%{name}
/etc/yum.repos.d/wakapp.repo

%changelog
