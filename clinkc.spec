# note: for versions >= 3 (with changed library name) see mupnp.spec
#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_with	libxml2		# libxml2 instead of expat
#
Summary:	CyberLink for C UPnP library
Summary(pl.UTF-8):	Biblioteka UPnP CyberLink dla C
Name:		clinkc
# keep 2.x here for libclinkc name
Version:	2.4.1
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/cybergarage/mupnp/releases
Source0:	https://github.com/cybergarage/mupnp/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	622ba12704305091dbc5978d5a0a49df
Patch0:		%{name}-libtool.patch
Patch1:		%{name}-iconv.patch
Patch2:		%{name}-doc.patch
Patch3:		%{name}-version.patch
Patch4:		%{name}-av.patch
URL:		https://sourceforge.net/projects/clinkc/
BuildRequires:	autoconf >= 2.50
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

%package av
Summary:	CyberLink for C UPnP library - AV component
Summary(pl.UTF-8):	Biblioteka UPnP CyberLink dla C - komponent AV
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description av
CyberLink for C UPnP library - AV component.

%description av -l pl.UTF-8
Biblioteka UPnP CyberLink dla C - komponent AV.

%package av-devel
Summary:	Header files for clinkcav library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki clinkcav
Group:		Development/Libraries
Requires:	%{name}-av = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}

%description av-devel
Header files for clinkcav library.

%description av-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki clinkcav.

%package av-static
Summary:	Static clinkcav library
Summary(pl.UTF-8):	Statyczna biblioteka clinkcav
Group:		Development/Libraries
Requires:	%{name}-av-devel = %{version}-%{release}

%description av-static
Static clinkcav library.

%description av-static -l pl.UTF-8
Statyczna biblioteka clinkcav.

%prep
%setup -q -n mupnp-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

topdir=$(pwd)
cd std/av
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CPPFLAGS="%{rpmcppflags} -I${topdir}/include" \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C std/av install \
	DESTDIR=$RPM_BUILD_ROOT
	
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libclinkc*.la
# compiled binaries
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/clinkc-%{version}/samples
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
%dir %{_includedir}/cybergarage
%{_includedir}/cybergarage/http
%{_includedir}/cybergarage/io
%{_includedir}/cybergarage/net
%{_includedir}/cybergarage/soap
%dir %{_includedir}/cybergarage/upnp
%{_includedir}/cybergarage/upnp/control
%{_includedir}/cybergarage/upnp/event
%{_includedir}/cybergarage/upnp/ssdp
%{_includedir}/cybergarage/upnp/*.h
%{_includedir}/cybergarage/util
%{_includedir}/cybergarage/xml
%{_includedir}/cybergarage/typedef.h
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

%files av
%defattr(644,root,root,755)
%doc std/av/{COPYING,ChangeLog}
%attr(755,root,root) %{_libdir}/libclinkcav.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libclinkcav.so.0

%files av-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libclinkcav.so
%{_includedir}/cybergarage/upnp/std

%if %{with static_libs}
%files av-static
%defattr(644,root,root,755)
%{_libdir}/libclinkcav.a
%endif
