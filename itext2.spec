%define section free
%define gcj_support 1

Summary:        A Free Java-PDF library
Name:           itext2
Version:        2.0.1
Release:        %mkrel 2
Epoch:          0
License:        LGPL
URL:            http://www.lowagie.com/iText/
Group:          Development/Java
Source0:        http://ovh.dl.sourceforge.net/itext/itext-src-%{version}.tar.gz
Source1:        itext-www-20070221.tar.bz2
Source2:        itext-1.4-manifest.mf
Patch0:         itext-escape-jpeg-java-trap.patch
Patch1:         itext-2.0.0-no-get.patch
Requires:       bouncycastle-jdk1.4 >= 0:1.35
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant
BuildRequires:  ant-trax
BuildRequires:  bouncycastle-jdk1.4 >= 0:1.35
BuildRequires:  xalan-j2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
%else
BuildRequires:  java-devel >= 0:1.4.2
BuildRequires:  java-devel <= 0:1.5.0
BuildArch:      noarch
%endif

%description
iText is a library that allows you to generate PDF files on the fly. The 
iText classes are very useful for people who need to generate read-only, 
platform independent documents containing text, lists, tables and 
images. The library is especially useful in combination with Java(TM) 
technology-based Servlets: The look and feel of HTML is browser 
dependent; with iText and PDF you can control exactly how your servlet's 
output will look.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
API documentation for the %{name} package.

%package manual
Summary:        Documents for %{name}
Group:          Development/Java

%description manual
A programming manual for the %{name} package.

%prep
%setup -q -c -T -n itext
find . -type d -name CVS | xargs %{__rm} -rf
mkdir -p src/META-INF
(cd src
%{__tar} xf %{SOURCE0})
cp %{SOURCE2} src/META-INF/MANIFEST.MF
%{__tar} xf %{SOURCE1}
find . -name "*.jar" -exec rm {} \;
%patch0 -p0
%patch1 -p1
%{__perl} -pi -e 's/<link.*$//' src/ant/site.xml

%build
pushd src
export CLASSPATH=$(build-classpath bcprov-jdk14 bcmail-jdk14)
export OPT_JAR_LIST="ant/ant-trax xalan-j2 xalan-j2-serializer"
%{ant} jar javadoc tutorial lowagie.com
popd

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/bin/iText.jar \
      $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%{__perl} -pi -e 's/\r$//g' build/lowagie/*.{txt,xml}
%{__perl} -pi -e 's/\r$//g' build/lowagie/ant/*.xml
%{__perl} -pi -e 's/\r$//g' build/lowagie/ant/.ant.properties

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

# manual
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -a build/lowagie/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -a build/examples $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -a build/tutorial $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}/MPL-1.1.txt
%doc %{_docdir}/%{name}-%{version}/lgpl.txt
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}

%files manual
%defattr(0644,root,root,0755)
%doc %{_docdir}/*

# -----------------------------------------------------------------------------


