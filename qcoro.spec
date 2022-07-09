%bcond_without qt5
%bcond_without qt6

%define major 0
%define oldlibname %mklibname %{name} %{major}
%define olddevname %mklibname %{name} -d
%define qt5libname %mklibname QCoro5 %{major}
%define qt5devname %mklibname QCoro5 -d
%define qt6libname %mklibname QCoro6 %{major}
%define qt6devname %mklibname QCoro6 -d

%global oname QCoro

Name: qcoro
Version: 0.6.0
Release: 1
Group:   System/Libraries
License: MIT
Summary: C++ Coroutines for Qt
URL: https://github.com/danvratil/qcoro
Source0: https://github.com/danvratil/qcoro/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: ninja

%if %{with qt5}
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Network)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: qmake5
%endif

%if %{with qt6}
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: qmake-qt6
BuildRequires: qt6-cmake
%endif

%description
The QCoro library provides set of tools to make use of the C++20 coroutines
in connection with certain asynchronous Qt actions.

%package -n %{qt5libname}
Summary:	The QCoro library for Qt 5.x
Group:		System/Libraries
Provides:   qcoro
Provides:   QCoro
%rename %oldlibname

%description -n %{qt5libname}
The QCoro library provides set of tools to make use of the C++20 coroutines
in connection with certain asynchronous Qt actions.

%package -n %{qt5devname}
Summary: Development files for %{name} for Qt 5.x
Requires: %{qt5libname} = %{version}-%{release}
%rename %olddevname

%description -n %{qt5devname}
Development files for QCoro library for Qt 5.x

%package -n %{qt6libname}
Summary:	The QCoro library for Qt 6.x
Group:		System/Libraries
Provides:   qcoro-qt6
Provides:   QCoro-qt6

%description -n %{qt6libname}
The QCoro library provides set of tools to make use of the C++20 coroutines
in connection with certain asynchronous Qt actions.

%package -n %{qt6devname}
Summary: Development files for %{name} for Qt 6.x
Requires: %{qt6libname} = %{version}-%{release}

%description -n %{qt6devname}
Development files for QCoro library for Qt 6.x

%prep
%autosetup -p1
%if %{with qt5}
%cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-DUSE_QT_VERSION:STRING=5 \
	-DBUILD_TESTING:BOOL=OFF \
	-DQCORO_BUILD_EXAMPLES:BOOL=OFF \
	-DQCORO_ENABLE_ASAN:BOOL=OFF \
	-DQCORO_WITH_QTDBUS:BOOL=ON \
	-DQCORO_WITH_QTNETWORK:BOOL=ON \
	-DOpenGL_GL_PREFERENCE=GLVND \
	-G Ninja
cd ..
%endif

%if %{with qt6}
CMAKE_BUILD_DIR=build-qt6 %cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-DUSE_QT_VERSION:STRING=6 \
	-DBUILD_TESTING:BOOL=OFF \
	-DQCORO_BUILD_EXAMPLES:BOOL=OFF \
	-DQCORO_ENABLE_ASAN:BOOL=OFF \
	-DQCORO_WITH_QTDBUS:BOOL=ON \
	-DQCORO_WITH_QTNETWORK:BOOL=ON \
	-DOpenGL_GL_PREFERENCE=GLVND \
	-G Ninja
%endif

%build
%if %{with qt5}
%ninja_build -C build
%endif

%if %{with qt6}
%ninja_build -C build-qt6
%endif

%install
%if %{with qt6}
%ninja_install -C build-qt6
%endif

%if %{with qt5}
%ninja_install -C build
%endif

%if %{with qt5}
%files -n %{qt5libname}
%{_libdir}/libQCoro5*.so.%{major}*

%files -n %{qt5devname}
%doc README.md
%license LICENSES/*
%{_includedir}/qcoro5/QCoro/
%{_includedir}/qcoro5/qcoro/
%{_libdir}/cmake/QCoro5/
%{_libdir}/cmake/QCoro5Coro/
%{_libdir}/cmake/QCoro5Core/
%{_libdir}/cmake/QCoro5DBus/
%{_libdir}/cmake/QCoro5Network/
%{_libdir}/libQCoro5*.so
%endif

%if %{with qt6}
%files -n %{qt6libname}
%{_libdir}/libQCoro6*.so.%{major}*

%files -n %{qt6devname}
%doc README.md
%license LICENSES/*
%{_includedir}/qcoro6/QCoro/
%{_includedir}/qcoro6/qcoro/
%{_libdir}/cmake/QCoro6/
%{_libdir}/cmake/QCoro6Coro/
%{_libdir}/cmake/QCoro6Core/
%{_libdir}/cmake/QCoro6DBus/
%{_libdir}/cmake/QCoro6Network/
%{_libdir}/libQCoro6*.so
%endif
