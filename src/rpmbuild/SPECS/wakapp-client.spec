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
#mkdir -p %{buildroot}/usr/lib/wakapp
#cp /root/rpmbuild/SOURCES/wakapp-client-1.0/install.sh %{buildroot}/usr/lib/wakapp
mkdir -p %{buildroot}/etc/yum.repos.d
cp /root/rpmbuild/SOURCES/wakapp-client-1.0/wakapp.repo %{buildroot}/etc/yum.repos.d/wakapp.repo

%post
/usr/bin/wakapp-client
#/usr/lib/wakapp/install.sh

%postun
userdel -r wakausr >/dev/null 2>&1
sed -i 's/wakausr.*//g' /etc/sudoers 2>&1>/dev/null
#rm -rf /usr/lib/wakapp
rm -f /etc/yum.repos.d/wakapp.repo
rm -f /etc/ansible/facts.d/setuphost.fact

%files
%{_bindir}/%{name}
#/usr/lib/wakapp/install.sh
/etc/yum.repos.d/wakapp.repo

%changelog
