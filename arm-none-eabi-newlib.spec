# FORCE NOARCH
# This package is noarch intentionally, although it supplies binaries,
# as they're not intended for the build platform, but for ARM.
# The related discussion can be found here:
# https://www.redhat.com/archives/fedora-devel-list/2009-February/msg02261.html
%global _binaries_in_noarch_packages_terminate_build 0

%global target arm-none-eabi
%global pkg_version 2.2.0-1

Name:           %{target}-newlib
Version:        2.2.0_1
Release:        4%{?dist}
Summary:        C library intended for use on %{target} embedded systems
Group:          Development/Tools
# For a breakdown of the licensing, see NEWLIB-LICENSING
License:        BSD and MIT and LGPLv2+ and ISC
URL:            http://sourceware.org/newlib/
Source0:        ftp://sourceware.org/pub/newlib/newlib-%{pkg_version}.tar.gz
Source1:        README.fedora
Source2:        NEWLIB-LICENSING

BuildRequires:  %{target}-binutils %{target}-gcc %{target}-gcc-c++ texinfo texinfo-tex
BuildArch:      noarch

%description
Newlib is a C library intended for use on embedded systems. It is a
conglomeration of several library parts, all under free software licenses
that make them easily usable on embedded products.

%prep
%setup -q -n newlib-%{pkg_version}


%build
# ARCH AND UBUNTU HAVE
# --enable-newlib-io-long-long \
# --enable-newlib-register-fini \
# ARCH AND UBUNTU DON'T HAVE
# --enable-interwork \
# --enable-multilib \


# END FROM
rm -rf build-{newlib,nano}
mkdir build-{newlib,nano}

pushd build-newlib

export CFLAGS="-g -O2 -ffunction-sections -fdata-sections"
../configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --htmldir=%{_docdir}/html \
    --pdfdir=%{_docdir}/pdf \
    --target=%{target} \
    --enable-interwork \
    --enable-multilib \
    --disable-nls \
    --disable-libssp \
    --disable-nls \
    --disable-newlib-supplied-syscalls \
    --with-float=soft

make

popd
pushd build-nano
export CFLAGS="-g -Os -ffunction-sections -fdata-sections"
../configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --target=%{target} \
    --disable-nls \
    --disable-newlib-supplied-syscalls \
    --enable-newlib-reent-small \
    --disable-newlib-fvwrite-in-streamio \
    --disable-newlib-fseek-optimization \
    --disable-newlib-wide-orient \
    --enable-newlib-nano-malloc \
    --disable-newlib-unbuf-stream-opt \
    --enable-lite-exit \
    --enable-newlib-global-atexit \
    --enable-newlib-nano-formatted-io

make

popd

%install
pushd build-newlib
make install DESTDIR=%{buildroot}
popd
pushd build-nano
NANO_ROOT=%{buildroot}/nano
make install DESTDIR=$NANO_ROOT

for i in $(find $NANO_ROOT -regex ".*/lib\(c\|g\|rdimon\)\.a"); do
    file=$(basename $i | sed "s|\.a|_nano\.a|")
    target_path=$(dirname $i | sed "s|$NANO_ROOT||")
    mv $i "%{buildroot}$target_path/$file"
done
popd

cp %{SOURCE1} .
cp %{SOURCE2} .

# we don't want these as we are a cross version
rm -r %{buildroot}%{_infodir}

rm -rf $NANO_ROOT
# despite us being noarch redhat-rpm-config insists on stripping our files
%if %{fedora}0 > 200
%global __os_install_post /usr/lib/rpm/brp-compress
%else
%global __os_install_post /usr/lib/rpm/redhat/brp-compress
%endif


%files
%defattr(-,root,root,-)
%doc README.fedora
%license NEWLIB-LICENSING COPYING*
%dir %{_prefix}/%{target}
%dir %{_prefix}/%{target}/include/
%{_prefix}/%{target}/include/*
%dir %{_prefix}/%{target}/lib
%{_prefix}/%{target}/lib/*

%changelog
* Mon Aug 31 2015 Michal Hlavinka <mhlavink@redhat.com> - 2.2.0_1-4
- added nano versions of libraries
- cleaned up spec file
- credits: Johnny Robeson

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0_1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 01 2015 Michal Hlavinka <mhlavink@redhat.com> - 2.2.0_1-2
- rebuild for gcc 5.1

* Tue Apr 14 2015 Michal Hlavinka <mhlavink@redhat.com> - 2.2.0_1-1
- newlib updated to 2.2.0_1

* Mon Jun 09 2014 Michal Hlavinka <mhlavink@redhat.com> - 2.1.0-5
- fix FTBFS (#1105970)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Michal Hlavinka <mhlavink@redhat.com> - 2.1.0-3
- enable libnosys (#1060567,#1058722)

* Tue Jan 14 2014 Michal Hlavinka <mhlavink@redhat.com> - 2.1.0-2
- rebuild with newer arm-none-eabi-gcc

* Wed Jan 08 2014 Michal Hlavinka <mhlavink@redhat.com> - 2.1.0-1
- initial import
