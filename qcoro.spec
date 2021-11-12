#undefine __cmake_in_source_build
%global appname QCoro
%global tests 0


%global optflags %{optflags} -pthread

Name: qcoro
Version: 0.3.0
Release: 1
Group:   System/Libraries
License: MIT
Summary: C++ Coroutines for Qt
URL: https://github.com/danvratil/qcoro
Source0: https://github.com/danvratil/qcoro/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: qmake5
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
export CC=gcc
export CXX=g++
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
    -DQCORO_WITH_QTNETWORK:BOOL=ON
%make_build

%install
%make_install -C build

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
