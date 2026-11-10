%global daemon_name intel_lpmd

Name:		intel-lpmd
Version:	0.1.0
Release:	1%{?dist}

Summary:	Intel Low Power Mode Daemon

License:	GPL-2.0-or-later
URL:		https://github.com/intel/intel-lpmd
Source0:	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Rebase to the latest commits
Patch1001:      0001-Deprecate-the-dbus-glib-dependency-at-Install-Depend.patch
Patch1002:      0002-lpmd_cpu-Tablets-are-also-a-Mobile-platform.patch
Patch1003:      0003-build-replace-open-coded-if-in-configure.ac-with-AS_.patch
Patch1004:      0004-build-avoid-use-of-test-.-a.patch
Patch1005:      0005-build-fix-spelling-in-error-message-when-libsystemd-.patch
Patch1006:      0006-build-apply-consistent-argument-quoting-in-configure.patch
Patch1007:      0007-lpmd_cgroup-simple-isolation-fix-works-without-inter.patch
Patch1008:      0008-state_machine-Fix-issue-106-incorrect-order-of-polli.patch
Patch1009:      0009-lpmd_state_machine-Fix-deadlock-on-power-profile-swi.patch
Patch1010:      0010-Process-itmt-read-error.patch
Patch1011:      0011-lpmd_misc-Fix-ITMT.patch
Patch1012:      0012-make-itmt_init-to-void.patch
Patch1013:      0013-config-Fix-incorrect-cpu-numbers.patch
Patch1014:      0014-readme-Reformat-long-lines-into-markdown-readable-bl.patch
Patch1015:      0015-readme-Emphasize-expectations-from-the-user.patch
Patch1016:      0016-man-Update-the-main-man-page.patch
Patch1017:      0017-man-Update-lpmd-control-utility-man-page.patch
Patch1018:      0018-man-Generic-updates-to-the-config-man-page.patch
Patch1019:      0019-man-Move-unused-config-options-to-the-unused-section.patch
Patch1020:      0020-Add-Panther-Lake-4P0E4L.patch
Patch1021:      0021-Remove-power-group.patch
Patch1022:      0022-Add-GetState-D-Bus-method-to-query-current-LPM-contr.patch
Patch1023:      0023-fix-restore-systemd-unit-install-path.patch
Patch1024:      0024-fix-prevent-cgroup-isolation-churn-during-WLT-pollin.patch
Patch1025:      0025-Fix-build-breakage-with-the-last-commit.patch
Patch1026:      0026-git-Setup-gitignore.patch
Patch1027:      0027-lpmd_config-Cleanup-code-indentation-in-parse-states.patch
Patch1028:      0028-lpmd_config-Rename-island-number-cores-tags.patch
Patch1029:      0029-lpmd_state_machine-Count-system-of-specifing-active-.patch
Patch1030:      0030-lpmd_cpumask-Dynamic-core-type-cpumask-allocation.patch
Patch1031:      0031-lpmd_config-ALL-keyword-for-active-P-E-L-cores-tag.patch
Patch1032:      0032-config-Simplify-the-M204-configuration.patch
Patch1033:      0033-lpmd_cpu-Fix-incorrect-struct-initialization.patch
Patch1034:      0034-Introduce-WLT-state-mask-and-notification-delay.patch
Patch1035:      0035-Arrow-Lake-enabling.patch
Patch1036:      0036-lpmd_config-Skip-platform-check-if-a-matching-config.patch
Patch1037:      0037-config-Nova-Lake-enabling.patch
Patch1038:      0038-lpmd_cpu-Add-wildcard-for-active_cpus-and-cpu-types.patch
Patch1039:      0039-data-Fix-active-cpu-spelling.patch
Patch1040:      0040-Enable-platform-agnostic-config-fallback-for-unknown.patch
Patch1041:      0041-docs-Clarify-slider-config.patch
Patch1042:      0042-Validate-slider-balance-and-offset-configuration.patch
Patch1043:      0043-lpmd_cpumask-Refactor-get_cgroup_systemd_vals-to-avo.patch
Patch1044:      0044-lpmd_cpu-Add-a-CPU-blacklist-cpumask.patch
Patch1045:      0045-lpmd_cpu-Skip-filling-out-type-cpumasks-if-there-was.patch
Patch1046:      0046-lpmd_cpumask-init-level-complex-isolation-fix-blackl.patch
Patch1047:      0047-lpmd_cpumask-Refresh-cached-data-when-blacklisting-c.patch
Patch1048:      0048-lpmd_cpumask-Refactor-getting-cached-values.patch
Patch1049:      0049-lpmd_proc-Export-the-state-name-when-an-empty-cpumas.patch
Patch1050:      0050-Use-return-value-of-lpmd_read_int.patch
Patch1051:      0051-all-Apply-kernel-formatting.patch
Patch1052:      0052-Add-a-simple-Makefile-to-use-without-autotools.patch
Patch1053:      0053-Minor-printf-formatting-fixes.patch
Patch1054:      0054-lpmd_config-Fix-compilation-warning-on-buffer-size.patch
Patch1055:      0055-Fix-cpumask_exclude_copy-destination-population.patch
Patch1056:      0056-When-GFX-trigger-is-enabled-don-t-disable-util-calcu.patch

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
# Nova lake config
install -D -p -m 644 data/intel_lpmd_config_F18_M1.xml %{buildroot}/%{_sysconfdir}/%{daemon_name}/intel_lpmd_config_F18_M1.xml

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
%config(noreplace) %{_sysconfdir}/%{daemon_name}/intel_lpmd_config_F6_M181.xml
%config(noreplace) %{_sysconfdir}/%{daemon_name}/intel_lpmd_config_F6_M204.xml
%config(noreplace) %{_sysconfdir}/%{daemon_name}/intel_lpmd_config_F18_M1.xml

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
