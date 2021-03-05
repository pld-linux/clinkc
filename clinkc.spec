#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_with	libxml2		# libxml2 instead of expat
#
Summary:	CyberLink for C UPnP library
Summary(pl.UTF-8):	Biblioteka UPnP CyberLink dla C
Name:		clinkc
Version:	2.4.0
%define	fver	%(echo %{version} | tr -d .)
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://downloads.sourceforge.net/clinkc/%{name}%{fver}.tar.gz
# Source0-md5:	d548ead428419b0e2e521f06cd7b2ddb
Patch0:		%{name}-libtool.patch
Patch1:		%{name}-iconv.patch
Patch2:		%{name}-doc.patch
URL:		https://sourceforge.net/projects/clinkc/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	curl-devel >= 7.13.0
BuildRequires:	doxygen
%{!?with_libxml2:BuildRequires:	expat-devel >= 1.95}
BuildRequires:	libtool
BuildRequires:	libuuid-devel
%{?with_libxml2:BuildRequires:	libxml2-devel >= 1:2.6.0}
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
%{?with_libxml2:Requires:	libxml2 >= 1:2.6.0}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CyberLink for C is a toolkit for creating UPnP devices and control
points. 

%description -l pl.UTF-8
CyberLink dla C to biblioteka narzędziowa do tworzenia urządzeń i
punktów kontrolnych UPnP.

%package devel
Summary:	Header files for clinkc library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki clinkc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{!?with_libxml2:Requires:	expat-devel >= 1.95}
Requires:	libuuid-devel
%{?with_libxml2:Requires:	libxml2-devel >= 1:2.6.0}

%description devel
Header files for clinkc library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki clinkc.

%package static
Summary:	Static clinkc library
Summary(pl.UTF-8):	Statyczna biblioteka clinkc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static clinkc library.

%description static -l pl.UTF-8
Statyczna biblioteka clinkc.

%package apidocs
Summary:	API documentation for clinkc library
Summary(pl.UTF-8):	Dokumentacja API biblioteki clinkc
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for clinkc library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki clinkc.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libclinkc.la
# compiled binaries
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/clinkc-2.3
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/{clinkc-dev,clinkc0}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog
%attr(755,root,root) %{_libdir}/libclinkc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libclinkc.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libclinkc.so
%{_includedir}/cybergarage
%{_pkgconfigdir}/clinkc.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libclinkc.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doxygen/html/*.{css,html,js,png}
%endif
