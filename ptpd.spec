Summary:	PTPd implements the Precision Time protocol (PTP) as defined by the IEEE 1588
Name:		ptpd
Version:	2.3.0
Release:	1
License:	BSD
Group:		Daemons
Source0:	http://downloads.sourceforge.net/ptpd/%{name}-%{version}.tar.gz
# Source0-md5:	f5e931b4a229705ff0dbdfe22490566b
Source1:	%{name}2.service
Source2:	%{name}2
Source3:	%{name}2.conf
URL:		http://ptpd.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libpcap-devel
BuildRequires:	libtool
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	zlib-devel
Requires(post,preun,postun):	systemd-units >= 38
Requires:	systemd-units >= 0.38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The PTP daemon (PTPd) implements the Precision Time protocol (PTP) as
defined by the relevant IEEE 1588 standard. PTP was developed to
provide very precise time coordination of LAN connected computers.

PTPd is a complete implementation of the IEEE 1588 specification for a
standard (non-boundary) clock. PTPd has been tested with and is known
to work properly with other IEEE 1588 implementations.

%prep
%setup -q

%build
%{__aclocal} -I m4
%{__libtoolize}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-statistics \
	--enable-ntpdc \
	--enable-sigusr2=counters \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man{5,8},%{systemdunitdir},%{_localstatedir}/log,/etc/sysconfig}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdunitdir}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig
install -p src/ptpd2 $RPM_BUILD_ROOT%{_bindir}
cp -p src/ptpd2.8 $RPM_BUILD_ROOT%{_mandir}/man8
cp -p src/ptpd2.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5
# have to create the below, else ptpd will not log drift
touch $RPM_BUILD_ROOT%{_localstatedir}/log/ptpd2_kernelclock.drift

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post ptpd2.service

%preun
%systemd_preun ptpd2.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc COPYRIGHT ChangeLog README
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ptpd2
%config(noreplace) %{_sysconfdir}/ptpd2.conf
%attr(755,root,root) %{_bindir}/ptpd2
%{_mandir}/man5/ptpd2.conf.5*
%{_mandir}/man8/ptpd2.8*
%{systemdunitdir}/ptpd2.service
%config %{_localstatedir}/log/ptpd2_kernelclock.drift
