import sys
from functools import update_wrapper

from typing import Hashable, Optional, List, overload


def has_alternatives(name: Hashable, *more_names: str) -> callable:
    """
    Gives a function the ability to have alternative versions which can be switched between at will.

    :param name: The name of the alternative for the initially-decorated function.
    :param more_names: Any other names desired to alias to this version of the function.
    """
    def wrapper(funk: callable) -> callable:
        options = {name: funk}
        for _name in more_names:
            options[_name] = funk

        class AlternativeFunk:
            def __init__(self, method=None):
                update_wrapper(self, method)
                self._inst = None
                self.cur_funk = funk
                self.cur_funks = {}

            def __call__(self, *args, **kwargs):
                if self._inst is not None:
                    return self.cur_funks[self._inst](self._inst, *args, **kwargs)

                return self.cur_funk(*args, **kwargs)

            def __get__(self, inst, owner):
                # This is how we know what class the method belongs to, if necessary.
                if inst is not None:
                    self._inst = inst
                    if inst not in self.cur_funks:
                        self.cur_funks[inst] = self.cur_funk

                else:
                    self._inst = None

                return self

            def set_alternative(self, name: Hashable):
                """
                Sets the alternative of the function to be used. Will throw an error if an invalid
                alternative is selected.

                :param name: The name of the desired alternative.
                """
                if self._inst is not None:
                    self.cur_funks[self._inst] = options[name]

                else:
                    self.cur_funk = options[name]

            def alternative(self, name: Hashable, *more_names: str):
                """
                Can be used to decorate other functions.

                **Example of Usage:**

                .. code-block:: python

                    @has_alternatives("llama")
                    def llama(shrub: str, /, age: int):
                        print(f'I am a llama. My favorite type of shrub is {shrub}.\n'
                              f'I am {age} years old.')

                    @llama.alternative("alpaca")
                    def alpaca(apple: str, /, age: int):
                        print(f'I am an alpaca. My favorite type of apple is {apple}.\n'
                              f'I am {age} years old.')

                .. warning::
                    While it is advised to only decorate functions with the same signature in this
                    fashion, it is not enforced. Please take this into consideration.

                .. note::
                    The decorated methods should have different names.

                :param name: The name to assign the alternative.
                :param more_names: Any other names desired to alias to this version of the function.
                """
                def inner_wrapper(_funk: callable) -> callable:
                    options[name] = _funk
                    for _name in more_names:
                        options[_name] = _funk

                    return self

                return inner_wrapper

        return AlternativeFunk(funk)

    return wrapper


def _not_defined_for_version():
    raise NotImplementedError(
        f'The function called is not implemented for the current version of Python '
        f'{repr(sys.version_info)}.'
    )


@overload
def versioned(funk: callable) -> callable: ...


def versioned(*min_version: int) -> callable:
    """
    Allows functions to only be created if they meet the correct Python version.

    :param min_version: The minimum version of Python the function requires. Each part of the
        version should be its own argument. For example: ``3.10.5`` would be input as ``3``, ``10``,
        ``5``. If the decorator is called directly on the target function, the target function will
        act as a default regardless of version. The same behavior will occur if this argument is
        simply absent.
    """
    # When the decorator is being used with arguments (technically zero arguments counts, as long as
    # parenthesis were used).
    if not len(min_version) or isinstance(min_version[0], int):
        def wrapper(funk: callable) -> callable:
            if not len(min_version):
                versions = {}
                def_version = funk

            else:
                versions = {min_version: funk}
                def_version = None

            def find_matching_version() -> Optional[callable]:
                _version = sys.version_info
                v_versions: List[tuple] = []
                for version, funk in versions.items():
                    if version <= _version:
                        v_versions.append(version)

                if len(v_versions):
                    return versions[max(v_versions)]

                return def_version

            class VersionedFunk:
                def __init__(self, method=None):
                    update_wrapper(self, method)
                    self._inst = None
                    self.cur_funk = funk
                    # self.cur_funks = {}
                    self.determined = False

                def __call__(self, *args, **kwargs):
                    if not self.determined:
                        self.cur_funk = find_matching_version()
                        self.determined = True

                    if self.cur_funk is None:
                        _not_defined_for_version()

                    if self._inst is not None:
                        # return self.cur_funks[self._inst](self._inst, *args, **kwargs)
                        return self.cur_funk(self._inst, *args, **kwargs)

                    return self.cur_funk(*args, **kwargs)

                def __get__(self, inst, owner):
                    # This is how we know what class the method belongs to, if necessary.
                    if inst is not None:
                        self._inst = inst
                        # if inst not in self.cur_funks:
                        #     self.cur_funks[inst] = self.cur_funk

                    else:
                        self._inst = None

                    return self

                def new_version(self, *min_version: int):
                    """
                    Can be used to decorate other functions.

                    **Example of Usage:**

                    .. code-block:: python

                        @versioned(3, 10)
                        def llama(shrub: str, /, age: int):
                            print(f'I am a llama. My favorite type of shrub is {shrub}.\n'
                                  f'I am {age} years old.')

                        @llama.new_version(3, 9)
                        def llama3_9(apple: str, /, age: int):
                            print(f'I am an alpaca. My favorite type of apple is {apple}.\n'
                                  f'I am {age} years old.')

                    .. warning::
                        While it is advised to only decorate functions with the same signature in
                        this fashion, it is not enforced. Please take this into consideration.

                    .. note::
                        The decorated methods should have different names.

                    :param min_version: The minimum version of Python needed for this version of
                        the function to work.
                    """
                    if not len(min_version):
                        raise ValueError('A version is required for all versioned functions other '
                                         'than the original.')

                    def inner_wrapper(_funk: callable) -> callable:
                        versions[min_version] = _funk
                        return self

                    return inner_wrapper

            return VersionedFunk(funk)

        return wrapper

    # If there are no arguments in minimum_version, then the function is a default for when no
    # version is matched.
    else:
        versions = {}
        # Assume the first argument is the function. All others will be discarded.
        funk = def_version = min_version[0]

        def find_matching_version() -> Optional[callable]:
            _version = sys.version_info
            v_versions: List[tuple] = []
            for version, funk in versions.items():
                if version <= _version:
                    v_versions.append(version)

            if len(v_versions):
                return versions[max(v_versions)]

            return def_version

        class VersionedFunk:
            def __init__(self, method=None):
                update_wrapper(self, method)
                self._inst = None
                self.cur_funk = funk
                # self.cur_funks = {}
                self.determined = False

            def __call__(self, *args, **kwargs):
                if not self.determined:
                    self.cur_funk = find_matching_version()
                    self.determined = True

                if self.cur_funk is None:
                    _not_defined_for_version()

                if self._inst is not None:
                    # return self.cur_funks[self._inst](self._inst, *args, **kwargs)
                    return self.cur_funk(self._inst, *args, **kwargs)

                return self.cur_funk(*args, **kwargs)

            def __get__(self, inst, owner):
                # This is how we know what class the method belongs to, if necessary.
                if inst is not None:
                    self._inst = inst
                    # if inst not in self.cur_funks:
                    #     self.cur_funks[inst] = self.cur_funk

                else:
                    self._inst = None

                return self

            def new_version(self, *min_version: int):
                """
                Can be used to decorate other functions.

                **Example of Usage:**

                .. code-block:: python

                    @versioned(3, 10)
                    def llama(shrub: str, /, age: int):
                        print(f'I am a llama. My favorite type of shrub is {shrub}.\n'
                              f'I am {age} years old.')

                    @llama.new_version(3, 9)
                    def llama3_9(apple: str, /, age: int):
                        print(f'I am an alpaca. My favorite type of apple is {apple}.\n'
                              f'I am {age} years old.')

                .. warning::
                    While it is advised to only decorate functions with the same signature in
                    this fashion, it is not enforced. Please take this into consideration.

                .. note::
                    The decorated methods should have different names.

                :param min_version: The minimum version of Python needed for this version of
                    the function to work.
                """
                if not len(min_version):
                    raise ValueError('A version is required for all versioned functions other '
                                     'than the original.')

                def inner_wrapper(_funk: callable) -> callable:
                    versions[min_version] = _funk
                    return self

                return inner_wrapper

        return VersionedFunk(funk)
