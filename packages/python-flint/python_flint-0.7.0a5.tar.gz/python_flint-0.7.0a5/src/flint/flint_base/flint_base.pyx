from flint.flintlib.types.flint cimport (
    FLINT_BITS as _FLINT_BITS,
    FLINT_VERSION as _FLINT_VERSION,
    __FLINT_RELEASE as _FLINT_RELEASE,
)
from flint.utils.flint_exceptions import DomainError
from flint.flintlib.types.mpoly cimport ordering_t
from flint.flint_base.flint_context cimport thectx
from flint.utils.typecheck cimport typecheck
cimport libc.stdlib

from collections.abc import Iterable
from flint.utils.flint_exceptions import IncompatibleContextError

from flint.types.fmpz cimport fmpz, any_as_fmpz

import enum

FLINT_BITS = _FLINT_BITS
FLINT_VERSION = _FLINT_VERSION.decode("ascii")
FLINT_RELEASE = _FLINT_RELEASE


cdef class flint_elem:
    def __repr__(self):
        if thectx.pretty:
            return self.str()
        else:
            return self.repr()

    def __str__(self):
        return self.str()


cdef class flint_scalar(flint_elem):
    # =================================================
    # These are the functions a new class should define
    # assumes that addition and multiplication are
    # commutative
    # =================================================
    def is_zero(self):
        return False

    def _any_as_self(self, other):
        return NotImplemented

    def _neg_(self):
        return NotImplemented

    def _add_(self, other):
        return NotImplemented

    def _sub_(self, other):
        return NotImplemented

    def _rsub_(self, other):
        return NotImplemented

    def _mul_(self, other):
        return NotImplemented

    def _div_(self, other):
        return NotImplemented

    def _rdiv_(self, other):
        return NotImplemented

    def _floordiv_(self, other):
        return NotImplemented

    def _rfloordiv_(self, other):
        return NotImplemented

    def _invert_(self):
        return NotImplemented

    # =================================================
    # Generic arithmetic using the above functions
    # =================================================

    def __pos__(self):
        return self

    def __neg__(self):
        return self._neg_()

    def __add__(self, other):
        other = self._any_as_self(other)
        if other is NotImplemented:
            return NotImplemented
        return self._add_(other)

    def __radd__(self, other):
        other = self._any_as_self(other)
        if other is NotImplemented:
            return NotImplemented
        return self._add_(other)

    def __sub__(self, other):
        other = self._any_as_self(other)
        if other is NotImplemented:
            return NotImplemented
        return self._sub_(other)

    def __rsub__(self, other):
        other = self._any_as_self(other)
        if other is NotImplemented:
            return NotImplemented
        return self._rsub_(other)

    def __mul__(self, other):
        other = self._any_as_self(other)
        if other is NotImplemented:
            return NotImplemented
        return self._mul_(other)

    def __rmul__(self, other):
        other = self._any_as_self(other)
        if other is NotImplemented:
            return NotImplemented
        return self._mul_(other)

    def __truediv__(self, other):
        other = self._any_as_self(other)
        if other is NotImplemented:
            return NotImplemented

        if other.is_zero():
            raise ZeroDivisionError

        return self._div_(other)

    def __rtruediv__(self, other):
        if self.is_zero():
            raise ZeroDivisionError

        other = self._any_as_self(other)
        if other is NotImplemented:
            return NotImplemented
        return self._rdiv_(other)

    def __floordiv__(self, other):
        other = self._any_as_self(other)
        if other is NotImplemented:
            return NotImplemented

        if other.is_zero():
            raise ZeroDivisionError

        return self._floordiv_(other)

    def __rfloordiv__(self, other):
        if self.is_zero():
            raise ZeroDivisionError

        other = self._any_as_self(other)
        if other is NotImplemented:
            return NotImplemented
        return self._rfloordiv_(other)

    def __invert__(self):
        if self.is_zero():
            raise ZeroDivisionError
        return self._invert_()


cdef class flint_poly(flint_elem):
    """
    Base class for polynomials.
    """

    def __iter__(self):
        cdef long i, n
        n = self.length()
        for i in range(n):
            yield self[i]

    def coeffs(self):
        """
        Returns the coefficients of ``self`` as a list

            >>> from flint import fmpz_poly
            >>> f = fmpz_poly([1,2,3,4,5])
            >>> f.coeffs()
            [1, 2, 3, 4, 5]
        """
        return list(self)

    def str(self, bint ascending=False, var="x", *args, **kwargs):
        """
        Convert to a human-readable string (generic implementation for
        all polynomial types).

        If *ascending* is *True*, the monomials are output from low degree to
        high, otherwise from high to low.
        """
        coeffs = [c.str(*args, **kwargs) for c in self]
        if not coeffs:
            return "0"
        s = []
        coeffs = enumerate(coeffs)
        if not ascending:
            coeffs = reversed(list(coeffs))
        for i, c in coeffs:
            if c == "0":
                continue
            else:
                if c.startswith("-") or (" " in c):
                    c = "(" + c + ")"
                if i == 0:
                    s.append("%s" % c)
                elif i == 1:
                    if c == "1":
                        s.append(var)
                    else:
                        s.append(f"{c}*{var}")
                else:
                    if c == "1":
                        s.append(f"{var}^{i}")
                    else:
                        s.append(f"{c}*{var}^{i}")
        return " + ".join(s)

    def roots(self):
        """
        Computes all the roots in the base ring of the polynomial.
        Returns a list of all pairs (*v*, *m*) where *v* is the
        integer root and *m* is the multiplicity of the root.

        To compute complex roots of a polynomial, instead use
        the ``.complex_roots()`` method, which is available on
        certain polynomial rings.

            >>> from flint import fmpz_poly
            >>> fmpz_poly([1, 2]).roots()
            []
            >>> fmpz_poly([2, 1]).roots()
            [(-2, 1)]
            >>> fmpz_poly([12, 7, 1]).roots()
            [(-3, 1), (-4, 1)]
            >>> (fmpz_poly([-5,1]) * fmpz_poly([-5,1]) * fmpz_poly([-3,1])).roots()
            [(3, 1), (5, 2)]
        """
        factor_fn = getattr(self, "factor", None)
        if not callable(factor_fn):
            raise NotImplementedError("Polynomial has no factor method, roots cannot be determined")

        roots = []
        factors = self.factor()
        for fac, m in factors[1]:
            if fac.degree() == 1:
                try:
                    v = - fac[0] / fac[1]
                except DomainError:
                    pass
                else:
                    roots.append((v, m))
        return roots

    def real_roots(self):
        raise NotImplementedError("Real roots are not supported for this polynomial")

    def complex_roots(self):
        raise NotImplementedError("Complex roots are not supported for this polynomial")


class Ordering(enum.Enum):
    lex = "lex"
    deglex = "deglex"
    degrevlex = "degrevlex"


cdef ordering_t ordering_py_to_c(ordering):
    if ordering == Ordering.lex:
        return ordering_t.ORD_LEX
    elif ordering == Ordering.deglex:
        return ordering_t.ORD_DEGLEX
    elif ordering == Ordering.degrevlex:
        return ordering_t.ORD_DEGREVLEX

cdef ordering_c_to_py(ordering_t ordering):
    if ordering == ordering_t.ORD_LEX:
        return Ordering.lex
    elif ordering == ordering_t.ORD_DEGLEX:
        return Ordering.deglex
    elif ordering == ordering_t.ORD_DEGREVLEX:
        return Ordering.degrevlex
    else:
        raise ValueError("unimplemented term order %d" % ordering)


cdef class flint_mpoly_context(flint_elem):
    """
    Base class for multivariate ring contexts
    """

    _ctx_cache = None

    def __init__(self, *_, **_2):
        raise RuntimeError(
            f"{self.__class__.__name__} should not be constructed directly. "
            f"Use '{self.__class__.__name__}.get' instead."
        )

    @classmethod
    def _new_(_, flint_mpoly_context self, names: Iterable[str]):
        """
        Constructor for all mpoly context types. This method is not intended for
        user-face use. See ``get`` instead.

        Construction via ``__init__`` is disabled to prevent the accidental creation of
        new mpoly contexts. By ensuring each context is unique they can be compared via
        pointer comparisons.

        Each concrete subclass should maintain their own context cache in
        ``_ctx_cache``, and the ``get`` method should insert newly created contexts into
        the cache.
        """
        self.py_names = tuple(name.encode("ascii") if not isinstance(name, bytes) else name for name in names)
        self.c_names = <const char**> libc.stdlib.malloc(len(names) * sizeof(const char *))
        for i in range(len(names)):
            self.c_names[i] = self.py_names[i]
        return self

    def __dealloc__(self):
        libc.stdlib.free(self.c_names)
        self.c_names = NULL

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.nvars()}, '{repr(self.ordering())}', {self.names()})"

    def name(self, i: int):
        if not 0 <= i < len(self.py_names):
            raise IndexError("variable name index out of range")
        return self.py_names[i].decode("ascii")

    def names(self) -> tuple[str]:
        return tuple(name.decode("ascii") for name in self.py_names)

    def gens(self):
        return tuple(self.gen(i) for i in range(self.nvars()))

    def variable_to_index(self, var: Union[int, str]) -> int:
        """Convert a variable name string or possible index to its index in the context."""
        if isinstance(var, str):
            try:
                i = self.names().index(var)
            except ValueError:
                raise ValueError("variable not in context")
        elif isinstance(var, int):
            if not 0 <= var < self.nvars():
                raise IndexError("generator index out of range")
            i = var
        else:
            raise TypeError("invalid variable type")

        return i

    @staticmethod
    def create_variable_names(names: str | Iterable[str | tuple[str, int]]) -> tuple[str]:
        """
        Create a tuple of variable names based off either ``str``, ``Iterable[str]``,
        ``tuple[str, int]``, or ``Iterable[tuple[str, int]]``.

            >>> flint_mpoly_context.create_variable_names('x')
            ('x',)
            >>> flint_mpoly_context.create_variable_names(('x', 3))
            ('x0', 'x1', 'x2')
            >>> flint_mpoly_context.create_variable_names([('x', 3), 'y'])
            ('x0', 'x1', 'x2', 'y')
        """
        res: list[str] = []

        # To avoid having to pass a nested tuple we allow a tuple[str, int]
        if len(names) == 2 and isinstance(names[0], str) and isinstance(names[1], int):
            names = (names,)

        for name in names:
            if isinstance(name, str):
                res.append(name)
            else:
                base, num = name
                if num < 0:
                    raise ValueError("cannot create a negative number of variables")
                res.extend(base + str(i) for i in range(num))

        return tuple(res)

    @classmethod
    def create_context_key(
            cls,
            names: str | Iterable[str | tuple[str, int]],
            ordering: Ordering | str = Ordering.lex
    ):
        """
        Create a key for the context cache via the variable names and the ordering.
        """
        return cls.create_variable_names(names), Ordering(ordering) if not isinstance(ordering, Ordering) else ordering

    @classmethod
    def get(cls, *args, **kwargs):
        """
        Retrieve or create a context via generator names, ``names`` and the ordering, ``ordering``.

        See ``create_variable_names`` for naming schemes.
        """
        key = cls.create_context_key(*args, **kwargs)

        ctx = cls._ctx_cache.get(key)
        if ctx is None:
            ctx = cls._ctx_cache.setdefault(key, cls._new_(*key))
        return ctx

    @classmethod
    def from_context(cls, ctx: flint_mpoly_context):
        return cls.get(
            ordering=ctx.ordering(),
            names=ctx.names(),
        )

    def _any_as_scalar(self, other):
        raise NotImplementedError("abstract method")

    def _scalar_as_mpoly(self, other):
        raise NotImplementedError("abstract method")

    def compatible_context_check(self, other):
        if not typecheck(other, type(self)):
            raise TypeError(f"type {type(other)} is not {type(self)}")
        elif other is not self:
            raise IncompatibleContextError(f"{other} is not {self}")

    def term(self, coeff = None, exp_vec = None):
        """
        Create a monomial from a coefficient and exponent vector. ``coeff`` defaults
        to ``1``. ``exp_vec``` defaults to ``(0,) * self.nvars()```.

            >>> from flint import fmpz_mpoly_ctx
            >>> ctx = fmpz_mpoly_ctx.get(('x', 2), 'lex')
            >>> ctx.term(coeff=5, exp_vec=(2, 3))
            5*x0^2*x1^3
            >>> ctx.term()
            1
        """
        if coeff is None:
            coeff = 1
        if exp_vec is None:
            exp_vec = (0,) * self.nvars()
        return self.from_dict({tuple(exp_vec): coeff})

cdef class flint_mod_mpoly_context(flint_mpoly_context):
    @classmethod
    def _new_(_, flint_mod_mpoly_context self, names, prime_modulus):
        super()._new_(self, names)
        self.__prime_modulus = <bint>prime_modulus

        return self

    @classmethod
    def create_context_key(
            cls,
            names: Iterable[str | tuple[str, int]],
            modulus,
            ordering: Ordering | str = Ordering.lex
    ):
        """
        Create a key for the context cache via the variable names, modulus, and the ordering.
        """
        return *super().create_context_key(names, ordering), modulus

    @classmethod
    def from_context(cls, ctx: flint_mod_mpoly_context):
        return cls.get(
            names=ctx.names(),
            modulus=ctx.modulus(),
            ordering=ctx.ordering(),
        )

    def is_prime(self):
        """
        Return whether the modulus is prime

            >>> from flint import fmpz_mod_mpoly_ctx
            >>> ctx = fmpz_mod_mpoly_ctx.get(('z',), 2**127, 'degrevlex')
            >>> ctx.is_prime()
            False
            >>> ctx = fmpz_mod_mpoly_ctx.get(('z',), 2**127 - 1, 'degrevlex')
            >>> ctx.is_prime()
            True
        """
        return self.__prime_modulus


cdef class flint_mpoly(flint_elem):
    """
    Base class for multivariate polynomials.
    """

    def leading_coefficient(self):
        return self.coefficient(0)

    def to_dict(self):
        return {self.monomial(i): self.coefficient(i) for i in range(len(self))}

    def _division_check(self, other):
        if not other:
            raise ZeroDivisionError(f"{self.__class__.__name__} division by zero")

    cdef _add_scalar_(self, other):
        return NotImplemented

    cdef _sub_scalar_(self, other):
        return NotImplemented

    cdef _mul_scalar_(self, other):
        return NotImplemented

    cdef _add_mpoly_(self, other):
        return NotImplemented

    cdef _sub_mpoly_(self, other):
        return NotImplemented

    cdef _mul_mpoly_(self, other):
        return NotImplemented

    cdef _divmod_mpoly_(self, other):
        return NotImplemented

    cdef _floordiv_mpoly_(self, other):
        return NotImplemented

    cdef _truediv_scalar_(self, other):
        return NotImplemented

    cdef _divexact_scalar_(self, other):
        return NotImplemented

    cdef _truediv_mpoly_(self, other):
        return NotImplemented

    cdef _mod_mpoly_(self, other):
        return NotImplemented

    cdef _rsub_scalar_(self, other):
        return NotImplemented

    cdef _rsub_mpoly_(self, other):
        return NotImplemented

    cdef _rdivmod_mpoly_(self, other):
        return NotImplemented

    cdef _rfloordiv_mpoly_(self, other):
        return NotImplemented

    cdef _rtruediv_mpoly_(self, other):
        return NotImplemented

    cdef _rmod_mpoly_(self, other):
        return NotImplemented

    cdef _pow_(self, other):
        return NotImplemented

    cdef _iadd_scalar_(self, other):
        return NotImplemented

    cdef _isub_scalar_(self, other):
        return NotImplemented

    cdef _imul_scalar_(self, other):
        return NotImplemented

    cdef _iadd_mpoly_(self, other):
        return NotImplemented

    cdef _isub_mpoly_(self, other):
        return NotImplemented

    cdef _imul_mpoly_(self, other):
        return NotImplemented

    def __add__(self, other):
        if typecheck(other, type(self)):
            self.context().compatible_context_check(other.context())
            return self._add_mpoly_(other)

        other = self.context()._any_as_scalar(other)
        if other is NotImplemented:
            return NotImplemented

        return self._add_scalar_(other)

    def __radd__(self, other):
        if typecheck(other, type(self)):
            self.context().compatible_context_check(other.context())
            return self._add_mpoly_(other)

        other = self.context()._any_as_scalar(other)
        if other is NotImplemented:
            return NotImplemented

        return self._add_scalar_(other)

    def __sub__(self, other):
        if typecheck(other, type(self)):
            self.context().compatible_context_check(other.context())
            return self._sub_mpoly_(other)

        other = self.context()._any_as_scalar(other)
        if other is NotImplemented:
            return NotImplemented

        return self._sub_scalar_(other)

    def __rsub__(self, other):
        if typecheck(other, type(self)):
            self.context().compatible_context_check(other.context())
            return self._rsub_mpoly_(other)

        other = self.context()._any_as_scalar(other)
        if other is NotImplemented:
            return NotImplemented

        return self._rsub_scalar_(other)

    def __mul__(self, other):
        if typecheck(other, type(self)):
            self.context().compatible_context_check(other.context())
            return self._mul_mpoly_(other)

        other = self.context()._any_as_scalar(other)
        if other is NotImplemented:
            return NotImplemented

        return self._mul_scalar_(other)

    def __rmul__(self, other):
        if typecheck(other, type(self)):
            self.context().compatible_context_check(other.context())
            return self._mul_mpoly_(other)

        other = self.context()._any_as_scalar(other)
        if other is NotImplemented:
            return NotImplemented

        return self._mul_scalar_(other)

    def __pow__(self, other, modulus):
        if modulus is not None:
            raise NotImplementedError("cannot specify modulus outside of the context")
        elif typecheck(other, fmpz):
            return self._pow_(other)

        other = any_as_fmpz(other)
        if other is NotImplemented:
            return NotImplemented
        elif other < 0:
            raise ValueError("cannot raise to a negative power")

        return self._pow_(other)

    def __divmod__(self, other):
        if typecheck(other, type(self)):
            self.context().compatible_context_check(other.context())
            self._division_check(other)
            return self._divmod_mpoly_(other)

        other = self.context()._any_as_scalar(other)
        if other is NotImplemented:
            return NotImplemented

        other = self.context()._scalar_as_mpoly(other)
        self._division_check(other)
        return self._divmod_mpoly_(other)

    def __rdivmod__(self, other):
        other = self.context()._any_as_scalar(other)
        if other is NotImplemented:
            return NotImplemented

        other = self.context()._scalar_as_mpoly(other)
        other._division_check(self)
        return self._rdivmod_mpoly_(other)

    def __truediv__(self, other):
        if typecheck(other, type(self)):
            self.context().compatible_context_check(other.context())
            self._division_check(other)
            return self._truediv_mpoly_(other)

        other = self.context()._any_as_scalar(other)
        if other is NotImplemented:
            return NotImplemented

        self._division_check(other)
        res = self._truediv_scalar_(other)
        if res is not NotImplemented:
            return res

        other = self.context()._scalar_as_mpoly(other)
        return self._truediv_mpoly_(other)

    def __rtruediv__(self, other):
        other = self.context()._any_as_scalar(other)
        if other is NotImplemented:
            return NotImplemented

        other = self.context()._scalar_as_mpoly(other)
        other._division_check(self)
        return self._rtruediv_mpoly_(other)

    def __floordiv__(self, other):
        if typecheck(other, type(self)):
            self.context().compatible_context_check(other.context())
            self._division_check(other)
            return self._floordiv_mpoly_(other)

        other = self.context()._any_as_scalar(other)
        if other is NotImplemented:
            return NotImplemented

        other = self.context()._scalar_as_mpoly(other)
        self._division_check(other)
        return self._floordiv_mpoly_(other)

    def __rfloordiv__(self, other):
        other = self.context()._any_as_scalar(other)
        if other is NotImplemented:
            return NotImplemented

        other = self.context()._scalar_as_mpoly(other)
        other._division_check(self)
        return self._rfloordiv_mpoly_(other)

    def __mod__(self, other):
        if typecheck(other, type(self)):
            self.context().compatible_context_check(other.context())
            self._division_check(other)
            return self._mod_mpoly_(other)

        other = self.context()._any_as_scalar(other)
        if other is NotImplemented:
            return NotImplemented

        other = self.context()._scalar_as_mpoly(other)
        self._division_check(other)
        return self._mod_mpoly_(other)

    def __rmod__(self, other):
        other = self.context()._any_as_scalar(other)
        if other is NotImplemented:
            return NotImplemented

        other = self.context()._scalar_as_mpoly(other)
        other._division_check(self)
        return self._rmod_mpoly_(other)

    def iadd(self, other):
        """
        In-place addition, mutates self.

            >>> from flint import fmpz_mpoly_ctx
            >>> ctx = fmpz_mpoly_ctx.get(('x', 2), 'lex')
            >>> f = ctx.from_dict({(1, 0): 2, (0, 1): 3, (1, 1): 4})
            >>> f
            4*x0*x1 + 2*x0 + 3*x1
            >>> f.iadd(5)
            >>> f
            4*x0*x1 + 2*x0 + 3*x1 + 5

        """
        if typecheck(other, type(self)):
            self.context().compatible_context_check(other.context())
            self._iadd_mpoly_(other)
            return

        other_scalar = self.context()._any_as_scalar(other)
        if other_scalar is NotImplemented:
            raise NotImplementedError(f"cannot add {type(self)} and {type(other)}")

        self._iadd_scalar_(other_scalar)

    def isub(self, other):
        """
        In-place subtraction, mutates self.

            >>> from flint import fmpz_mpoly_ctx
            >>> ctx = fmpz_mpoly_ctx.get(('x', 2), 'lex')
            >>> f = ctx.from_dict({(1, 0): 2, (0, 1): 3, (1, 1): 4})
            >>> f
            4*x0*x1 + 2*x0 + 3*x1
            >>> f.isub(5)
            >>> f
            4*x0*x1 + 2*x0 + 3*x1 - 5

        """
        if typecheck(other, type(self)):
            self.context().compatible_context_check(other.context())
            self._isub_mpoly_(other)
            return

        other_scalar = self.context()._any_as_scalar(other)
        if other_scalar is NotImplemented:
            raise NotImplementedError(f"cannot subtract {type(self)} and {type(other)}")

        self._isub_scalar_(other_scalar)

    def imul(self, other):
        """
        In-place multiplication, mutates self.

            >>> from flint import fmpz_mpoly_ctx
            >>> ctx = fmpz_mpoly_ctx.get(('x', 2), 'lex')
            >>> f = ctx.from_dict({(1, 0): 2, (0, 1): 3, (1, 1): 4})
            >>> f
            4*x0*x1 + 2*x0 + 3*x1
            >>> f.imul(2)
            >>> f
            8*x0*x1 + 4*x0 + 6*x1

        """
        if typecheck(other, type(self)):
            self.context().compatible_context_check(other.context())
            self._imul_mpoly_(other)
            return

        other_scalar = self.context()._any_as_scalar(other)
        if other_scalar is NotImplemented:
            raise NotImplementedError(f"cannot multiply {type(self)} and {type(other)}")

        self._imul_scalar_(other_scalar)

    def __contains__(self, x):
        """
        Returns True if ``self`` contains a term with exponent vector ``x`` and a non-zero coefficient.

            >>> from flint import fmpq_mpoly_ctx
            >>> ctx = fmpq_mpoly_ctx.get(('x', 2), 'lex')
            >>> p = ctx.from_dict({(0, 1): 2, (1, 1): 3})
            >>> (1, 1) in p
            True
            >>> (5, 1) in p
            False

        """
        return bool(self[x])

    def __iter__(self):
        return iter(self.monoms())

    def __pos__(self):
        return self

    def terms(self):
        """
        Return the exponent vectors and coefficient of each term.

            >>> from flint import fmpq_mpoly_ctx
            >>> ctx = fmpq_mpoly_ctx.get(('x', 2), 'lex')
            >>> f = ctx.from_dict({(0, 0): 1, (1, 0): 2, (0, 1): 3, (1, 1): 4})
            >>> list(f.terms())
            [((1, 1), 4), ((1, 0), 2), ((0, 1), 3), ((0, 0), 1)]

        """
        return zip(self.monoms(), self.coeffs())


cdef class flint_series(flint_elem):
    """
    Base class for power series.
    """
    def __iter__(self):
        cdef long i, n
        n = self.length()
        for i in range(n):
            yield self[i]

    def coeffs(self):
        return list(self)


cdef class flint_mat(flint_elem):
    """
    Base class for matrices.
    """

    def repr(self):
        # XXX
        return "%s(%i, %i, [%s])" % (type(self).__name__,
                                     self.nrows(),
                                     self.ncols(),
                                     ", ".join(map(str, self.entries())))

    def str(self, *args, **kwargs):
        tab = self.table()
        if len(tab) == 0 or len(tab[0]) == 0:
            return "[]"
        tab = [[r.str(*args, **kwargs) for r in row] for row in tab]
        widths = []
        for i in xrange(len(tab[0])):
            w = max([len(row[i]) for row in tab])
            widths.append(w)
        for i in xrange(len(tab)):
            tab[i] = [s.rjust(widths[j]) for j, s in enumerate(tab[i])]
            tab[i] = "[" + (", ".join(tab[i])) + "]"
        return "\n".join(tab)

    def entries(self):
        cdef long i, j, m, n
        m = self.nrows()
        n = self.ncols()
        L = [None] * (m * n)
        for i from 0 <= i < m:
            for j from 0 <= j < n:
                L[i*n + j] = self[i, j]
        return L

    def __iter__(self):
        cdef long i, j, m, n
        m = self.nrows()
        n = self.ncols()
        for i from 0 <= i < m:
            for j from 0 <= j < n:
                yield self[i, j]

    def table(self):
        cdef long i, m, n
        m = self.nrows()
        n = self.ncols()
        L = self.entries()
        return [L[i*n : (i+1)*n] for i in range(m)]

    # supports mpmath conversions
    tolist = table
