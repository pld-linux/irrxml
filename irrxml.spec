#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
#
Summary:	Simple and fast open source XML parser for C++
Summary(pl.UTF-8):	Prosty, szybki, mający otwarte źródła parser XML dla C++
Name:		irrxml
Version:	1.2
Release:	1
License:	Zlib
Group:		Libraries
Source0:	http://downloads.sourceforge.net/irrlicht/%{name}-%{version}.zip
# Source0-md5:	41eabd2d337917c912ee6d28613efebf
URL:		https://www.ambiera.com/irrxml/
BuildRequires:	libstdc++-devel >= 5:3.2
BuildRequires:	libtool >= 2:2
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautocompressdoc	*.chm

%description
irrXML is a simple and fast open source XML parser for C++. The
strenghts of irrXML are its speed and its simplicity. It ideally fits
into realtime projects which need to read XML data without overhead,
like games. irrXML was originally written as part of the Irrlicht
Engine but after it has become quite mature it now has become a
separate project.

%description -l pl.UTF-8
irrXML to prosty i szybki, mający otwarte źródła parser XML dla C++.
Mocnymi stronami irrXML są szybkość i prostota. Idealnie nadaje się do
projektów czasu rzeczywistego, potrzebujących czytać dane XML bez
narzutu, jak gry. irrXML pierowtnie był pisany jako część silnika
Irrlight, ale gdy stał się w miarę dojrzały, został osobnym projektem.

%package devel
Summary:	Header files for IrrXML library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki IrrXML
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 5:3.2

%description devel
Header files for IrrXML library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki IrrXML.

%package static
Summary:	Static IrrXML library
Summary(pl.UTF-8):	Statyczna biblioteka IrrXML
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static IrrXML library.

%description static -l pl.UTF-8
Statyczna biblioteka IrrXML.

%package apidocs
Summary:	API documentation for IrrXML library
Summary(pl.UTF-8):	Dokumentacja API biblioteki IrrXML
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for IrrXML library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki IrrXML.

%prep
%setup -q

%build
cd src
libtool --mode=compile --tag=CXX %{__cxx} %{rpmcppflags} %{rpmcxxflags} -o irrXML.lo -c irrXML.cpp -I.
libtool --mode=link --tag=CXX %{__cxx} %{rpmldflags} %{rpmcppflags} -o libIrrXML.la irrXML.lo -rpath %{_libdir} %{!?with_static_libs:-shared}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir}/irrxml,%{_libdir},%{_examplesdir}/%{name}-%{version}}

libtool --mode=install install src/libIrrXML.la $RPM_BUILD_ROOT%{_libdir}
cp -p src/irrXML.h $RPM_BUILD_ROOT%{_includedir}/irrxml
cp -p example/{test.cpp,config.xml} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# no external dependencies (beside libstdc++)
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libIrrXML.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc changes.txt readme.txt
%attr(755,root,root) %{_libdir}/libIrrXML.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIrrXML.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libIrrXML.so
%{_includedir}/irrxml
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libIrrXML.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/irrXML.chm
%endif
