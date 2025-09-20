Name:           kernel-zen
Version:        6.16.8
Release:        1%{?dist}
Summary:        Zen Linux Kernel - low-latency & performance patches
Packager:       Zaman Hüseynli <admin@azccriminal.space>

License:        GPL-2.0
URL:            https://github.com/zen-kernel/zen-kernel
Source0:        linux-zen-%{version}.tar.gz
Patch0:         linux-v%{version}-zen1.patch.zst
BuildRequires:  gcc make bc bison flex elfutils-libelf-devel ncurses-devel openssl-devel zlib-devel zstd
Requires:       dracut

%description
Zen Linux Kernel with low-latency, MUQSS scheduler, and desktop performance improvements.

%prep
%setup -q -n linux-zen-%{version} -T
tar -xzf %{SOURCE0} -C .

# Apply zst patch
zstd -d %{PATCH0} -c | patch -p1

%build
make olddefconfig
make -j$(nproc)

%install
rm -rf $RPM_BUILD_ROOT
make INSTALL_MOD_PATH=$RPM_BUILD_ROOT modules_install
make INSTALL_MOD_PATH=$RPM_BUILD_ROOT install

# Generate initramfs
%post
/sbin/dracut --kver %{version} --force

%files
/boot/*
/lib/modules/%{version}*/

%changelog
* Sat Sep 21 2025 Zaman Hüseynli <admin@azccriminal.space> - 6.16.8-1
- Initial Zen kernel build with .zst patch
