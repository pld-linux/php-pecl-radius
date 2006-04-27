%define		_modname	radius
%define		_status		stable
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)
Summary:	Radius client library
Summary(pl):	Biblioteka klienta Radiusa
Name:		php-pecl-%{_modname}
Version:	1.2.4
Release:	8
License:	PHP/BSD
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	3d48ccb9486b9e8839d814d7ff318091
URL:		http://pecl.php.net/package/radius/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.254
%{?requires_php_extension}
Requires(triggerpostun):	sed >= 4.0
Requires:	%{_sysconfdir}/conf.d
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

install -d $RPM_BUILD_ROOT%{_sysconfdir}/conf.d
%{__make} -C %{_modname}-%{version} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%triggerpostun -- %{name} < 1.2.4-4
%{__sed} -i -e '/^extension[[:space:]]*=[[:space:]]*%{_modname}\.so/d' %{_sysconfdir}/php.ini

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/examples/*.php
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
