#!/bin/bash

. env.sh

yum -y install proftpd

echo '
# This is the ProFTPD configuration file
#
# See: http://www.proftpd.org/docs/directives/linked/by-name.html

# Server Config - config used for anything outside a <VirtualHost> or <Global> context
# See: http://www.proftpd.org/docs/howto/Vhost.html

ServerName			"ProFTPD server"
ServerIdent			on "FTP Server ready."
ServerAdmin			root@localhost
DefaultServer			on

# Cause every FTP user except adm to be chrooted into their home directory
# Aliasing /etc/security/pam_env.conf into the chroot allows pam_env to
# work at session-end time (http://bugzilla.redhat.com/477120)
VRootEngine			on
DefaultRoot			~ !adm
VRootAlias			/etc/security/pam_env.conf etc/security/pam_env.conf

# Use pam to authenticate (default) and be authoritative
# AuthPAMConfig			proftpd
AuthPAM				off
PersistentPasswd		off
RequireValidShell		off
AuthOrder			mod_auth_file.c # mod_auth_pam.c* mod_auth_unix.c
# Save user name and password in file
AuthUserFile			/etc/proftpd/ftpd.passwd

# Dont do reverse DNS lookups (hangs on DNS problems)
UseReverseDNS			off

# Set the user and group that the server runs as
User				work
Group				work

# To prevent DoS attacks, set the maximum number of child processes
# to 20.  If you need to allow more than 20 concurrent connections
# at once, simply increase this value.  Note that this ONLY works
# in standalone mode; in inetd mode you should use an inetd server
# that allows you to limit maximum number of processes per service
# (such as xinetd)
MaxInstances			20

# Disable sendfile by default since it breaks displaying the download speeds in
# ftptop and ftpwho
UseSendfile			off

# Define the log formats
LogFormat			default	"%h %l %u %t \"%r\" %s %b"
LogFormat			auth	"%v [%P] %h %t \"%r\" %s"

# TLS (http://www.castaglia.org/proftpd/modules/mod_tls.html)
<IfDefine TLS>
  TLSEngine			on
  TLSRequired			on
  TLSRSACertificateFile		/etc/pki/tls/certs/proftpd.pem
  TLSRSACertificateKeyFile	/etc/pki/tls/certs/proftpd.pem
  TLSCipherSuite		ALL:!ADH:!DES
  TLSOptions			NoCertRequest
  TLSVerifyClient		off
  #TLSRenegotiate		ctrl 3600 data 512000 required off timeout 300
  TLSLog			/var/log/proftpd/tls.log
  <IfModule mod_tls_shmcache.c>
    TLSSessionCache		shm:/file=/var/run/proftpd/sesscache
  </IfModule>
</IfDefine>

# Dynamic ban lists (http://www.proftpd.org/docs/contrib/mod_ban.html)
# Enable this with PROFTPD_OPTIONS=-DDYNAMIC_BAN_LISTS in /etc/sysconfig/proftpd
<IfDefine DYNAMIC_BAN_LISTS>
  LoadModule			mod_ban.c
  BanEngine			on
  BanLog			/var/log/proftpd/ban.log
  BanTable			/var/run/proftpd/ban.tab

  # If the same client reaches the MaxLoginAttempts limit 2 times
  # within 10 minutes, automatically add a ban for that client that
  # will expire after one hour.
  BanOnEvent			MaxLoginAttempts 2/00:10:00 01:00:00

  # Allow the FTP admin to manually add/remove bans
  BanControlsACLs		all allow user ftpadm
</IfDefine>

# Global Config - config common to Server Config and all virtual hosts
# See: http://www.proftpd.org/docs/howto/Vhost.html

# Umask 022 is a good standard umask to prevent new dirs and files
# from being group and world writable
Umask				022

# Allow users to overwrite files and change permissions
AllowOverwrite	        on	
<Limit ALL>
  AllowUser poly
  DenyALL
</Limit>
<Limit STOR MKD RNTO STOR STOU XMKD RETR DIRS READ>
        AllowAll
</Limit>

<Directory "/home/work/sites/">
    AllowOverwrite on
    <Limit ALL PWD LOGIN>
	AllowUser eagle
        DenyAll
    </Limit>
</Directory>' > /etc/proftpd.conf

mkdir -p /etc/proftpd/
touch /etc/proftpd/ftpd.passwd

if [ $OS_M_VERSION -eq 7 ]; then
    systemctl enable proftpd
    systemctl start proftpd
else
    chkconfig proftpd on
    /etc/init.d/proftpd start
fi
