%undefine __cmake_in_source_build
%global appname QCoro
%global tests 1

Name: qcoro
Version: 0.3.0
Release: 1%{?dist}

License: MIT
Summary: C++ Coroutines for Qt
URL: https://github.com/danvratil/%{name}
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Widgets)

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: ninja-build

%if 0%{?tests}
BuildRequires: cmake(Qt5Concurrent)
BuildRequires: cmake(Qt5Test)
BuildRequires: dbus-x11
%endif

%description
The QCoro library provides set of tools to make use of the C++20 coroutines
in connection with certain asynchronous Qt actions.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -p1

%build
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DUSE_QT_VERSION:STRING=5 \
%if 0%{?tests}
    -DBUILD_TESTING:BOOL=ON \
    -DQCORO_BUILD_EXAMPLES:BOOL=ON \
%else
    -DBUILD_TESTING:BOOL=OFF \
    -DQCORO_BUILD_EXAMPLES:BOOL=OFF \
%endif
    -DQCORO_ENABLE_ASAN:BOOL=OFF \
    -DQCORO_WITH_QTDBUS:BOOL=ON \
    -DQCORO_WITH_QTNETWORK:BOOL=ON \
%cmake_build

%install
%cmake_install

%if 0%{?tests}
%check
%ctest
%endif

%files
%doc README.md
%license LICENSES/*
%{_libdir}/lib%{appname}*.so.0*

%files devel
%{_includedir}/%{appname}/
%{_includedir}/%{name}/
%{_libdir}/cmake/%{appname}/
%{_libdir}/lib%{appname}*.so

%changelog
* Mon Oct 25 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 0.3.0-1
- Updated to version 0.3.0.

* Sat Oct 02 2021 Vitaly Zaitsev <vitaly@easycoding.org> - 0.2.0-1
- Initial SPEC release.
