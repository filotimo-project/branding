Name:           filotimo-branding
Version:        0.7
Release:        1%{?dist}
Summary:        Logos and branding for Filotimo Linux

License:        GPL-2.0
URL:            https://github.com/filotimo-linux/branding
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  inkscape
BuildRequires:  python3-scour
BuildRequires:  netpbm-progs
BuildRequires:  libicns-utils
BuildRequires:  zopfli
BuildRequires:  hardlink
BuildRequires:	kde4-macros(api)

Provides:       fedora-logos
Obsoletes:      fedora-logos

Provides:       redhat-logos
Provides:       gnome-logos
Provides:       system-logos

%description
Logos and branding for Filotimo Linux.

%define debug_package %{nil}

%prep
%setup -q

%build

%install
install -pm 0644 %{SOURCE0} LICENSE

# Build icons
mkdir -p build/pixmaps
mkdir -p build/bootloader
mkdir -p build/hicolor

# Plymouth watermark and gdm logo
inkscape -h 80 src/logos/banner-darkbackground.svg -o build/watermark.png

# SVG Fedora logos
inkscape -h 80 src/logos/banner-darkbackground.svg -o build/fedora_darkbackground.svg
inkscape -h 80 src/logos/banner-lightbackground.svg -o build/fedora_lightbackground.svg
inkscape -h 415 src/logos/banner-darkbackground.svg -o build/fedora_logo_darkbackground.svg
inkscape -h 415 src/logos/banner-lightbackground.svg -o build/fedora_logo.svg

# /usr/share/pixmaps
inkscape -h 252 -w 252 src/icons/icon-darkbackground.svg -o build/pixmaps/fedora-logo-sprite.png
inkscape -h 252 -w 252 src/icons/icon-darkbackground.svg -o build/pixmaps/fedora-logo-sprite.svg

inkscape -h 164 src/logos/banner-darkbackground.svg -o build/pixmaps/fedora-logo.png
inkscape -h 47 src/logos/banner-darkbackground.svg -o build/pixmaps/fedora-logo-small.png
inkscape -h 80 src/logos/banner-darkbackground.svg -o build/pixmaps/fedora-logo-med.png

# /usr/share/pixmaps/bootloader
inkscape -h 128 -w 128 src/icons/icon-darkbackground.svg -o build/bootloader/bootlogo_128.png
inkscape -h 256 -w 256 src/icons/icon-darkbackground.svg -o build/bootloader/bootlogo_256.png
zopflipng -ym build/bootloader/bootlogo_128.png build/bootloader/bootlogo_128.png
zopflipng -ym build/bootloader/bootlogo_256.png build/bootloader/bootlogo_256.png
png2icns build/bootloader/fedora.icns build/bootloader/bootlogo_128.png
inkscape -h 12 -w 12 src/icons/icon-darkbackground.svg -o build/bootloader/apple.png
pngtopnm build/bootloader/apple.png | ppmtoapplevol > build/bootloader/fedora.vol
pngtopnm build/bootloader/apple.png | ppmtoapplevol > build/bootloader/fedora_media.vol

# /usr/share/icons/hicolor
for size in 16x16 22x22 24x24 32x32 36x36 48x48 96x96 256x256 ; do
    mkdir -p build/hicolor/$size
    inkscape -h $(echo $size | cut -d 'x' -f 1 ) -w $(echo $size | cut -d 'x' -f 1 ) src/icons/icon-darkbackground.svg -o build/hicolor/$size/fedora-logo-icon.png
done
inkscape -h 128 -w 128 src/icons/icon-darkbackground.svg -o build/hicolor/scalable/fedora-logo-icon.svg

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
install -p -m 644 build/hicolor/scalable/fedora-logo-icon.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/start-here.svg
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/places/
pushd $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/places/
  ln -s ../apps/start-here.svg .
popd

hardlink -vv %{buildroot}/usr

%files
%license LICENSE
%config(noreplace) %{_sysconfdir}/favicon.png
%{_datadir}/plymouth/themes/spinner/watermark.png
%{_datadir}/plymouth/themes/filotimo/watermark.png
%{_kde4_iconsdir}/oxygen/
%{_datadir}/pixmaps/*
# Anaconda icons don't exist, we will use Calamares
# %{_datadir}/anaconda/pixmaps/*
# %{_datadir}/anaconda/boot/splash.lss
# %{_datadir}/anaconda/boot/syslinux-splash.png
# %{_datadir}/anaconda/boot/splash.png
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
# %dir %{_datadir}/anaconda
# %dir %{_datadir}/anaconda/boot/
# %dir %{_datadir}/anaconda/pixmaps/
%dir %{_datadir}/plymouth/

%changelog
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
