%define		_modname	radius
%define		_status		stable

Summary:	Radius client library
Summary(pl):	Biblioteka klienta Radiusa
Name:		php-pecl-%{_modname}
Version:	1.2.4
Release:	3
License:	PHP/BSD
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	3d48ccb9486b9e8839d814d7ff318091
URL:		http://pecl.php.net/package/radius/
BuildRequires:	php-devel
Requires:	php-common
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
This package is based on the libradius of FreeBSD. This PECL adds full
support for Radius Authentication (RFC 2865) and Radius Accounting
(RFC 2866). This package is available for Unix and for Windows.

In PECL status of this package is: %{_status}.

%description -l pl
Ten pakiet jest bazowany na libradius z FreeBSD. Ten PECL dodaje pe³ne
wsparcie dla autentyfikacji Radius (RFC 2865) oraz dla accountingu
Radius (RFC 2866). Ten pakiet jest osi±galny dla systemów Unix oraz
Windows.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure

%{__make} \
	CPPFLAGS="-DHAVE_CONFIG_H -I%{_prefix}/X11R6/include/X11/" \
	CFLAGS_CLEAN="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

cd %{_modname}-%{version}
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install %{_modname} %{_sysconfdir}/php.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove %{_modname} %{_sysconfdir}/php.ini
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/examples/*.php
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
