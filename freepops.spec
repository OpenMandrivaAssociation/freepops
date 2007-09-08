Name:		freepops
Version:	0.2.5
Release:	%mkrel 2

Summary:	POP3 interface to webmail
License:	GPL
Group:		Networking/Mail
Source: 	http://prdownloads.sourceforge.net/freepops/%{name}-%{version}.tar.bz2
Source1:	freepopsd.init.d
Source2:	freepopsd.sysconfig
Source3:	manual.pdf
Patch1:	freepops-0.2.4-configure.sh.patch
Patch2:	freepops-0.2.0-Makefile.patch
Patch3:	freepops-0.2.0-config.h.patch
Patch4:	freepops-0.2.0-updater-dialog.patch
URL:		http://www.freepops.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
Requires(post): rpm-helper
Requires(preun):rpm-helper
BuildRequires:  curl-devel
BuildRequires:  lua-devel >= 5.1
BuildRequires:  expat-devel
BuildRequires:  readline-devel
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  fltk-devel

Requires:	lua >= 5.1 mktemp dialog chkconfig   


%description
FreePOPs is a daemon that acts as a local pop3 server, translating
local pop3 requests to remote http requests to supported webmails.

%package updater
Summary: The new FreePOPs updater (Fltk)
Group: Applications/Internet
Requires: freepops = %{version}-%{release} fltk

%description updater
Fltk based graphical user interface for FreePOPs updating mechanism

%prep
%setup -q

%patch1 -p1 -b .configure
%patch2 -p0 -b .makefile
%patch3 -p0 -b .config
%patch4 -p0 -b .dialog

sed -i.debug -e '/getdate.c/s|rm|:|' modules/src/getdate/getdate-curl-7.11.0.diff

cp -p %{SOURCE3} ./

%build
./configure.sh linux -lua -fltk-ui

make all WHERE=%{_prefix}/ H="" \
	CC="gcc $RPM_OPT_FLAGS" \
	HCC="gcc $RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}%{_initrddir}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/freepops/lua_unofficial
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/freepops/lua_updates
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/freepops/lua_updates/lxp
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/freepops/lua_updates/browser
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/freepops/lua_updates/soap

make install DESTDIR=$RPM_BUILD_ROOT/
rm -rf $RPM_BUILD_ROOT/usr/share/doc/freepops
chmod +x ${RPM_BUILD_ROOT}%{_bindir}/freepops-updater-dialog
chmod +x ${RPM_BUILD_ROOT}%{_bindir}/freepops-updater-fltk

install -p -m755 %{SOURCE1} ${RPM_BUILD_ROOT}%{_initrddir}/freepopsd
install -p -m644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/freepopsd

%post
%_post_service freepops

%preun
%_preun_service freepops

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc  doc/MANUAL.txt manual.pdf COPYING INSTALL BUILD AUTHORS ChangeLog README README.modules TODO

%{_bindir}/freepopsd
%{_bindir}/freepops-updater-dialog
%{_datadir}/freepops/*
%{_mandir}/man1/*
%{_initrddir}/freepopsd
%config(noreplace) %{_sysconfdir}/freepops/config.lua
%config(noreplace) %{_sysconfdir}/sysconfig/freepopsd

%files updater
%{_bindir}/freepops-updater-fltk
%{_libdir}/freepops/updater_fltk.so
