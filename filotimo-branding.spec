Name:           filotimo-branding
Version:        1.5
Release:        5%{?dist}
Summary:        Logos and branding for Filotimo Linux

License:        GPL-2.0
URL:            https://github.com/filotimo-project/branding
Source:         %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  inkscape
BuildRequires:  python3-scour
BuildRequires:  netpbm-progs
BuildRequires:  libicns-utils
BuildRequires:  zopfli
BuildRequires:  hardlink
BuildRequires:  kde4-macros(api)

Conflicts:      fedora-logos < 38.1.0-100%{?dist}.filotimo
Obsoletes:      fedora-logos < 38.1.0-100%{?dist}.filotimo

%description
Logos and branding for Filotimo.

%define debug_package %{nil}

%prep
%setup -q

%build

%install
install -pm 0644 %{SOURCE0} LICENSE

# Bartholemule
mkdir -p %{buildroot}%{_datadir}

# Build icons
mkdir -p build/pixmaps
mkdir -p build/bootloader
mkdir -p build/hicolor

# Plymouth watermark and gdm logo
inkscape -h 64 src/banners/banner-darkbackground.svg -o build/watermark.png

# SVG Fedora logos
inkscape -h 80 src/banners/banner-darkbackground.svg -o build/fedora_darkbackground.svg
inkscape -h 80 src/banners/banner-lightbackground.svg -o build/fedora_lightbackground.svg
inkscape -h 415 src/banners/banner-darkbackground.svg -o build/fedora_logo_darkbackground.svg
inkscape -h 415 src/banners/banner-lightbackground.svg -o build/fedora_logo.svg

# /usr/share/pixmaps
inkscape -h 252 -w 252 src/icons/icon-colorful.svg -o build/pixmaps/fedora-logo-sprite.png
inkscape -h 252 -w 252 src/icons/icon-colorful.svg -o build/pixmaps/fedora-logo-sprite.svg

inkscape -h 164 src/banners/banner-darkbackground.svg -o build/pixmaps/fedora-logo.png
inkscape -h 47 src/banners/banner-darkbackground.svg -o build/pixmaps/fedora-logo-small.png
inkscape -h 80 src/banners/banner-darkbackground.svg -o build/pixmaps/fedora-logo-med.png

# /usr/share/pixmaps/bootloader
inkscape -h 128 -w 128 src/icons/icon-colorful.svg -o build/bootloader/bootlogo_128.png
inkscape -h 256 -w 256 src/icons/icon-colorful.svg -o build/bootloader/bootlogo_256.png
zopflipng -ym build/bootloader/bootlogo_128.png build/bootloader/bootlogo_128.png
zopflipng -ym build/bootloader/bootlogo_256.png build/bootloader/bootlogo_256.png
png2icns build/bootloader/fedora.icns build/bootloader/bootlogo_128.png
inkscape -h 12 -w 12 src/icons/icon-colorful.svg -o build/bootloader/apple.png
pngtopnm build/bootloader/apple.png | ppmtoapplevol > build/bootloader/fedora.vol
pngtopnm build/bootloader/apple.png | ppmtoapplevol > build/bootloader/fedora_media.vol

# /usr/share/icons/hicolor
for size in 16x16 22x22 24x24 32x32 36x36 48x48 96x96 256x256 ; do
    mkdir -p build/hicolor/$size
    inkscape -h $(echo $size | cut -d 'x' -f 1 ) -w $(echo $size | cut -d 'x' -f 1 ) src/icons/icon-colorful.svg -o build/hicolor/$size/fedora-logo-icon.png
done
inkscape -h 128 -w 128 src/icons/icon-colorful.svg -o build/hicolor/scalable/fedora-logo-icon.svg
inkscape -h 128 -w 128 src/icons/icon-symbolic.svg -o build/hicolor/scalable/fedora-logo-icon-symbolic.svg

# Optimise SVGS
find ./build/ -type f -name "*.svg" -exec sh -c 'scour -i "$0" -o "$0"' {} \;

# Install icons

# Plymouth watermark and gdm logo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/spinner
mkdir -p $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/filotimo
install -p -m 644 build/watermark.png $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/spinner/watermark.png
install -p -m 644 build/watermark.png $RPM_BUILD_ROOT%{_datadir}/plymouth/themes/filotimo/watermark.png

# /usr/share/pixmaps/bootloader
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps/bootloader
install -p -m 644 build/bootloader/fedora.icns $RPM_BUILD_ROOT%{_datadir}/pixmaps/bootloader
install -p -m 644 build/bootloader/fedora.vol build/bootloader/fedora_media.vol $RPM_BUILD_ROOT%{_datadir}/pixmaps/bootloader

# SVG Filotimo logos
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fedora-logos
cp -a build/fedora_*.svg $RPM_BUILD_ROOT%{_datadir}/fedora-logos

# /usr/share/pixmaps
for i in build/pixmaps/* ; do
  install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/pixmaps
done
install -p -m 644 build/pixmaps/fedora-logo-sprite.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/system-logo-white.png

# /usr/share/icons/hicolor and Bluecurve
for size in 16x16 22x22 24x24 32x32 36x36 48x48 96x96 256x256 ; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$size/apps
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve/$size/apps
  pushd $RPM_BUILD_ROOT%{_datadir}/icons/Bluecurve/$size/apps
    ln -s ../../../hicolor/$size/apps/fedora-logo-icon.png icon-panel-menu.png
    ln -s ../../../hicolor/$size/apps/fedora-logo-icon.png gnome-main-menu.png
    ln -s ../../../hicolor/$size/apps/fedora-logo-icon.png kmenu.png
    ln -s ../../../hicolor/$size/apps/fedora-logo-icon.png start-here.png
  popd
  for i in build/hicolor/$size/* ; do
    install -p -m 644 $i $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$size/apps
  done
done

for i in 16 22 24 32 36 48 96 256 ; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/places
  install -p -m 644 -D $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/apps/fedora-logo-icon.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/places/start-here.png
  install -p -m 644 -D $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/apps/fedora-logo-icon.png $RPM_BUILD_ROOT%{_kde4_iconsdir}/oxygen/${i}x${i}/places/start-here-kde-fedora.png
done

# favicon
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
pushd $RPM_BUILD_ROOT%{_sysconfdir}
  ln -s %{_datadir}/icons/hicolor/16x16/apps/fedora-logo-icon.png favicon.png
popd

# Fedora hicolor icons
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps
install -p -m 644 build/hicolor/scalable/fedora-logo-icon.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/fedora-logo-icon.svg
install -p -m 644 build/hicolor/scalable/fedora-logo-icon-symbolic.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/fedora-logo-icon-symbolic.svg
install -p -m 644 build/hicolor/scalable/fedora-logo-icon.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/start-here.svg
install -p -m 644 build/hicolor/scalable/fedora-logo-icon-symbolic.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/start-here-symbolic.svg
install -p -m 644 build/hicolor/scalable/fedora-logo-icon-symbolic.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/start-here-kde-fedora-symbolic.svg
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/places/
pushd $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/places/
  ln -s ../apps/start-here.svg .
  ln -s ../apps/start-here-symbolic.svg .
popd

# Anaconda
# https://pagure.io/fedora-logos/blob/master/f/anaconda
# https://src.fedoraproject.org/rpms/fedora-logos/blob/rawhide/f/fedora-logos.spec
mkdir -p %{buildroot}%{_datadir}/anaconda/boot
install -p -m 644 anaconda/splash.lss %{buildroot}%{_datadir}/anaconda/boot/
install -p -m 644 anaconda/syslinux-splash.png %{buildroot}%{_datadir}/anaconda/boot/
install -p -m 644 anaconda/syslinux-vesa-splash.png %{buildroot}%{_datadir}/anaconda/boot/splash.png

mkdir -p %{buildroot}%{_datadir}/anaconda/pixmaps
install -p -m 644 anaconda/anaconda_header.png %{buildroot}%{_datadir}/anaconda/pixmaps/
install -p -m 644 anaconda/sidebar-logo.png %{buildroot}%{_datadir}/anaconda/pixmaps/
install -p -m 644 anaconda/sidebar-bg.png %{buildroot}%{_datadir}/anaconda/pixmaps/
install -p -m 644 anaconda/topbar-bg.png %{buildroot}%{_datadir}/anaconda/pixmaps/
install -p -m 644 anaconda/fedora.css %{buildroot}%{_datadir}/anaconda/pixmaps/


hardlink -vv %{buildroot}/usr

%files
%license LICENSE
%config(noreplace) %{_sysconfdir}/favicon.png
%{_datadir}/plymouth/themes/spinner/watermark.png
%{_datadir}/plymouth/themes/filotimo/watermark.png
%{_kde4_iconsdir}/oxygen/
%{_datadir}/pixmaps/*
%{_datadir}/anaconda/pixmaps/*
%{_datadir}/anaconda/boot/splash.lss
%{_datadir}/anaconda/boot/syslinux-splash.png
%{_datadir}/anaconda/boot/splash.png
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/places/*
%{_datadir}/icons/Bluecurve/*/apps/*
%{_datadir}/fedora-logos/
%dir %{_datadir}/icons/Bluecurve/
%dir %{_datadir}/icons/Bluecurve/16x16/
%dir %{_datadir}/icons/Bluecurve/16x16/apps/
%dir %{_datadir}/icons/Bluecurve/22x22/
%dir %{_datadir}/icons/Bluecurve/22x22/apps/
%dir %{_datadir}/icons/Bluecurve/24x24/
%dir %{_datadir}/icons/Bluecurve/24x24/apps/
%dir %{_datadir}/icons/Bluecurve/32x32/
%dir %{_datadir}/icons/Bluecurve/32x32/apps/
%dir %{_datadir}/icons/Bluecurve/36x36/
%dir %{_datadir}/icons/Bluecurve/36x36/apps/
%dir %{_datadir}/icons/Bluecurve/48x48/
%dir %{_datadir}/icons/Bluecurve/48x48/apps/
%dir %{_datadir}/icons/Bluecurve/96x96/
%dir %{_datadir}/icons/Bluecurve/96x96/apps/
%dir %{_datadir}/icons/Bluecurve/256x256/
%dir %{_datadir}/icons/Bluecurve/256x256/apps/
%dir %{_datadir}/icons/hicolor/
%dir %{_datadir}/icons/hicolor/16x16/
%dir %{_datadir}/icons/hicolor/16x16/apps/
%dir %{_datadir}/icons/hicolor/16x16/places/
%dir %{_datadir}/icons/hicolor/22x22/
%dir %{_datadir}/icons/hicolor/22x22/apps/
%dir %{_datadir}/icons/hicolor/22x22/places/
%dir %{_datadir}/icons/hicolor/24x24/
%dir %{_datadir}/icons/hicolor/24x24/apps/
%dir %{_datadir}/icons/hicolor/24x24/places/
%dir %{_datadir}/icons/hicolor/32x32/
%dir %{_datadir}/icons/hicolor/32x32/apps/
%dir %{_datadir}/icons/hicolor/32x32/places/
%dir %{_datadir}/icons/hicolor/36x36/
%dir %{_datadir}/icons/hicolor/36x36/apps/
%dir %{_datadir}/icons/hicolor/36x36/places/
%dir %{_datadir}/icons/hicolor/48x48/
%dir %{_datadir}/icons/hicolor/48x48/apps/
%dir %{_datadir}/icons/hicolor/48x48/places/
%dir %{_datadir}/icons/hicolor/96x96/
%dir %{_datadir}/icons/hicolor/96x96/apps/
%dir %{_datadir}/icons/hicolor/96x96/places/
%dir %{_datadir}/icons/hicolor/256x256/
%dir %{_datadir}/icons/hicolor/256x256/apps/
%dir %{_datadir}/icons/hicolor/256x256/places/
%dir %{_datadir}/icons/hicolor/scalable/
%dir %{_datadir}/icons/hicolor/scalable/apps/
%dir %{_datadir}/icons/hicolor/scalable/places/
%dir %{_datadir}/anaconda
%dir %{_datadir}/anaconda/boot/
%dir %{_datadir}/anaconda/pixmaps/
%dir %{_datadir}/plymouth/

%changelog
* Sun Feb 09 2025 Thomas Duckworth <tduck973564@gmail.com> 1.5-5
- fix it (tduck973564@gmail.com)
- fix it (tduck973564@gmail.com)

* Sun Feb 09 2025 Thomas Duckworth <tduck973564@gmail.com>
- fix it (tduck973564@gmail.com)

<<<<<<< Updated upstream
=======
* Sun Feb 09 2025 Thomas Duckworth <tduck973564@gmail.com>
- 

* Sun Feb 09 2025 Thomas Duckworth <tduck973564@gmail.com> 1.5-5
- 

>>>>>>> Stashed changes
* Sun Feb 09 2025 Thomas Duckworth <tduck973564@gmail.com> 1.5-4
- 

* Sun Feb 09 2025 Thomas Duckworth <tduck973564@gmail.com> 1.5-3
- Dependency stuff

* Sun Feb 09 2025 Thomas Duckworth <tduck973564@gmail.com> 1.5-2
- 

* Sat Feb 08 2025 Thomas Duckworth <tduck973564@gmail.com> 1.5-1
- anaconda logos (tduck973564@gmail.com)

* Thu Dec 12 2024 Thomas Duckworth <tduck973564@gmail.com> 1.4-1
- new package built with tito

* Thu Jul 11 2024 Thomas Duckworth <tduck973564@gmail.com> 0.14-1
- OBS releaser for Tito

* Wed Jul 03 2024 Thomas Duckworth <tduck973564@gmail.com> 0.13-1
- Swap darkbackground and lightbackground icons (tduck973564@gmail.com)

* Tue Jun 25 2024 Thomas Duckworth <tduck973564@gmail.com> 0.12-1
- Shrink watermark and remove sddm logo - ugly (tduck973564@gmail.com)

* Sun Jun 23 2024 Thomas Duckworth <tduck973564@gmail.com> 0.11-1
- Sddm logo (tduck973564@gmail.com)

* Sun Jun 23 2024 Thomas Duckworth <tduck973564@gmail.com> 0.10-1
- Fix symbolic icon (tduck973564@gmail.com)

* Sun Jun 23 2024 Thomas Duckworth <tduck973564@gmail.com> 0.9-1
- Update icons to look nicer (tduck973564@gmail.com)

* Sun Jun 23 2024 Thomas Duckworth <tduck973564@gmail.com> 0.8-1
- Add symbolic icons (tduck973564@gmail.com)

* Sat Jun 22 2024 Thomas Duckworth <tduck973564@gmail.com> 0.7-1
- Add svg optimisations (tduck973564@gmail.com)

* Sat Jun 22 2024 Thomas Duckworth <tduck973564@gmail.com> 0.6-1
- Add scalable fedora-logo-icon (tduck973564@gmail.com)

* Sat Jun 22 2024 Thomas Duckworth <tduck973564@gmail.com> 0.5-1
- Fix provides (tduck973564@gmail.com)

* Sat Jun 22 2024 Thomas Duckworth <tduck973564@gmail.com> 0.4-1
- Replace Conflicts with Obsoletes (tduck973564@gmail.com)

* Sat Jun 22 2024 Thomas Duckworth <tduck973564@gmail.com> 0.3-1
- Simplify logos (tduck973564@gmail.com)

* Sat Jun 22 2024 Thomas Duckworth <tduck973564@gmail.com> 0.2-1
- Fix buildrequires (tduck973564@gmail.com)
- Remove duplicate changelog entry (tduck973564@gmail.com)

* Sat Jun 22 2024 Thomas Duckworth <tduck973564@gmail.com> 0.1-1
- new package built with tito
