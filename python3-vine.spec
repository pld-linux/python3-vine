#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		vine
%define		egg_name	vine
%define		pypi_name	vine
Summary:	Python promises
Summary(pl.UTF-8):	Obietnice dla Pythona
Name:		python3-%{module}
Version:	5.0.0
Release:	2
License:	BSD
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/v/vine/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	2fc3270a999cdc9341ba173360d62367
URL:		https://vine.readthedocs.io/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools >= 1:20.6.7
%if %{with tests}
BuildRequires:	python3-case >= 1.3.1
BuildRequires:	python3-pytest >= 3.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_celery >= 1.1
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python promises.

%description -l pl.UTF-8
Obietnice (promise) dla Pythona.

%package apidocs
Summary:	API documentation for vine module
Summary(pl.UTF-8):	Dokumentacja API modułu vine
Group:		Documentation

%description apidocs
API documentation for vine module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu vine.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="case.pytest" \
%{__python3} -m pytest t/unit
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changelog LICENSE README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,reference,*.html,*.js}
%endif
