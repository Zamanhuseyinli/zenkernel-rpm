Name:           kernel-zen
Version:        6.16.8
Release:        1%{?dist}
Summary:        Zen Linux Kernel - low-latency & performance patches
License:        GPL-2.0
URL:            https://github.com/zen-kernel/zen-kernel
Source0:        linux-zen-%{version}.tar.gz


%description
Zen Linux Kernel with low-latency, MUQSS scheduler, and desktop performance improvements.

%prep
# Manuel tar.gz açma, %setup kullanma
rm -rf %{_builddir}/kernel-zen-%{version}
mkdir -p %{_builddir}/kernel-zen-%{version}
tar -xzf %{SOURCE0} -C %{_builddir}/kernel-zen-%{version} --strip-components=1

%build
cd %{_builddir}/kernel-zen-%{version}
make olddefconfig
make -j$(nproc)

%install
cd %{_builddir}/kernel-zen-%{version}
rm -rf %{buildroot}
make INSTALL_MOD_PATH=%{buildroot} modules_install
make INSTALL_MOD_PATH=%{buildroot} install

%post
/sbin/dracut --kver $(uname -r) --force

%preun
if [ $1 -eq 0 ]; then
    rm -f /boot/vmlinuz-%{version}*
    rm -f /boot/initramfs-%{version}*.img
    rm -f /boot/System.map-%{version}*
    rm -f /boot/config-%{version}*
    rm -rf /lib/modules/%{version}*
fi

%files
%defattr(-,root,root)
/boot/vmlinuz-%{version}*
/boot/initramfs-%{version}*.img
/boot/System.map-%{version}*
/boot/config-%{version}*
/lib/modules/%{version}*/

%changelog
* Sat Sep 20 2025 Zaman Hüseynli <admin@azccriminal.space> - 6.16.8-1
- Initial Zen kernel build (patch removed for GitHub CI/CD Releases)
- Cleanup added in %preun
