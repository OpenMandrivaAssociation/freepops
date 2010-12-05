Name:		freepops
Version:	0.2.9
Release:	%mkrel 4

Summary:	POP3 interface to webmail
License:	GPLv2+
Group:		Networking/Mail
Source: 	http://prdownloads.sourceforge.net/freepops/%{name}-%{version}.tar.gz
Source1:	freepopsd.init.d
Source2:	freepopsd.sysconfig
Source3:	manual.pdf
Patch0:		freepops-0.2.9-fix-str-fmt.patch
Patch1:		freepops-0.2.8-configure.sh.patch
Patch2:		freepops-0.2.7-Makefile.patch
Patch3:		freepops-0.2.0-config.h.patch
#Patch4:		freepops-0.2.0-updater-dialog.patch
Patch5:		freepops-0.2.7-fltk-1.1.9.patch
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
Group: Networking/Mail
Requires: freepops = %{version}-%{release} fltk

%description updater
Fltk based graphical user interface for FreePOPs updating mechanism

%prep
%setup -q

%patch0 -p0
%patch1 -p0 -b .configure
%patch2 -p0 -b .makefile
%patch3 -p0 -b .config
#%patch4 -p0 -b .dialog
%patch5 -p0 -b .fltk

sed -i.debug -e '/getdate.c/s|rm|:|' modules/src/getdate/getdate-curl-7.11.0.diff

cp -p %{SOURCE3} ./

%build
export PKG_CONFIG_PATH=/usr/lib/pkgconfig
./configure.sh linux -lua -fltk-ui

make all WHERE=%{_prefix}/ H="" \
	CC="gcc $RPM_OPT_FLAGS" \
	HCC="gcc $RPM_OPT_FLAGS"


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_datadir}/freepops/lua_unofficial
mkdir -p %{buildroot}%{_datadir}/freepops/lua_updates
mkdir -p %{buildroot}%{_datadir}/freepops/lua_updates/lxp
mkdir -p %{buildroot}%{_datadir}/freepops/lua_updates/browser
mkdir -p %{buildroot}%{_datadir}/freepops/lua_updates/soap

make install DESTDIR=%{buildroot}/
rm -rf %{buildroot}/usr/share/doc/freepops
chmod +x %{buildroot}%{_bindir}/freepops-updater-dialog
chmod +x %{buildroot}%{_bindir}/freepops-updater-fltk

install -p -m755 %{SOURCE1} %{buildroot}%{_initrddir}/freepopsd
install -p -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/freepopsd

%find_lang updater_fltk

%post
%_post_service freepopsd

%preun
%_preun_service freepopsd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc  doc/MANUAL.txt manual.pdf COPYING INSTALL BUILD AUTHORS ChangeLog README README.modules TODO

%{_bindir}/freepopsd
%{_bindir}/freepops-updater-dialog
%{_bindir}/freepops-updater-zenity
%{_datadir}/freepops/*
%{_mandir}/man1/*
%{_initrddir}/freepopsd
%config(noreplace) %{_sysconfdir}/freepops/config.lua
%config(noreplace) %{_sysconfdir}/sysconfig/freepopsd

%files updater -f updater_fltk.lang
%{_bindir}/freepops-updater-fltk
/usr/lib/freepops/updater_fltk.so
