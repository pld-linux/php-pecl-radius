%define		php_name	php%{?php_suffix}
%define		modname		radius
Summary:	Radius client library
Summary(pl.UTF-8):	Biblioteka klienta Radiusa
Name:		%{php_name}-pecl-%{modname}
Version:	1.2.7
Release:	2
License:	BSD
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	6d7ecfebf3f1a337cbe9fdce491aa762
URL:		http://pecl.php.net/package/radius/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires(triggerpostun):	sed >= 4.0
Requires:	php(core) >= 5.0.4
Provides:	php(%{modname}) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package is based on the libradius of FreeBSD. This PECL adds full
support for Radius Authentication (RFC 2865) and Radius Accounting
(RFC 2866). This package is available for Unix and for Windows.

%description -l pl.UTF-8
Ten pakiet jest bazowany na libradius z FreeBSD. Ten PECL dodaje pełne
wsparcie dla autentyfikacji Radius (RFC 2865) oraz dla accountingu
Radius (RFC 2866). Ten pakiet jest osiągalny dla systemów Unix oraz
Windows.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure

%{__make} \
	CPPFLAGS="-DHAVE_CONFIG_H -I/usr/X11R6/include/X11/" \
	CFLAGS_CLEAN="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
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
%{__sed} -i -e '/^extension[[:space:]]*=[[:space:]]*%{modname}\.so/d' %{php_sysconfdir}/php.ini

%files
%defattr(644,root,root,755)
%doc examples/*.php
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
