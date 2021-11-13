%define major 0
# Mandriva suffix
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

%global oname QCoro

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
BuildRequires: cmake(Qt5Network)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: qmake5

%description
The QCoro library provides set of tools to make use of the C++20 coroutines
in connection with certain asynchronous Qt actions.

%package -n %{libname}
Summary:	The QCoro library
Group:		System/Libraries
Provides:   qcoro
Provides:   QCoro

%description -n %{libname}
The QCoro library provides set of tools to make use of the C++20 coroutines
in connection with certain asynchronous Qt actions.

%package -n %{devname}
Summary: Development files for %{name}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Development files for QCoro library.

%prep
%autosetup -p1

%build
# GCC is needed on Cooker or on Clang can't find "threads"
# Reported to upstream: https://github.com/danvratil/qcoro/issues/22
export CC=gcc
export CXX=g++
%cmake  \
    -DCMAKE_BUILD_TYPE=Release \
    -DUSE_QT_VERSION:STRING=5 \
    -DBUILD_TESTING:BOOL=OFF \
    -DQCORO_BUILD_EXAMPLES:BOOL=OFF \
    -DQCORO_ENABLE_ASAN:BOOL=OFF \
    -DQCORO_WITH_QTDBUS:BOOL=ON \
    -DQCORO_WITH_QTNETWORK:BOOL=ON \
    -DOpenGL_GL_PREFERENCE=GLVND
%make_build

%install
%make_install -C build

%files -n %{libname}
%{_libdir}/lib%{appname}*.so.%{major}*

%files -n %{devname}
%doc README.md
%license LICENSES/*
%{_includedir}/%{oname}/
%{_includedir}/%{name}/
%{_libdir}/cmake/%{oname}/
%{_libdir}/lib%{oname}*.so
