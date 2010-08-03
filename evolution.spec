%define major_version 2.32
%define gtkhtml_version_required 3.31.2
%define libsoup_version_required 2.4.0
%define eds_version_required %{version}
%define with_mono 1
%{?_without_mono:	%{expand: %%global with_mono 0}}
%{?_with_mono:	%{expand: %%global with_mono 1}}

%ifarch %arm %mips
%define with_mono 0
%endif

Name:		evolution
Summary:	Integrated GNOME mail client, calendar and address book
Version:	2.31.6
Release:	%mkrel 1
License: 	LGPLv2+
Group:		Networking/Mail
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Source2:	evolution_48.png
Source3:	evolution_32.png
Source4:	evolution_16.png
Patch:		evolution-2.2.3-no-diagnostics.patch
# (fc) 1.5.94.1-4mdk import welcome mail from indexhtml
Patch17:	evolution-2.27.3-firstmail.patch
# (fc) 2.22.0-4mdv set back spamassassin as default spam software (typo in gconf key from upstream)
Patch24:	evolution-2.22.0-spamassassin.patch

URL: 		http://www.gnome.org/projects/evolution/
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

# (fc) 0.8-5mdk implicit dependency is not enough
Requires: evolution-data-server >= %{eds_version_required}
Requires: gtkhtml-3.14 >= %{gtkhtml_version_required}
Requires: gnupg
Requires: scrollkeeper >= 0.3
Requires: gtk+2.0 >= 2.4.0
Requires: indexhtml >= 10.1
Suggests: gstreamer0.10-plugins-good
Suggests: spamassassin
BuildRequires: bison flex
BuildRequires: dbus-glib-devel
BuildRequires: evolution-data-server-devel >= %{eds_version_required}
BuildRequires: gtk+2-devel >= 2.4.0
BuildRequires: gtkimageview-devel
BuildRequires: gtk-doc
BuildRequires: intltool
BuildRequires: krb5-devel 
BuildRequires: libgnomeui2-devel
BuildRequires: gstreamer0.10-devel
BuildRequires: gtkhtml-3.14-devel >= %{gtkhtml_version_required}
BuildRequires: libsoup-devel >= %{libsoup_version_required}
BuildRequires: nss-devel 
BuildRequires: libgdata-devel >= 0.4.0
BuildRequires: openldap-devel 
BuildRequires: libnotify-devel >= 0.3.0
BuildRequires: libgweather-devel
BuildRequires: libgnome-desktop-2-devel >= 2.26.0
BuildRequires: libcanberra-devel
BuildRequires: unique-devel < 2
BuildRequires: libchamplain-devel
BuildRequires: libgeoclue-devel
#gw needed by the tnef plugin
BuildRequires: libytnef-devel
BuildRequires: gnome-icon-theme
BuildRequires: gnome-doc-utils
BuildRequires: scrollkeeper
BuildRequires: desktop-file-utils
#gw if we run aclocal
BuildRequires: gnome-common
#(eandry) needed for pst files import plugin
BuildRequires: libpst-devel >= 0.6.41

%description
Evolution is the GNOME mailer, calendar, contact manager and
communications tool.  The tools which make up Evolution will
be tightly integrated with one another and act as a seamless
personal information-management tool. 

%package -n %{name}-devel
Summary:	Libraries and include files for developing Evolution components
Group:		Development/GNOME and GTK+
Requires:	%{name} = %{version}-%{release}
# gw all other devel deps are expressed by pkgconfig() deps
Requires:  gtkhtml-3.14-devel >= %{gtkhtml_version_required}
Obsoletes:	libevolution0-devel
Provides:	libevolution0-devel

%description -n %{name}-devel
Evolution is the GNOME mailer, calendar, contact manager and
communications tool.  The tools which make up Evolution will
be tightly integrated with one another and act as a seamless
personal information-management tool.

This package contains the files necessary to develop applications
using Evolution's libraries.

%if %with_mono
%package mono
Summary: Mono plugin loader for Evolution
Group: Communications
BuildRequires: mono-devel
Requires: %name = %version
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
%patch -p1 -b .diagnostics
#%patch17 -p1 -b .firstmail
%patch24 -p1 -b .spamassassin

%build

%configure2_5x \
--enable-plugins=experimental \
--with-krb5=%{_prefix} --with-krb5-libs=%{_libdir} \
--with-openldap=yes --with-static-ldap=no --with-sub-version="-%{release}"  \
--disable-nm \
%if %with_mono
--enable-mono=yes
%endif

%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

mkdir -p %{buildroot}%{_iconsdir}  %{buildroot}%{_liconsdir}  %{buildroot}%{_miconsdir}
cp -f %{SOURCE2} %{buildroot}%{_liconsdir}/evolution.png
cp -f %{SOURCE3} %{buildroot}%{_iconsdir}/evolution.png
cp -f %{SOURCE4} %{buildroot}%{_miconsdir}/evolution.png

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
Exec=%{_libdir}/evolution/%{major_version}/evolution-alarm-notify
Terminal=false
Type=Application
OnlyShowIn=GNOME;
Categories=
EOF

#remove unpackaged files
rm -rf %{buildroot}%{_libdir}/evolution/*/components/*.{a,la} \
 %{buildroot}%{_libdir}/evolution/*/plugins/*.la \
 %{buildroot}%{_libdir}/evolution/*/camel-providers/*.{a,la} \
 %{buildroot}%{_libdir}/evolution/*/conduits/*.la \
 %buildroot/var/lib/

# do not package obsolete mime-info files, evolution doesn't import them on commandline (Mdv bug #53984)
rm -fr %{buildroot}/%{_datadir}/mime-info

%{find_lang} %{name}-%{major_version} --with-gnome
%{find_lang} %{name} --with-gnome
cat %name.lang >> %{name}-%{major_version}.lang

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%define schemas apps_evolution_eplugin_face apps-evolution-external-editor apps_evolution_email_custom_header apps-evolution-mail-notification apps-evolution-mail-prompts-checkdefault apps_evolution_addressbook apps_evolution_calendar apps_evolution_shell bogo-junk-plugin evolution-mail apps-evolution-attachment-reminder apps-evolution-template-placeholders


%if %mdkversion < 200900
%post
%{update_scrollkeeper}
%{update_menus}
%post_install_gconf_schemas %{schemas}
%update_icon_cache hicolor
%endif

%preun
%preun_uninstall_gconf_schemas %{schemas}

%if %mdkversion < 200900
%postun
%{clean_scrollkeeper}
%{clean_menus}
%clean_icon_cache hicolor
%endif

%files -f %{name}-%{major_version}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_sysconfdir}/xdg/autostart/*.desktop
%_sysconfdir/gconf/schemas/apps-evolution-external-editor.schemas
%_sysconfdir/gconf/schemas/apps_evolution_email_custom_header.schemas
%_sysconfdir/gconf/schemas/apps-evolution-mail-notification.schemas
%_sysconfdir/gconf/schemas/apps-evolution-mail-prompts-checkdefault.schemas
%_sysconfdir/gconf/schemas/apps-evolution-template-placeholders.schemas
%_sysconfdir/gconf/schemas/apps_evolution_addressbook.schemas
%_sysconfdir/gconf/schemas/apps_evolution_eplugin_face.schemas
%_sysconfdir/gconf/schemas/apps-evolution-attachment-reminder.schemas
%_sysconfdir/gconf/schemas/apps_evolution_calendar.schemas
%_sysconfdir/gconf/schemas/apps_evolution_shell.schemas
%_sysconfdir/gconf/schemas/bogo-junk-plugin.schemas
%_sysconfdir/gconf/schemas/evolution-mail.schemas
%{_bindir}/*
%dir %{_libdir}/evolution
%dir %{_libdir}/evolution/%{major_version}
%{_libdir}/evolution/%{major_version}/csv2vcard
%{_libdir}/evolution/%{major_version}/evolution-addressbook-clean
%{_libdir}/evolution/%{major_version}/evolution-addressbook-export
%{_libdir}/evolution/%{major_version}/evolution-alarm-notify
%{_libdir}/evolution/%{major_version}/*.so.0*
%{_libdir}/evolution/%{major_version}/evolution-backup
%{_libdir}/evolution/%{major_version}/evolution-alarm-notify
%{_libdir}/evolution/%{major_version}/killev
%dir %{_libdir}/evolution/%{major_version}/modules/
%{_libdir}/evolution/%{major_version}/modules/libevolution-module-addressbook.*
%{_libdir}/evolution/%{major_version}/modules/libevolution-module-calendar.*
%{_libdir}/evolution/%{major_version}/modules/libevolution-module-mail.*
%{_libdir}/evolution/%{major_version}/modules/libevolution-module-mailto-handler.*
%{_libdir}/evolution/%{major_version}/modules/libevolution-module-plugin-lib.*
%{_libdir}/evolution/%{major_version}/modules/libevolution-module-startup-wizard.*
%dir %{_libdir}/evolution/%{major_version}/plugins
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-addressbook-file.*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-audio-inline.*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-b*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-c*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-d*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-email-custom-header.so
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-evolution-attachment-reminder.so
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-evolution-bbdb.*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-evolution-caldav.so
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-evolution-google.so

 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-evolution-webdav*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-external-editor.so
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-face*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-image-inline.so
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-imap*
# %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-evolution-mail-remote.so
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-g*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-itip-formatter.*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-m*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-p*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-s*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-t*
%{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-v*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-a*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-b*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-c*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-d*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-email-custom-header.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-evolution-attachment-reminder.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-evolution-bbdb.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-evolution-caldav.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-evolution-google.eplug
# %{_libdir}/evolution/%{major_version}/plugins/org-gnome-evolution-mail-remote.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-evolution-webdav.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-external-editor.*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-face*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-groupwise-features.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-itip-formatter.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-image-inline.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-imap*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-mail-notification*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-mail-to-task.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-mailing-list-actions.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-mark-all-read.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-plugin-manager.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-publish-calendar.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-prefer-plain.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-pst-import.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-sa-junk-plugin.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-save-calendar.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-subject-thread.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-templates.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-tnef-attachments.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-vcard-inline.eplug
%{_datadir}/applications/*
%{_datadir}/evolution
%_datadir/icons/hicolor/*/apps/*
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%{_miconsdir}/*.png
%{_datadir}/omf/*

%files -n %{name}-devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/evolution/%{major_version}/*.so
%{_libdir}/evolution/%{major_version}/*.la
%_datadir/gtk-doc/html/*

%if %with_mono
%files mono
%defattr(-, root, root)
%{_libdir}/evolution/%{major_version}/modules/*mono*
%endif
