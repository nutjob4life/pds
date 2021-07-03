# PDS Namespace Packaging

This repository contains three small nearly identical Python source packages. All three provide a simple `main` program installed as `pds-experiment` that prints a "hello world" message and then lists each name found in the `pds.api_client` package. They differ as follows:

| Package   | Difference                                                         | Works |
| --------- | ------------------------------------------------------------------ |:-----:| 
| `non-pds` | Has a top-level `pds2` namespace package                           |   ✓   |
| `without` | Has a top-level `pds` module, but it's _not_ a namespace package   |   ✗   |
| `with`    | Has a top level `pds` module, and _is_ a namespace package         |   ✗   |

All three depend on `pds.api_client==0.6.0` (although [0.6.0 suffers from a separate bug](https://github.com/NASA-PDS/pds-api-client/issues/6)).

All three ought to work okay, except only the `non-pds` seems to function. As of this writing, this behavior appears with Python 3.9.5, `setuptools` 57.0.0, and `pip` 21.1.3.


## 📚 Reproduction

In each directory, do the following:

1.  `python3 -m venv venv`
2.  `venv/bin/pip install --quiet --upgrade setuptools pip wheel`
3.  `venv/bin/pip install --editable .`
4.  `venv/bin/pds-experiment`


## 🔬 Analysis

With the `non-pds` package, the experiment works because the top-level module is `pds2`; this does not conflict with the top-level module `pds` of `pds.client_api`. (`pds2` is also a namespace package, but that's orthogonal to this demonstraion.)

With the `without` package, the experiment fails with the error `ModuleNotFoundError: No module named 'pds.experiment'`. This seems to be caused by Python discovering that the `pds` module exists in `site-packages` and sets its `__path__` attribute as the root for all future lookups of `pds` submodules. This is fine for `pds.client_api` but prevents the console script from finding `pds.experiment.main`.

The `with` package has a top-level module `pds` but also declares it as a namespace package, which is the ideal case. However, `pds.client_api` is an issue here, too. The error message is `ModuleNotFoundError: No module named 'pds.api_client'`. In this case, Python seems to know now that `pds` is strictly a namespace, but then cannot resolve any non-namespace usage of `pds`, as in the case for `pds.client_api`.
