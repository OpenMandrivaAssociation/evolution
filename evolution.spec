%define major_version 2.24
%define gtkhtml_version_required 3.23.5
%define gnomepilot_version_required 2.0.14
%define gnomespell_version_required 1.0.5
%define libsoup_version_required 2.3.0
%define eds_version_required 2.23.91
%define with_mono 1
%{?_without_mono:	%{expand: %%global with_mono 0}}
%{?_with_mono:	%{expand: %%global with_mono 1}}


# disable underlinking check, because upstream has split libraries in such a strange way you can't build with no_undefined
%define _disable_ld_no_undefined 0

Name:		evolution
Summary:	Integrated GNOME mail client, calendar and address book
Version: 2.23.92
Release: %mkrel 1
License: 	LGPLv2+
Group:		Networking/Mail
Source0: 	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Source2:	evolution_48.png
Source3:	evolution_32.png
Source4:	evolution_16.png
Patch:		evolution-2.2.3-no-diagnostics.patch
# (fc) 1.5.94.1-4mdk import welcome mail from indexhtml
Patch17:	evolution-2.11.3-firstmail.patch
# (fc) 2.2.3-5mdk enable autocompletion on personal addressbook when creating it (Mdk bug #16427)
Patch18:	evolution-2.2.3-defaultcompletion.patch
# (fc) 2.11.92-3mdv configure default sound notification (Mdv bug #29414)
Patch21:	evolution-2.11.92-soundnotification.patch
# (fc) 2.22.0-4mdv set back spamassassin as default spam software (typo in gconf key from upstream)
Patch24:	evolution-2.22.0-spamassassin.patch

URL: 		http://www.gnome.org/projects/evolution/
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

# (fc) 0.8-5mdk implicit dependency is not enough
Requires: evolution-data-server >= %{eds_version_required}
Requires: gtkhtml-3.14 >= %{gtkhtml_version_required}
Requires: gnome-spell >= %{gnomespell_version_required}
Requires: gnupg
Requires: scrollkeeper >= 0.3
Requires: gtk+2.0 >= 2.4.0
Requires: indexhtml >= 10.1
Suggests: gstreamer0.10-plugins-good
Suggests: gnome-audio
Suggests: spamassassin
BuildRequires: bison flex
BuildRequires: dbus-glib-devel
BuildRequires: evolution-data-server-devel >= %{eds_version_required}
BuildRequires: gnome-pilot-devel >= %{gnomepilot_version_required}
BuildRequires: gtk+2-devel >= 2.4.0
BuildRequires: gtk-doc
BuildRequires: intltool
BuildRequires: krb5-devel 
BuildRequires: libgnomeui2-devel
BuildRequires: gstreamer0.10-devel
BuildRequires: gtkhtml-3.14-devel >= %{gtkhtml_version_required}
BuildRequires: libsoup-devel >= %{libsoup_version_required}
BuildRequires: nss-devel 
BuildRequires: openldap-devel 
BuildRequires: hal-devel
BuildRequires: libnotify-devel >= 0.3.0
#gw needed by the tnef plugin
BuildRequires: libytnef-devel
BuildRequires: gnome-icon-theme
BuildRequires: gnome-doc-utils
BuildRequires: scrollkeeper
BuildRequires: desktop-file-utils
#gw if we run aclocal
BuildRequires: gnome-common

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

%package pilot
Summary:	Evolution conduits for gnome-pilot
Group:		Communications
Requires:	%{name} = %{version}-%{release}
Requires:   gnome-pilot >= %{gnomepilot_version_required}

%description pilot
Evolution is the GNOME mailer, calendar, contact manager and
communications tool.  The tools which make up Evolution will
be tightly integrated with one another and act as a seamless
personal information-management tool.

This package contains conduits needed by gnome-pilot to 
synchronize your Palm with Evolution

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
%patch17 -p1 -b .firstmail
%patch18 -p1 -b .defaultcompletion
%patch21 -p1 -b .defaultsound
%patch24 -p1 -b .spamassassin

%build
%configure2_5x --enable-pilot-conduits=yes \
--enable-plugins=experimental \
--with-krb5=%{_prefix} --with-krb5-libs=%{_libdir} --without-krb4 \
--with-openldap=yes --with-static-ldap=no --with-sub-version="-%{release}" --enable-ipv6 --enable-default_binary \
%if %with_mono
--enable-mono=yes
%endif

%make

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%makeinstall_std

mkdir -p $RPM_BUILD_ROOT%{_iconsdir}  $RPM_BUILD_ROOT%{_liconsdir}  $RPM_BUILD_ROOT%{_miconsdir}
cp -f %{SOURCE2} $RPM_BUILD_ROOT%{_liconsdir}/evolution.png
cp -f %{SOURCE3} $RPM_BUILD_ROOT%{_iconsdir}/evolution.png
cp -f %{SOURCE4} $RPM_BUILD_ROOT%{_miconsdir}/evolution.png

desktop-file-install --vendor="" \
  --remove-category="Office" \
  --remove-category="Calendar" \
  --remove-category="ContactManagement" \
  --add-category="Network" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/evolution.desktop

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/ 

cat << EOF > $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/evolution-alarm-notify.desktop
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
rm -rf $RPM_BUILD_ROOT%{_libdir}/gnome-pilot/conduits/*.{a,la} \
 $RPM_BUILD_ROOT%{_libdir}/evolution/%{major_version}/components/*.{a,la} \
 $RPM_BUILD_ROOT%{_libdir}/evolution/%{major_version}/plugins/*.la \
 $RPM_BUILD_ROOT%{_libdir}/evolution/%{major_version}/camel-providers/*.{a,la} \
 $RPM_BUILD_ROOT%{_libdir}/evolution/%{major_version}/conduits/*.la \
 %buildroot/var/lib/


%{find_lang} %{name}-%{major_version} --with-gnome
%{find_lang} %{name} --with-gnome
cat %name.lang >> %{name}-%{major_version}.lang

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%define schemas apps-evolution-external-editor apps_evolution_email_custom_header apps-evolution-mail-notification apps-evolution-mail-prompts-checkdefault apps_evolution_addressbook apps_evolution_calendar apps_evolution_shell bogo-junk-plugin evolution-mail apps-evolution-attachment-reminder apps-evolution-template-placeholders


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
%_sysconfdir/gconf/schemas/apps-evolution-attachment-reminder.schemas
%_sysconfdir/gconf/schemas/apps_evolution_calendar.schemas
%_sysconfdir/gconf/schemas/apps_evolution_shell.schemas
%_sysconfdir/gconf/schemas/bogo-junk-plugin.schemas
%_sysconfdir/gconf/schemas/evolution-mail.schemas
%{_bindir}/*
%{_libdir}/bonobo/servers/*
%dir %{_libdir}/evolution
%dir %{_libdir}/evolution/%{major_version}
%dir %{_libdir}/evolution/%{major_version}/components
%{_libdir}/evolution/%{major_version}/csv2vcard
%{_libdir}/evolution/%{major_version}/evolution-addressbook-clean
%{_libdir}/evolution/%{major_version}/evolution-addressbook-export
%{_libdir}/evolution/%{major_version}/components/*.so
%{_libdir}/evolution/%{major_version}/*.so.*
%{_libdir}/evolution/%{major_version}/evolution-alarm-notify
%{_libdir}/evolution/%{major_version}/evolution-backup
%{_libdir}/evolution/%{major_version}/killev
%dir %{_libdir}/evolution/%{major_version}/plugins
 %{_libdir}/evolution/%{major_version}/plugins/attachment-reminder.glade
 %{_libdir}/evolution/%{major_version}/plugins/libmail-account-disable.*
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

 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-evolution-hula*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-evolution-webdav*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-external-editor.so
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-face*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-imap*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-ipod-sync-evolution.so
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-evolution-mail-attachments-import-ics.so
# %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-evolution-mail-remote.so
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-evolution-startup-wizard*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-exchange-operations.*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-g*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-itip-formatter.*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-m*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-p*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-s*
 %{_libdir}/evolution/%{major_version}/plugins/liborg-gnome-t*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-a*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-b*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-c*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-d*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-email-custom-header.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-evolution-attachment-reminder.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-evolution-bbdb.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-evolution-caldav.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-evolution-google.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-evolution-hula-account-setup.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-evolution-mail-attachments-import-ics.eplug
# %{_libdir}/evolution/%{major_version}/plugins/org-gnome-evolution-mail-remote.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-evolution-startup-wizard.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-evolution-webdav.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-exchange*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-external-editor.*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-face*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-folder-permissions.xml
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-folder-subscription.xml
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-groupwise-features.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-gw-account-setup.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-itip-formatter.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-imap*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-ipod-sync-evolution.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-mail-notification*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-mail-account-disable.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-mail-folder-unsubscribe.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-mail-to-meeting.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-mail-to-task.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-mail-to-task.xml
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-mailing-list-actions.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-mailing-list-actions.xml
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-mark-all-read.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-mark-calendar-offline.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-plugin-manager.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-plugin-manager.xml
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-publish-calendar.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-publish-calendar.xml
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-prefer-plain.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-sa-junk-plugin.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-save-attachments.*
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-save-calendar.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-select-one-source.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-subject-thread.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-subject-thread.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-templates.eplug
 %{_libdir}/evolution/%{major_version}/plugins/org-gnome-tnef-attachments.eplug
 %{_libdir}/evolution/%{major_version}/plugins/*.glade
%{_datadir}/applications/*
%{_datadir}/evolution
%{_datadir}/idl/*
%{_datadir}/mime-info/*
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

%if %with_mono
%files mono
%defattr(-, root, root)
%{_libdir}/evolution/%{major_version}/plugins/*mono*
%endif

%files pilot
%defattr(-, root, root)
%dir %{_libdir}/evolution/%{major_version}/conduits
%{_libdir}/evolution/%{major_version}/conduits/*.so
%{_datadir}/gnome-pilot/conduits/*
