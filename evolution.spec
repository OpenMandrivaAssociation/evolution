%define api 3.4
%define with_mono 1

%ifarch %arm %mips
%define with_mono 0
%endif

Summary:	Integrated GNOME mail client, calendar and address book
Name:		evolution
Version:	3.4.2
Release:	1
License: 	LGPLv2+
Group:		Networking/Mail
URL: 		http://www.gnome.org/projects/evolution/
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.xz
Patch0:		evolution-2.2.3-no-diagnostics.patch

BuildRequires: gtk-doc
BuildRequires: gnome-doc-utils
BuildRequires: intltool
BuildRequires: desktop-file-utils
BuildRequires: openldap-devel
BuildRequires: pkgconfig(atk)
BuildRequires: pkgconfig(cairo-gobject)
BuildRequires: pkgconfig(camel-1.2) >= %{version}
BuildRequires: pkgconfig(clutter-1.0) >= 1.0.0
BuildRequires: pkgconfig(clutter-gtk-1.0) >= 0.90
BuildRequires: pkgconfig(gail-3.0) >= 3.0.2
BuildRequires: pkgconfig(gconf-2.0) >= 2.0.0
BuildRequires: pkgconfig(gio-2.0) >= 2.30
BuildRequires: pkgconfig(gnome-desktop-3.0) >= 2.91.3
BuildRequires: pkgconfig(gnome-icon-theme) >= 2.30.2.1
BuildRequires: pkgconfig(goa-1.0) >= 3.1.1
BuildRequires: pkgconfig(gsettings-desktop-schemas) >= 2.91.92
BuildRequires: pkgconfig(gstreamer-0.10)
BuildRequires: pkgconfig(gtkhtml-editor-4.0)
BuildRequires: pkgconfig(gtk+-3.0) >= 3.2.0
BuildRequires: pkgconfig(gweather-3.0) >= 2.90.0
BuildRequires: pkgconfig(ice)
BuildRequires: pkgconfig(libcanberra-gtk3) >= 0.25
BuildRequires: pkgconfig(libebackend-1.2) >= %{version}
BuildRequires: pkgconfig(libebook-1.2) >= %{version}
BuildRequires: pkgconfig(libecal-1.2) >= %{version}
BuildRequires: pkgconfig(libedataserver-1.2) >= %{version}
BuildRequires: pkgconfig(libedataserverui-3.0) >= %{version}
BuildRequires: pkgconfig(libgdata) >= 0.10.0
BuildRequires: pkgconfig(libgtkhtml-4.0) >= 4.1.2
BuildRequires: pkgconfig(libnotify) >= 0.5.1
BuildRequires: pkgconfig(libpst)
BuildRequires: pkgconfig(libsoup-gnome-2.4) >= 2.31.2
BuildRequires: pkgconfig(libxml-2.0) >= 2.7.3
BuildRequires: pkgconfig(libnm-glib)
BuildRequires: pkgconfig(mx-1.0)
BuildRequires: pkgconfig(nspr)
BuildRequires: pkgconfig(nss)
BuildRequires: pkgconfig(shared-mime-info) >= 0.22
BuildRequires: pkgconfig(sm)

# (fc) 0.8-5mdk implicit dependency is not enough
Requires: evolution-data-server >= %{version}
Requires: gtkhtml4 
Requires: gnupg
Requires: gtk+3.0
Suggests: gstreamer0.10-plugins-good
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
Obsoletes:	%{_lib}evolution3.2-devel

%description devel
This package contains the files necessary to develop applications
using Evolution's libraries.

%if %{with_mono}
%package mono
Summary: Mono plugin loader for Evolution
Group: Communications
BuildRequires: mono-devel
Requires: %{name} = %{version}
Requires: mono

%description mono
Evolution is the GNOME mailer, calendar, contact manager and
communications tool.  The tools which make up Evolution will
be tightly integrated with one another and act as a seamless
personal information-management tool.

This is the Mono plugin loader that adds support for plugins developed 
with mono.
%endif

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
	--enable-plugins=experimental \
	--with-krb5=%{_prefix} \
	--with-krb5-libs=%{_libdir} \
	--with-openldap=yes \
	--with-static-ldap=no \
	--with-sub-version="-%{release}"  \
%if %{with_mono}
	--enable-mono=yes
%endif

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
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/evolution.desktop

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

%define schemas apps_evolution_eplugin_face apps-evolution-external-editor apps_evolution_email_custom_header apps-evolution-mail-notification apps-evolution-mail-prompts-checkdefault apps_evolution_addressbook apps_evolution_calendar apps_evolution_shell evolution-mail apps-evolution-attachment-reminder apps-evolution-template-placeholders evolution-bogofilter.schemas evolution-spamassassin.schemas

%preun
%preun_uninstall_gconf_schemas %{schemas}

%files -f %{name}-%{api}.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%{_sysconfdir}/xdg/autostart/*.desktop
%{_sysconfdir}/gconf/schemas/apps-evolution-external-editor.schemas
%{_sysconfdir}/gconf/schemas/apps_evolution_email_custom_header.schemas
%{_sysconfdir}/gconf/schemas/apps-evolution-mail-notification.schemas
%{_sysconfdir}/gconf/schemas/apps-evolution-mail-prompts-checkdefault.schemas
%{_sysconfdir}/gconf/schemas/apps-evolution-template-placeholders.schemas
%{_sysconfdir}/gconf/schemas/apps_evolution_addressbook.schemas
%{_sysconfdir}/gconf/schemas/apps_evolution_eplugin_face.schemas
%{_sysconfdir}/gconf/schemas/apps-evolution-attachment-reminder.schemas
%{_sysconfdir}/gconf/schemas/apps_evolution_calendar.schemas
%{_sysconfdir}/gconf/schemas/apps_evolution_shell.schemas
%{_sysconfdir}/gconf/schemas/evolution-mail.schemas
%{_sysconfdir}/gconf/schemas/evolution-bogofilter.schemas
%{_sysconfdir}/gconf/schemas/evolution-spamassassin.schemas
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
%{_libdir}/evolution/%{api}/modules/libevolution-module-*.so
%{_libdir}/evolution/%{api}/plugins/liborg-gnome-*.so
%{_libdir}/evolution/%{api}/plugins/org-gnome*.eplug
%if %{with_mono}
%exclude %{_libdir}/evolution/%{api}/modules/*mono*
%endif
%{_datadir}/applications/*
%{_datadir}/evolution
%{_datadir}/GConf/gsettings/evolution.convert
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/icons/hicolor/*/apps/*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*
%doc %{_datadir}/gtk-doc/html/*

%if %{with_mono}
%files mono
%{_libdir}/evolution/%{api}/modules/*mono*
%endif

