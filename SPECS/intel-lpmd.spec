%global daemon_name intel_lpmd

Name:		intel-lpmd
Version:	0.0.9
Release:	1%{?dist}
Summary:	Intel Low Power Mode Daemon

License:	GPL-2.0-or-later
URL:		https://github.com/intel/intel-lpmd
Source0:	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Drop unused variables https://github.com/intel/intel-lpmd/pull/93
# https://github.com/intel/intel-lpmd/commit/c2cea33c873146f1b6186c02fe79d1a2bb1c7867.patch
Patch1001:      0001-lpmd_util-Remove-unused-variables.patch
# https://github.com/intel/intel-lpmd/commit/311b7929d4c821630fabf5293ec5b4bec5411162.patch
Patch1002:      0002-wlt_proxy-state_manager-Fix-Werror-switch.patch
# https://github.com/intel/intel-lpmd/commit/4277f3496dc51f89ed0815e0f51659338f7a6ba9.patch
Patch1003:      0003-wlt_proxy-state_util-Remove-unused-variables.patch
# https://github.com/intel/intel-lpmd/commit/af6d8f93a0a1041bd936b8901707e1253c5e5279.patch
Patch1004:      0004-wlt_proxy-state_util-Drop-unused-function-read_tsc_c.patch

ExclusiveArch:	x86_64

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcc
BuildRequires:  glib2-devel
BuildRequires:	gtk-doc
BuildRequires:	libnl3-devel
BuildRequires:	libxml2-devel
BuildRequires:	libtool
BuildRequires:	systemd-devel
BuildRequires:	systemd-units
BuildRequires:  upower-devel

%description
Intel Low Power Model Daemon is a Linux daemon used to optimize active idle
power. It selects a set of most power efficient CPUs based on configuration
file or CPU topology. Based on system utilization and other hints, it puts
the system into Low Power Mode by activating the power efficient CPUs and
disabling the rest, and restoring the system from Low Power Mode by activating
all CPUs.

%prep
%autosetup -p1

# fedora path fix
sed -i -e "s|etc|usr/share|" configure.ac

%build
aclocal --install
gtkdocize --copy --flavour no-tmpl
autoreconf --install --verbose
%configure
%make_build

%install
%make_install
install -D -p -m 644 src/%{daemon_name}_dbus_interface.xml %{buildroot}/%{_datadir}/dbus-1/interfaces/org.freedesktop.%{daemon_name}.xml

%post
%systemd_post %{daemon_name}.service

%preun
%systemd_preun %{daemon_name}.service

%postun
%systemd_postun_with_restart %{daemon_name}.service

%files
%license COPYING
%doc README.md
%{_bindir}/%{daemon_name}_control
%{_sbindir}/%{daemon_name}
%dir %{_sysconfdir}/%{daemon_name}
%config(noreplace) %{_sysconfdir}/%{daemon_name}/%{daemon_name}_config.xml
%config(noreplace) %{_sysconfdir}/%{daemon_name}/intel_lpmd_config_F6_M170.xml
%config(noreplace) %{_sysconfdir}/%{daemon_name}/intel_lpmd_config_F6_M189.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.%{daemon_name}.xml
%{_datadir}/dbus-1/system.d/org.freedesktop.%{daemon_name}.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.%{daemon_name}.service
%{_unitdir}/%{daemon_name}.service
%{_mandir}/man5/%{daemon_name}_config.xml.5*
%{_mandir}/man8/%{daemon_name}.8*
%{_mandir}/man8/%{daemon_name}_control.8*

%changelog
* Mon May 05 2025 Kate Hsuan <hpa@redhat.com> - 0.0.9-1
- Update to the upstream version 0.0.9

* Tue Jul 16 2024 Kate Hsuan <hpa@redhat.com> - 0.0.6-1
- Update to upstream release 0.0.6

* Wed May 29 2024 Kate Hsuan <hpa@redhat.com> - 0.0.3-2
- Rebuild for RHEL-9.5
- Resolves: RHEL-20167

* Mon Feb 26 2024 Kate Hsuan <hpa@redhat.com> - 0.0.3-1
- Update to 0.0.3
- Use cpuid() to detect Lcores

* Fri Feb 2 2024 Kate Hsuan <hpa@redhat.com> - 0.0.2-1
- Initial upstream release
