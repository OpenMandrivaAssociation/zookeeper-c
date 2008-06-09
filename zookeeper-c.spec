%define	major 2
%define libname	%mklibname zookeeper %{major}
%define develname %mklibname zookeeper -d

Summary:	Zookeeper C client library
Name:		zookeeper-c
Version:	2.1.0
Release:	%mkrel 1
License:	Apache License
Group:		System/Libraries
URL:		http://zookeeper.sourceforge.net/
Source0:	http://dfn.dl.sourceforge.net/sourceforge/zookeeper/%{name}-%{version}.tgz
Patch0:		zookeeper-autopoo_fixes.diff
BuildRequires:	cppunit-devel >= 1.10.2
BuildRequires:	dos2unix
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This package provides a C client interface to Zookeeper server. For general
information about Zookeeper please see http://zookeeper.wiki.sourceforge.net/
							    
%package -n	%{libname}
Summary:	Zookeeper C client library
Group:		System/Libraries

%description -n	%{libname}
This package provides a C client interface to Zookeeper server. For general
information about Zookeeper please see http://zookeeper.wiki.sourceforge.net/

%package -n	%{develname}
Summary:	Development files for the %{libname} library
Group:		Development/C
Requires:	%{libname} >= %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
Development files for the %{libname} library.

%package -n	zookeeper
Summary:	Zookeeper C client library utilities
Group:		System/Servers

%description -n	zookeeper
Zookeeper C client library utilities

%prep

%setup -q
%patch0 -p0

dos2unix ChangeLog LICENSE README

# fix version
perl -pi -e "s|1\.1\.3|%{version}|g" configure.*

%build
autoreconf -fis

%configure2_5x \
    --disable-rpath \
    --with-syncapi

%make

make doxygen-doc

%check
make check

%install
rm -rf %{buildroot}

%makeinstall_std

# cleanup
rm -f docs/html/*.map

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n zookeeper
%defattr(-,root,root)
%{_bindir}/cli_mt
%{_bindir}/cli_st
%{_bindir}/load_gen

%files -n %{libname}
%defattr(-,root,root)
%doc ChangeLog LICENSE README
%{_libdir}/lib*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc docs/html/*
%dir %{_includedir}/zookeeper
%{_includedir}/zookeeper/*.h
%{_libdir}/*.so
%{_libdir}/*.*a

