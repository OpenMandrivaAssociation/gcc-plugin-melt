%define name gcc-plugin-melt
%define srcname melt-%{meltversion}-plugin-for-gcc-4.6-or-4.7
%define meltversion 0.9.5rc3
%define version 0.9.5.0.rc3

%define gccplugindir %(gcc -print-file-name=plugin)
%define vimdir %{_datadir}/vim

Name:		%{name}
Version:	%{version}
Epoch:		2
Release:	1
License:	GPLv3
Summary:	Middle End Lisp Translator GCC plugin
Group:		Development/C
URL:		https://gcc-melt.org
Source0:	http://gcc-melt.org/%{srcname}.tar.gz
# From https://gitorious.org/melt-vim-syntax/melt-vim-syntax/archive-tarball/master
Source1:	melt-vim-syntax.tar.gz
Source2:	ftdetect-melt.vim
Patch0:		melt-stage0-static.patch
Patch1:		gcc-plugin-melt-parallel-build.patch
Patch3:		melt-0.9.5rc3.fix-talpo.patch
Requires:	gcc
Requires:	gcc-plugin-devel
Suggests:	%{name}-doc
Suggests:	%{name}-vim
BuildConflicts:	gccmelt
BuildRequires:	gcc-plugin-devel
BuildRequires:	gmp-devel
BuildRequires:	ppl-devel
BuildRequires:	ppl_c-devel
BuildRequires:	mpfr-devel
BuildRequires:	libmpc-devel
BuildRequires:	texinfo
BuildRequires:	texi2html
BuildRequires:	autogen
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

%files
%{_bindir}/pygmentize-melt
%{gccplugindir}/include/*
%{gccplugindir}/melt-sources/*
%{gccplugindir}/melt-modules/*
%{gccplugindir}/melt-module.mk
%{gccplugindir}/melt.so

%package doc
Summary:	GCC MELT Plugin Documentation
BuildArch:	noarch

%description doc
This package provides the GCC MELT documentation.

%files doc
%doc %{_docdir}/gcc-plugin-melt-doc
%doc %{_infodir}/meltplugin.info*
%doc %{_infodir}/meltpluginapi.info*

%package vim
Summary:	VIM plugin to handle GCC MELT files
BuildArch:	noarch

%description vim
This package provides the VIM plugin for syntax and file
type handling of MELT sources.

%files vim
%{vimdir}/ftdetect/
%{vimdir}/ftplugin/
%{vimdir}/syntax/

%prep
%setup -q -n %{srcname} -a 1

# Required workaround suggested by basile to build on x86
#patch0 -p0 -b .stage0

# Removing of .NOTPARALLEL in MELT-Plugin-Makefile
# Must be one WITH usage of make -j (or %make)
#patch1 -p0 -b .notparallel

# Without '|| true', melt-tiny-tests fails
#patch2 -p0 -b .melt-tiny-tests

%patch3 -p0 -b .fix-talpo

# Avoid consuming too much memory
#sed -ri 								\
#	-e 's/MELTGCC_OPTIMFLAGS= -O2/MELTGCC_OPTIMFLAGS= -O0/g'	\
#	Makefile

%build
export LC_ALL=C
%make CC=g++ MELTGCC=gcc GCCMELT_CC=g++

%install
export LC_ALL=C
%make DESTDIR=%{buildroot}/ install

%{__install} -m755 -d %{buildroot}%{_bindir}
%{__install} -m755 -d %{buildroot}%{vimdir}
%{__install} -m755 -d %{buildroot}%{_infodir}
%{__install} -m755 -d %{buildroot}%{_docdir}/%{name}-doc/html/

%{__install} -m644 *.info %{buildroot}%{_infodir}
%{__install} -m644 *.html %{buildroot}%{_docdir}/%{name}-doc/html/

%{__install} -m644 -D %{SOURCE2} %{buildroot}%{vimdir}/ftdetect/melt.vim
%{__install} -m644 -D melt-vim-syntax-melt-vim-syntax/ftplugin/melt.vim %{buildroot}%{vimdir}/ftplugin/melt.vim
%{__install} -m644 -D melt-vim-syntax-melt-vim-syntax/syntax/melt.vim %{buildroot}%{vimdir}/syntax/melt.vim

%{__install} -m755 pygmentize-melt %{buildroot}%{_bindir}/

%clean
rm -fr %{buildroot}
