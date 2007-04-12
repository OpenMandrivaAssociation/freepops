Name:		freepops
Version:	0.0.99
Release:	%mkrel 2

Summary:	POP3 interface to webmail
License:	GPL
Group:		Networking/Mail
Source: 	http://prdownloads.sourceforge.net/freepops/%{name}-%{version}.tar.bz2
URL:		http://www.freepops.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
Requires(post): rpm-helper
Requires(preun):rpm-helper
BuildRequires:	curl-devel openssl-devel expat-devel bison

%description
FreePOPs is a daemon that acts as a local pop3 server, translating
local pop3 requests to remote http requests to supported webmails.

%prep
%setup -q
./configure.sh linux

%build
make all WHERE=/usr/ FORCE_LINK="-L /tmp/freepops-expat/expat/.libs/"

%install
mkdir -p ${RPM_BUILD_ROOT}/%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man1
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/init.d
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/rc3.d
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/sysconfig
make install DESTDIR=${RPM_BUILD_ROOT} WHERE=/usr/
#gzip -9 ${RPM_BUILD_ROOT}/usr/share/man/man1/freepopsd.1
cp buildfactory/freepops.rc.mandriva ${RPM_BUILD_ROOT}/etc/init.d/freepops
chmod a+x ${RPM_BUILD_ROOT}/etc/init.d/freepops
cp buildfactory/freepops.sysconfig ${RPM_BUILD_ROOT}/etc/sysconfig/freepops
mv ${RPM_BUILD_ROOT}/usr/share/doc/freepops/* ${RPM_BUILD_ROOT}/usr/share/doc/freepops-%{version}

%post
%_post_service freepops

%preun
%_preun_service freepops

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-,root,root)
%doc README ChangeLog AUTHORS
%{_bindir}/freepopsd
%{_mandir}/man1/freepopsd.1.bz2
%{_sysconfdir}/init.d/freepops
%config(noreplace) %{_sysconfdir}/sysconfig/freepops
%config(noreplace) %{_sysconfdir}/freepops/config.lua
%{_datadir}/freepops


