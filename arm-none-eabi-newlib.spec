# FORCE NOARCH
# This package is noarch intentionally, although it supplies binaries,
# as they're not intended for the build platform, but for ARM.
# The related discussion can be found here:
# https://www.redhat.com/archives/fedora-devel-list/2009-February/msg02261.html
%global _binaries_in_noarch_packages_terminate_build 0

%global target arm-none-eabi

Name:           %{target}-newlib
Version:        2.1.0
Release:        1%{?dist}
Summary:        C library intended for use on %{target} embedded systems
Group:          Development/Tools
# For a breakdown of the licensing, see NEWLIB-LICENSING 
License:        BSD and MIT and LGPLv2+ and ISC
URL:            http://sourceware.org/newlib/
Source0:        ftp://sourceware.org/pub/newlib/newlib-%{version}.tar.gz
Source1:        README.fedora
Source2:        NEWLIB-LICENSING
BuildRequires:  %{target}-binutils %{target}-gcc %{target}-gcc-c++ texinfo texinfo-tex
BuildArch:      noarch

%description
Newlib is a C library intended for use on embedded systems. It is a
conglomeration of several library parts, all under free software licenses
that make them easily usable on embedded products.

%prep
%setup -q -n newlib-%{version}
rm -rf libgloss
cp %{SOURCE1} .


%build
CFLAGS="-g -O2" ./configure --prefix=%{_prefix} \
  --libdir=%{_libdir} --mandir=%{_mandir} --infodir=%{_infodir} \
  --target=%{target} --enable-interwork --enable-multilib \
  --with-gnu-as --with-gnu-ld --disable-nls --enable-newlib-io-long-long \
  --enable-newlib-register-fini --disable-newlib-supplied-syscalls --disable-libgloss 

make %{?_smp_mflags} || make

%install
make install DESTDIR=$RPM_BUILD_ROOT
# we don't want these as we are a cross version
rm -r $RPM_BUILD_ROOT%{_infodir}

# despite us being noarch redhat-rpm-config insists on stripping our files
%global __os_install_post /usr/lib/rpm/redhat/brp-compress

%files
%defattr(-,root,root,-)
%doc COPYING* README.fedora
%dir %{_prefix}/%{target}
%dir %{_prefix}/%{target}/lib
%{_prefix}/%{target}/include/
%{_prefix}/%{target}/lib/*


%changelog
* Wed Jan 08 2014 Michal Hlavinka <mhlavink@redhat.com> - 2.1.0-1
- initial import
