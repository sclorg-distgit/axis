%{?scl:%scl_package axis}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 2

Name:          %{?scl_prefix}axis
Version:       1.4
Release:       29.%{baserelease}%{?dist}
Epoch:         0
Summary:       SOAP implementation in Java
License:       ASL 2.0
Group:         Development/Libraries
URL:           http://ws.apache.org/axis/
Source0:       axis-1.4-src.tar.gz
# svn export http://svn.apache.org/repos/asf/webservices/axis/branches/AXIS_1_4_FINAL/
# Build only
# cvs -d :pserver:anonymous@dev.eclipse.org:/cvsroot/tools export -r v1_1_0 org.eclipse.orbit/javax.xml.rpc/META-INF/MANIFEST.MF
# mv org.eclipse.orbit/javax.xml.rpc/META-INF/MANIFEST.MF xmlrpc-MANIFEST.MF
Source1: xmlrpc-MANIFEST.MF
# cvs -d :pserver:anonymous@dev.eclipse.org:/cvsroot/tools export -r v1_4_0 org.eclipse.orbit/org.apache.axis/META-INF/MANIFEST.MF
# mv org.eclipse.orbit/org.apache.axis/META-INF/MANIFEST.MF axis-MANIFEST.MF
Source2: axis-MANIFEST.MF
# cvs -d :pserver:anonymous@dev.eclipse.org:/cvsroot/tools export -r v1_3_0 org.eclipse.orbit/javax.xml.soap/META-INF/MANIFEST.MF
# mv org.eclipse.orbit/javax.xml.soap/META-INF/MANIFEST.MF saaj-MANIFEST.MF
Source3: saaj-MANIFEST.MF
Source4: http://repo1.maven.org/maven2/org/apache/axis/axis/1.4/axis-1.4.pom
Source5: http://repo1.maven.org/maven2/org/apache/axis/axis-ant/1.4/axis-ant-1.4.pom
Source6: http://repo1.maven.org/maven2/org/apache/axis/axis-jaxrpc/1.4/axis-jaxrpc-1.4.pom
Source7: http://repo1.maven.org/maven2/org/apache/axis/axis-saaj/1.4/axis-saaj-1.4.pom
# This POM is not present upstream, so a placeholder was created
Source8: axis-schema-1.4.pom
Source9: axis-ant-MANIFEST.MF
Patch0:        %{pkg_name}-java16.patch
Patch1:        %{pkg_name}-manifest.patch
Patch2:        axis-1.4-wsdl-pom.patch
# CVE-2012-5784: Does not verify that the server hostname matches X.509 certificate name
# https://issues.apache.org/jira/secure/attachment/12560257/CVE-2012-5784-2.patch
Patch3:        %{pkg_name}-CVE-2012-5784.patch
# Patch to use newer xml-commons-apis
Patch4:        axis-xml-commons-apis.patch

BuildRequires: %{?scl_prefix_java_common}jpackage-utils >= 0:1.6
BuildRequires: %{?scl_prefix_java_common}ant >= 0:1.6
BuildRequires: %{?scl_prefix_java_common}ant-junit
BuildRequires: %{?scl_prefix_maven}httpunit
BuildRequires: %{?scl_prefix_java_common}junit
BuildRequires: %{?scl_prefix_maven}xmlunit
# Main requires
BuildRequires: %{?scl_prefix_java_common}bea-stax-api
BuildRequires: %{?scl_prefix_java_common}bsf
BuildRequires: %{?scl_prefix_java_common}javamail
BuildRequires: %{?scl_prefix}glassfish-servlet-api
BuildRequires: %{?scl_prefix_java_common}apache-commons-discovery
BuildRequires: %{?scl_prefix_java_common}jakarta-commons-httpclient >= 1:3.0
BuildRequires: %{?scl_prefix_java_common}apache-commons-logging
BuildRequires: %{?scl_prefix_java_common}apache-commons-net
BuildRequires: %{?scl_prefix_java_common}jakarta-oro
BuildRequires: %{?scl_prefix_java_common}regexp
BuildRequires: %{?scl_prefix_java_common}log4j
BuildRequires: %{?scl_prefix}javax.wsdl
BuildRequires: %{?scl_prefix_java_common}xalan-j2
BuildRequires: %{?scl_prefix_java_common}xerces-j2
BuildRequires: %{?scl_prefix_java_common}xml-commons-apis
BuildRequires: zip
# optional requires
#BuildRequires: jimi


Requires:      %{?scl_prefix_java_common}jpackage-utils >= 0:1.6
Requires:      %{?scl_prefix_java_common}apache-commons-discovery
Requires:      %{?scl_prefix_java_common}apache-commons-logging
Requires:      %{?scl_prefix_java_common}jakarta-commons-httpclient >= 1:3.0
Requires:      %{?scl_prefix_java_common}log4j
Requires:      %{?scl_prefix_java_common}javamail
Requires:      %{?scl_prefix}javax.wsdl

BuildArch:     noarch

Provides:      %{?scl_prefix}javax.xml.rpc

%description
Apache AXIS is an implementation of the SOAP ("Simple Object Access Protocol")
submission to W3C.

From the draft W3C specification:

SOAP is a lightweight protocol for exchange of information in a decentralized,
distributed environment. It is an XML based protocol that consists of three
parts: an envelope that defines a framework for describing what is in a message
and how to process it, a set of encoding rules for expressing instances of
application-defined datatypes, and a convention for representing remote
procedure calls and responses.

This project is a follow-on to the Apache SOAP project.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
Javadoc for %{pkg_name}.

%package manual
Summary:        Manual for %{pkg_name}

%description manual
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n %{pkg_name}-%{version}-src
ln -s %{_javadocdir}/%{pkg_name} docs/apiDocs

# Remove provided binaries
#find . -name "*.jar" -exec rm -f {} \;
for f in $(find . -name "*.jar"); do mv $f $f.no; done
#find . -name "*.zip" -exec rm -f {} \;
for f in $(find . -name "*.zip"); do mv $f $f.no; done
#find . -name "*.class" -exec rm -f {} \;
for f in $(find . -name "*.class"); do mv $f $f.no; done

%patch0 -b .orig
%patch1 -b .orig

cp %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} .

# %patch2 -b .orig
%patch3 -p1 -b .orig
%patch4 -p1 -b .orig

# Disable doclinting for java 8
sed -i '/doctitle/a additionalparam="-Xdoclint:none"' build.xml
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
pushd lib
ln -sf $(build-classpath bea-stax-api) .
ln -sf $(build-classpath bsf) .
ln -sf $(build-classpath commons-discovery) .
ln -sf $(build-classpath commons-httpclient) .
ln -sf $(build-classpath commons-logging) .
ln -sf $(build-classpath commons-net) .
ln -sf $(build-classpath httpunit) .
ln -sf $(build-classpath log4j) .
ln -sf $(build-classpath oro) .
ln -sf $(build-classpath xalan-j2) .
ln -sf $(build-classpath wsdl4j) .
pushd endorsed
ln -sf $(build-classpath xerces-j2) .
ln -sf $(build-classpath xml-commons-apis) .
popd
ln -sf $(build-classpath javamail/mail) .
popd

ant \
    -Dant.build.javac.source=1.4 \
    -Dtest.functional.fail=no \
    -Dcommons-discovery.jar=$(build-classpath commons-discovery) \
    -Dcommons-httpclient.jar=$(build-classpath commons-httpclient) \
    -Dcommons-logging.jar=$(build-classpath commons-logging) \
    -Dlog4j-core.jar=$(build-classpath log4j) \
    -Dwsdl4j.jar=$(build-classpath wsdl4j) \
    -Dregexp.jar=$(build-classpath regexp) \
    -Dxmlunit.jar=$(build-classpath xmlunit) \
    -Dmailapi.jar=$(build-classpath javamail/mail) \
    -Dservlet.jar=$(build-classpath glassfish-servlet-api) \
    -Dbsf.jar=$(build-classpath bsf) \
    -Dcommons-net.jar=$(build-classpath commons-net) \
    -Dhttpunit.jar=$(build-classpath httpunit) \
    clean war javadocs # junit

#    -Djimi.jar=$(build-classpath jimi) \

# inject axis-ant OSGi manifest
mkdir -p META-INF
cp -p %{SOURCE9} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/lib/%{pkg_name}-ant.jar META-INF/MANIFEST.MF
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
### Jar files

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}

pushd build/lib
# install axis-schema.jar when xmlbeans is available
   install -m 644 axis.jar axis-ant.jar saaj.jar jaxrpc.jar \
           $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}
popd

### Javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{pkg_name}
cp -pr build/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{pkg_name}

install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{pkg_name}-%{version}/webapps
install -m 644 build/axis.war \
    $RPM_BUILD_ROOT%{_datadir}/%{pkg_name}-%{version}/webapps

# POMs
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -m 644 axis-1.4.pom $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{pkg_name}-axis.pom
%add_maven_depmap JPP.%{pkg_name}-axis.pom %{pkg_name}/axis.jar -a "axis:axis"
install -m 644 %{S:5} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{pkg_name}-axis-ant.pom
%add_maven_depmap JPP.%{pkg_name}-axis-ant.pom %{pkg_name}/axis-ant.jar -a "axis:axis-ant"
install -m 644 %{S:6} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{pkg_name}-jaxrpc.pom
%add_maven_depmap JPP.%{pkg_name}-jaxrpc.pom %{pkg_name}/jaxrpc.jar -a "axis:axis-jaxrpc"
install -m 644 %{S:7} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{pkg_name}-saaj.pom
%add_maven_depmap JPP.%{pkg_name}-saaj.pom %{pkg_name}/saaj.jar -a "axis:axis-saaj"

# J2EE API dir
install -d -m 755 %{buildroot}%{_javadir}/javax.xml.rpc/
ln -sf ../%{pkg_name}/jaxrpc.jar %{buildroot}%{_javadir}/javax.xml.rpc/
ln -sf ../%{pkg_name}/%{pkg_name}.jar %{buildroot}%{_javadir}/javax.xml.rpc/
build-jar-repository %{buildroot}%{_javadir}/javax.xml.rpc/ javax.wsdl \
              javamail apache-commons-logging apache-commons-discovery \
              jakarta-commons-httpclient log4j
%{?scl:EOF}


%files -f .mfiles
%doc LICENSE README release-notes.html changelog.html
%dir %{_javadir}/%{pkg_name}
%{_javadir}/javax.xml.rpc
%{_datadir}/%{pkg_name}-%{version}

%files javadoc
%{_javadocdir}/%{pkg_name}

%files manual
%doc docs/*

%changelog
* Tue Jul 26 2016 Mat Booth <mat.booth@redhat.com> - 0:1.4-29.2
- Avoid optional deps not available in the SCL

* Tue Jul 26 2016 Mat Booth <mat.booth@redhat.com> - 0:1.4-29.1
- Auto SCL-ise package for rh-eclipse46 collection

* Tue Jul 26 2016 Mat Booth <mat.booth@redhat.com> - 0:1.4-29
- Disable doclinting for java 8

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.4-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Alexander Kurtakov <akurtako@redhat.com> 0:1.4-27
- Fix FTBFS - switch to glassfish-servlet-api.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 0:1.4-24
- Use Requires: java-headless rebuild (#1067528)

* Tue Aug 13 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.4-23
- Add javax.xml.rpc provides and directory

* Wed Aug 07 2013 Mat Booth <fedora@matbooth.co.uk> - 0:1.4-22
- Update BR/R and patch to build against newer APIs, rhbz #992008

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.4-19
- Add missing connection hostname check against X.509 certificate name
- Resolves: CVE-2012-5784

* Tue Jul 31 2012 Andy Grimm <agrimm@gmail.com> - 0:1.4-18
- replace POMs with newer upstream versions using org.apache.axis gid

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Gerard Ryan <galileo@gedoraproject.org> 0:1.4-16
- Remove problematic comma from axis.jar manifest

* Sat Jun 23 2012 Gerard Ryan <galileo@gedoraproject.org> 0:1.4-15
- Fix existing OSGI manifests and add manifest to axis-ant.

* Fri May 11 2012 Marek Goldmann <mgoldman@redhat.com> 0:1.4-14
- Changed dependency from axis-wsdl4j to wsdl4j

* Mon Apr 30 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.4-13
- Revert RHEL conditionals - we are not getting complete build with them.

* Mon Apr 30 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.4-12
- Conditionalize xmlbeans/xml-security for RHEL.

* Mon Feb 13 2012 Andy Grimm <agrimm@gmail.com> - 0:1.4-11
- Add POM files from maven.org
- Uncomment optional BuildRequires to enable axis-schema build
- Disable tests, as they appear to be incompatible with junit4

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 01 2011 Andrew Robinson <arobinso@redhat.com> 0:1.4-9
- Inject orbit manifests to jars.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4-7
- Drop versioned jar and javadoc.
- Do not call build targets twice.
- Other cleanups per the new guidelines.

* Wed Oct 6 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4-6
- Fix javamail jar.

* Wed Oct 6 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4-5
- Fix groups.
- Use new package names.

* Fri Feb 12 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.4-4.1
- Update to 1.4.

* Fri Sep 25 2009 Dan Horak <dan[at]danny.cz> 0:1.2.1-7
- Backport fix for building with java 1.6, synced from F-11 branch (#511480, #523203)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.1-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.1-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 01 2008 Permaine Cheung <pcheung@redhat.com> 0:1.2.1-4.1
- Specify source=1.4 for javac

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0:1.2.1-4
- drop repotag
- fix license tag

* Thu Jun 05 2008 Permaine Cheung <pcheung@redhat.com> 0:1.2.1-3jpp.9
- Add javac.source=1.4 to the ant command for the build

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.2.1-3jpp.8
- Autorebuild for GCC 4.3

* Thu Apr 19 2007 Permaine Cheung <pcheung@redhat.com> 0:1.2.1-2jpp.8
- Rebuild

* Wed Apr 04 2007 Permaine Cheung <pcheung@redhat.com> 0:1.2.1-2jpp.7
- Fix building javadoc
- rpmlint cleanup

* Thu Aug 03 2006 Deepak Bhole <dbhole@redhat.com> 0:1.2.1-2jpp.6
- Added missing requirements

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:1.2.1-2jpp_5fc
- Rebuilt

* Wed Jul 19 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.2.1-2jpp_4fc
- Added conditional native compilation.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:1.2.1-2jpp_3fc
- rebuild

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:1.2.1-2jpp_2fc
- stop scriptlet spew

* Wed Mar  1 2006 Archit Shah <ashah@redhat.com> 0:1.2.1-2jpp_1fc
- remove unnecessary build dependencies on jacorb and jonathan-rmi
- include fix to Axis bug 2142
- merge from upstream 2jpp

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Jun 21 2005 Gary Benson <gbenson@redhat.com> 0:1.2.1-1jpp_1fc
- Upgrade to 1.2.1-1jpp.

* Fri Jun 17 2005 Fernando Nasser <fnasser@redhat.com> 0:1.2.1-1jpp
- Upgrade to 1.2.1 maintenance release

* Fri Jun 17 2005 Gary Benson <gbenson@redhat.com> 0:1.2-1jpp_1fc
- Work around file descripter leak (#160802).
- Build into Fedora.

* Mon Jun 13 2005 Gary Benson <gbenson@redhat.com>
- Add ObjectWeb's patch.

* Fri Jun 10 2005 Gary Benson <gbenson@redhat.com>
- Remove jarfiles from the tarball.

* Tue Jun  7 2005 Gary Benson <gbenson@redhat.com>
- Add DOM3 stubs to classes that need them (#152255).
- Avoid some API holes in libgcj's ImageIO implementation.
- Pick up CORBA and javax.rmi classes from jacorb and jonathan-rmi.

* Wed May 04 2005 Fernando Nasser <fnasser@redhat.com> 0:1.2-1jpp_1rh
- Merge with upstream for upgrade

* Wed May 04 2005 Fernando Nasser <fnasser@redhat.com> 0:1.2-1jpp
- Finaly 1.2 final release

* Sat Mar 12 2005 Ralph Apel <r.apel at r-apel.de>  0:1.2-0.rc2.3jpp
- Also Buildrequire ant-nodeps

* Fri Mar 11 2005 Ralph Apel <r.apel at r-apel.de>  0:1.2-0.rc2.2jpp
- Set OPT_JAR_LIST to "ant/ant-nodeps"
- Buildrequire ant >= 1.6

* Mon Feb 28 2005 Fernando Nasser <fnasser@redhat.com> 0:1.2-0.rc2.1jpp
- Upgrade to 1.2.rc2

* Fri Aug 20 2004 Ralph Apel <r.apel at r-apel.de>  0:1.1-3jpp
- Build with ant-1.6.2

* Thu Jun 26 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net>  0:1.1-2jpp
- fix javadoc versionning

* Thu Jun 26 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net>  0:1.1-1jpp
- Initial packaging
- no xml security for now since xml-security is not packaged yet
- functional tests not executed yet - seems they need some setup and do not
  run out of the box
- no webapp right now - file layout is too messy if hidden into a war file
  since jpp installs webapps expanded, this matters
