%define url_ver	%(echo %{version}|cut -d. -f1,2)
%define gstapi	1.0
%define api	3.8

Summary:	Integrated GNOME mail client, calendar and address book
Name:		evolution
Version:	3.8.3
Release:	1
License: 	LGPLv2+
Group:		Networking/Mail
Url: 		http://www.gnome.org/projects/evolution/
Source0: 	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	bogofilter
BuildRequires:	gtk-doc
BuildRequires:	highlight
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	desktop-file-utils
BuildRequires:	openldap-devel
BuildRequires:	pkgconfig(atk)
BuildRequires:	pkgconfig(libsecret-unstable)	
BuildRequires:	pkgconfig(cairo-gobject)
BuildRequires:	pkgconfig(camel-1.2) >= %{version}
BuildRequires:	pkgconfig(clutter-1.0) >= 1.0.0
BuildRequires:	pkgconfig(clutter-gtk-1.0) >= 0.90
BuildRequires:	pkgconfig(gail-3.0) >= 3.0.2
BuildRequires:	pkgconfig(gconf-2.0) >= 2.0.0
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gio-2.0) >= 2.30
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 2.91.3
BuildRequires:	pkgconfig(gnome-icon-theme) >= 2.30.2.1
BuildRequires:	pkgconfig(goa-1.0) >= 3.1.1
BuildRequires:	pkgconfig(gsettings-desktop-schemas) >= 2.91.92
BuildRequires:	pkgconfig(gstreamer-%{gstapi})
BuildRequires:	pkgconfig(gtkhtml-editor-4.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.2.0
BuildRequires:	pkgconfig(gweather-3.0) >= 2.90.0
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libcanberra-gtk3) >= 0.25
BuildRequires:	pkgconfig(libebackend-1.2) >= %{version}
BuildRequires:	pkgconfig(libebook-1.2) >= %{version}
BuildRequires:	pkgconfig(libecal-1.2) >= %{version}
BuildRequires:	pkgconfig(libedataserver-1.2) >= %{version}
BuildRequires:	pkgconfig(libgdata) >= 0.10.0
BuildRequires:	pkgconfig(libgtkhtml-4.0) >= 4.1.2
BuildRequires:	pkgconfig(libnotify) >= 0.5.1
BuildRequires:	pkgconfig(libpst)
BuildRequires:	pkgconfig(libsoup-gnome-2.4) >= 2.31.2
BuildRequires:	pkgconfig(libxml-2.0) >= 2.7.3
BuildRequires:	pkgconfig(libnm-glib)
BuildRequires:	pkgconfig(mx-1.0)
BuildRequires:	pkgconfig(nspr)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(shared-mime-info) >= 0.22
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(webkitgtk-3.0)

Requires:	bogofilter
# (fc) 0.8-5mdk implicit dependency is not enough
Requires:	evolution-data-server >= %{version}
Requires:	gtkhtml4 
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
%apply_patches

# Remove the welcome email from Novell
for inbox in mail/default/*/Inbox; do
	echo -n "" > $inbox
done

%build
%configure2_5x \
	--disable-static \
	--disable-spamassassin \
	--enable-plugins=all \
	--with-krb5=%{_prefix} \
	--with-krb5-libs=%{_libdir} \
	--with-openldap=yes \
	--with-static-ldap=no \
	--with-sub-version="-%{release}"

%make

%install
%makeinstall_std
#remove unpackaged files
rm -rf %{buildroot}/var/lib/
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

desktop-file-install --vendor="" \
	--remove-category="Office" \
	--remove-category="Calendar" \
	--remove-category="ContactManagement" \
	--add-category="Network" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/evolution.desktop

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

%find_lang %{name}-%{api} --with-gnome
%find_lang %{name} --with-gnome
cat %{name}.lang >> %{name}-%{api}.lang

%files -f %{name}-%{api}.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%{_sysconfdir}/xdg/autostart/*.desktop
%{_bindir}/*
%dir %{_libdir}/evolution
%dir %{_libdir}/evolution/%{api}
%dir %{_libdir}/evolution/%{api}/modules/
%dir %{_libdir}/evolution/%{api}/plugins
%{_libdir}/evolution/%{api}/*.so
%{_libdir}/evolution/%{api}/csv2vcard
%{_libdir}/evolution/%{api}/evolution-addressbook-export
%{_libdir}/evolution/%{api}/evolution-alarm-notify
%{_libdir}/evolution/%{api}/evolution-backup
%{_libdir}/evolution/%{api}/killev
%{_libdir}/evolution/%{api}/modules/*.so
%{_libdir}/evolution/%{api}/plugins/*.so
%{_libdir}/evolution/%{api}/plugins/*.eplug
%{_datadir}/applications/*
%{_datadir}/evolution
%{_datadir}/GConf/gsettings/evolution.convert
%{_datadir}/glib-2.0/schemas/*.xml
%{_iconsdir}/hicolor/*/apps/*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*
%doc %{_datadir}/gtk-doc/html/*

