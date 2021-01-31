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
Name:		python-%{module}
# keep 1.x here for python2 support
Version:	1.3.0
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/v/vine/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	5d125e0b4d759b39e03d11902dede8c9
URL:		https://vine.readthedocs.io/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 20.6.7
%if %{with tests}
BuildRequires:	python-case >= 1.3.1
BuildRequires:	python-pytest >= 3.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools >= 20.6.7
%if %{with tests}
BuildRequires:	python3-case >= 1.3.1
BuildRequires:	python3-pytest >= 3.0
%endif
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg-3
BuildRequires:	python3-sphinx_celery >= 1.1
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python promises.

%description -l pl.UTF-8
Obietnice (promise) dla Pythona.

%package -n python3-%{module}
Summary:	Python promises
Summary(pl.UTF-8):	Obietnice dla Pythona
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-%{module}
Python promises.

%description -n python3-%{module} -l pl.UTF-8
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
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="case.pytest" \
%{__python} -m pytest t/unit
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="case.pytest" \
%{__python3} -m pytest t/unit
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc Changelog LICENSE README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc Changelog LICENSE README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,reference,*.html,*.js}
%endif
