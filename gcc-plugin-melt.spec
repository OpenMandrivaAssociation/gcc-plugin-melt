%define name gcc-plugin-melt
%define srcname melt-%{meltversion}-plugin-for-gcc-%{meltbranch}
%define gccversion 4.6.1
%define gccrelease 2
%define meltversion 0.7
%define meltbranch 4.6
%define version %{gccversion}+%{meltversion}

%define gccdir %(gcc -print-file-name=plugin)

Name:		%{name}
Version:	%{version}
Release:	5
License:	GPLv3
Summary:	Middle End Lisp Translator GCC plugin
Group:		Development/C
URL:		http://gcc-melt.org
Source0:	http://gcc-melt.org/%{srcname}.tgz
Patch0:		melt-stage0-static.patch
Patch1:		0001-MELT-Separate-build-and-install-steps.patch
Requires:	gcc
Suggests:	%{name}-doc
BuildRequires:	gcc-plugin-devel
BuildRequires:	gmp-devel
BuildRequires:	ppl-devel
BuildRequires:	ppl_c-devel
BuildRequires:	mpfr-devel
BuildRequires:	libmpc-devel
BuildRequires:	texinfo
BuildRequires:	texi2html
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Provides:	gccmelt

%description
GCC MELT is a GCC plugin providing a lispy domain specific
language to easily code GCC extensions in.

GCC MELT should interest any important software project
(coded in C, C++, Ada, Fortran, ...), compiled with GCC,
since it facilitates the development of customized GCC
extensions for:

* specific warnings or typechecks
* specific optimizations
* coding rules validation
* source code navigation or processing, in particular aspect
  oriented programming, retro-engineering or refactoring tasks
* Any processing taking advantage of powerful GCC internal
  representations of your source code.

%post
  %_install_info meltplugin.info
  %_install_info meltpluginapi.info

%preun
  %_remove_install_info meltplugin.info
  %_remove_install_info meltpluginapi.info

%files
%defattr(-,root,root,-)
%{_bindir}/pygmentize-melt
%{gccdir}/include/*
%{gccdir}/libexec/*
%{gccdir}/melt-source/*
%{gccdir}/melt.so
%{gccdir}/melt-build-module.mk
%{_infodir}/meltplugin*

%package doc
Summary:	GCC MELT Plugin Documentation
BuildArch:	noarch

%description doc
This packages provides the GCC MELT documentation.

%files doc
%doc %{_docdir}/gcc-plugin-melt-doc

%prep
%setup -q -n %{srcname}
# Required workaround suggested by basile to build on x86
%patch0 -p0 -b .stage0
%patch1 -p2 -b .compil

%build
./build-melt-plugin.sh -q					\
	-s DESTDIR=%{buildroot}/			\
	-M$PWD						\
	-Y$PWD/melt/generated/gt-melt-runtime-plugin.h	\
	-b

%install
./build-melt-plugin.sh -q				\
	-s DESTDIR=%{buildroot}/			\
	-M$PWD						\
	-Y$PWD/melt/generated/gt-melt-runtime-plugin.h	\
	-i

%{__install} -m755 -d %{buildroot}%{_bindir}
%{__install} -m755 -d %{buildroot}%{_infodir}
%{__install} -m755 -d %{buildroot}%{_docdir}/%{name}-doc/html/

%{__install} -m644 *.info %{buildroot}%{_infodir}
%{__install} -m644 *.html %{buildroot}%{_docdir}/%{name}-doc/html/

%{__install} -m755 pygmentize-melt %{buildroot}%{_bindir}/

%clean
rm -fr %{buildroot}
