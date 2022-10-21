%define url_ver	%(echo %{version}|cut -d. -f1,2)
%define gstapi	1.0
%define api	3.30

%define _disable_rebuild_configure 1

%define _cmake_skip_rpath %nil

Summary:	Integrated GNOME mail client, calendar and address book
Name:		evolution
Version:	3.46.1
Release:	1
License: 	LGPLv2+
Group:		Networking/Mail
Url: 		http://www.gnome.org/projects/evolution/
Source0: 	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
Patch0:		0001-I-2037-EHeaderBarButton-Avoid-busy-loop-on-toggle-ac.patch
BuildRequires:	cmake
BuildRequires:	bogofilter
BuildRequires:	gtk-doc
BuildRequires:	highlight
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	desktop-file-utils
BuildRequires:	openldap-devel
BuildRequires:	pkgconfig(atk)
BuildRequires:	pkgconfig(libcmark)
BuildRequires:	pkgconfig(libsecret-unstable)
BuildRequires:	pkgconfig(cairo-gobject)
BuildRequires:	pkgconfig(camel-1.2) >= %{version}
BuildRequires:	pkgconfig(champlain-0.12)
BuildRequires:	pkgconfig(clutter-1.0) >= 1.0.0
BuildRequires:	pkgconfig(clutter-gtk-1.0) >= 0.90
BuildRequires:	pkgconfig(cryptui-0.0)
BuildRequires:	pkgconfig(gail-3.0) >= 3.0.2
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gio-2.0) >= 2.30
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 2.91.3
BuildRequires:	pkgconfig(goa-1.0) >= 3.1.1
BuildRequires:	pkgconfig(gsettings-desktop-schemas) >= 2.91.92
BuildRequires:	pkgconfig(gstreamer-%{gstapi})
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.2.0
BuildRequires:	pkgconfig(gweather4)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libcanberra-gtk3) >= 0.25
BuildRequires:	pkgconfig(libebackend-1.2) >= %{version}
BuildRequires:	pkgconfig(libebook-1.2) >= %{version}
BuildRequires:	pkgconfig(libecal-2.0) >= %{version}
BuildRequires:	pkgconfig(libedataserver-1.2) >= %{version}
BuildRequires:	pkgconfig(libgdata) >= 0.10.0
BuildRequires:	pkgconfig(libnotify) >= 0.5.1
BuildRequires:	pkgconfig(libpst)
BuildRequires:	pkgconfig(libsoup-3.0) 
BuildRequires:	pkgconfig(libxml-2.0) >= 2.7.3
BuildRequires:	pkgconfig(nspr)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(shared-mime-info) >= 0.22
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(webkit2gtk-4.1)
BuildRequires:	pkgconfig(gtkspell3-3.0)
BuildRequires:	pkgconfig(gnome-autoar-gtk-0)
BuildRequires:	pkgconfig(gnome-autoar-0)
BuildRequires:	pkgconfig(gspell-1)

BuildRequires: locales-extra-charsets

Requires:	bogofilter
# (fc) 0.8-5mdk implicit dependency is not enough
Requires:	evolution-data-server >= %{version}
Requires:	gnupg
Requires:	gtk+3.0
Requires:	highlight
Suggests:	gstreamer%{gstapi}-plugins-good
# the old shared lib pkg should be obsoleted after everything is rebuilt

%description
Evolution is the GNOME mailer, calendar, contact manager and
communications tool.  The tools which make up Evolution will
be tightly integrated with one another and act as a seamless
personal information-management tool.

%package devel
Summary:	Libraries and include files for developing Evolution components
Group:		Development/GNOME and GTK+
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the files necessary to develop applications
using Evolution's libraries.

%prep
%setup -q
%autopatch -p1

# Remove the welcome email from Novell
for inbox in src/mail/default/*/Inbox; do
	echo -n "" > $inbox
done

%build
%cmake \
	-DENABLE_MAINTAINER_MODE=OFF \
	-DVERSION_SUBSTRING=" (%{version}-%{release})" \
	-DENABLE_PLUGINS=all \
	-DENABLE_YTNEF=OFF \
	-DENABLE_INSTALLED_TESTS=OFF \
        -DWITH_OPENLDAP=ON \
        -DENABLE_SMIME=ON \
        -DENABLE_GTK_DOC=OFF \
        -DWITH_HELP=ON \
        -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
        -DLIB_INSTALL_DIR:PATH=%{_libdir} \
	-DWITH_GWEATHER4=ON

%make_build

%install
%make_install -C build
#remove unpackaged files
rm -rf %{buildroot}/var/lib/
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

desktop-file-install --vendor="" \
	--remove-category="Office" \
	--remove-category="Calendar" \
	--remove-category="ContactManagement" \
	--add-category="Network" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/org.gnome.Evolution.desktop

mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart/
cat << EOF > %{buildroot}%{_sysconfdir}/xdg/autostart/evolution-alarm-notify.desktop
[Desktop Entry]
Encoding=UTF-8
Name=Evolution Alarm Notifier
Comment=Evolution Alarm Notifier
Icon=stock_alarm
Exec=%{_libdir}/evolution/%{api}/evolution-alarm-notify
Terminal=false
Type=Application
OnlyShowIn=GNOME;
Categories=TrayIcon;
EOF

# do not package obsolete mime-info files, evolution doesn't import them on commandline (Mdv bug #53984)
rm -fr %{buildroot}/%{_datadir}/mime-info

%find_lang %{name} --with-gnome
cat %{name}.lang >> %{name}-%{api}.lang

%files -f %{name}-%{api}.lang
%doc AUTHORS COPYING ChangeLog NEWS README.md
%{_sysconfdir}/xdg/autostart/*.desktop
%{_bindir}/*
%dir %{_libdir}/evolution
%dir %{_libdir}/evolution/modules/
%dir %{_libdir}/evolution/plugins
%{_libdir}/evolution/web-extensions
%{_libdir}/evolution/*.so
%{_libdir}/evolution-data-server/camel-providers/libcamelrss*
#{_libexecdir}/evolution/evolution-alarm-notify
%{_libexecdir}/evolution/evolution-backup
%{_libexecdir}/evolution/killev
%{_libdir}/evolution/modules/*.so
%{_libdir}/evolution/plugins/*.so
%{_libdir}/evolution/plugins/*.eplug
%{_libdir}/evolution-data-server/ui-modules/module-evolution-alarm-notify.so
%{_datadir}/applications/*
%{_datadir}/evolution
%{_datadir}/GConf/gsettings/evolution.convert
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/metainfo/org.gnome.Evolution.appdata.xml
%{_datadir}/metainfo/org.gnome.Evolution-bogofilter.metainfo.xml
%{_datadir}/metainfo/org.gnome.Evolution-spamassassin.metainfo.xml
%{_datadir}/metainfo/org.gnome.Evolution-pst.metainfo.xml
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/evolution.1.*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*
#doc #{_datadir}/gtk-doc/html/*

