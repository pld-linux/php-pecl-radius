%define		_modname	radius
%define		_status		stable
%define		_sysconfdir	/etc/php
Summary:	Radius client library
Summary(pl.UTF-8):	Biblioteka klienta Radiusa
Name:		php-pecl-%{_modname}
Version:	1.2.5
Release:	4
License:	BSD
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	25d867dab8def71ab1b3e2410491ff4d
URL:		http://pecl.php.net/package/radius/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires(triggerpostun):	sed >= 4.0
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package is based on the libradius of FreeBSD. This PECL adds full
support for Radius Authentication (RFC 2865) and Radius Accounting
(RFC 2866). This package is available for Unix and for Windows.

In PECL status of this package is: %{_status}.

%description -l pl.UTF-8
Ten pakiet jest bazowany na libradius z FreeBSD. Ten PECL dodaje pełne
wsparcie dla autentyfikacji Radius (RFC 2865) oraz dla accountingu
Radius (RFC 2866). Ten pakiet jest osiągalny dla systemów Unix oraz
Windows.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure

%{__make} \
	CPPFLAGS="-DHAVE_CONFIG_H -I/usr/X11R6/include/X11/" \
	CFLAGS_CLEAN="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
%{__make} -C %{_modname}-%{version} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%triggerpostun -- %{name} < 1.2.4-4
%{__sed} -i -e '/^extension[[:space:]]*=[[:space:]]*%{_modname}\.so/d' %{php_sysconfdir}/php.ini

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/examples/*.php
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
