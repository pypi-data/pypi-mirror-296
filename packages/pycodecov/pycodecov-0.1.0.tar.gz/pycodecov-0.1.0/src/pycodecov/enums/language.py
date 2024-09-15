"""
Module to store a str enum class representation programming languages.
"""

from enum import StrEnum

__all__ = ["Language"]


class Language(StrEnum):
    """
    A str enum class that define valid programming languages.

    Attributes:
        JAVASCRIPT: `"javascript"`
        SHELL: `"shell"`
        PYTHON: `"python"`
        RUBY: `"ruby"`
        PERL: `"perl"`
        DART: `"dart"`
        JAVA: `"java"`
        C: `"c"`
        CLOJURE: `"clojure"`
        D: `"d"`
        FORTRAN: `"fortran"`
        GO: `"go"`
        GROOVY: `"groovy"`
        KOTLIN: `"kotlin"`
        PHP: `"php"`
        R: `"r"`
        SCALA: `"scala"`
        SWIFT: `"swift"`
        OBJECTIVE_C: `"objective-c"`
        XTEND: `"xtend"`
        TYPESCRIPT: `"typescript"`
        HASKELL: `"haskell"`
        RUST: `"rust"`
        LUA: `"lua"`
        MATLAB: `"matlab"`
        ASSEMBLY: `"assembly"`
        SCHEME: `"scheme"`
        POWERSHELL: `"powershell"`
        APEX: `"apex"`
        VERILOG: `"verilog"`
        COMMON_LISP: `"common lisp"`
        ERLANG: `"erlang"`
        JULIA: `"julia"`
        PROLOG: `"prolog"`
        VUE: `"vue"`
        CPP: `"c++"`
        C_SHARP: `"c#"`
        F_SHARP: `"f#"`

    Examples:
        >>> Language("javascript")
        <Language.JAVASCRIPT: 'javascript'>
        >>> Language["JAVASCRIPT"]
        <Language.JAVASCRIPT: 'javascript'>
        >>> Language.JAVASCRIPT
        <Language.JAVASCRIPT: 'javascript'>
        >>> Language.JAVASCRIPT == "javascript"
        True
        >>> print(Language.JAVASCRIPT)
        javascript
    """

    JAVASCRIPT: str = "javascript"
    SHELL: str = "shell"
    PYTHON: str = "python"
    RUBY: str = "ruby"
    PERL: str = "perl"
    DART: str = "dart"
    JAVA: str = "java"
    C: str = "c"
    CLOJURE: str = "clojure"
    D: str = "d"
    FORTRAN: str = "fortran"
    GO: str = "go"
    GROOVY: str = "groovy"
    KOTLIN: str = "kotlin"
    PHP: str = "php"
    R: str = "r"
    SCALA: str = "scala"
    SWIFT: str = "swift"
    OBJECTIVE_C: str = "objective-c"
    XTEND: str = "xtend"
    TYPESCRIPT: str = "typescript"
    HASKELL: str = "haskell"
    RUST: str = "rust"
    LUA: str = "lua"
    MATLAB: str = "matlab"
    ASSEMBLY: str = "assembly"
    SCHEME: str = "scheme"
    POWERSHELL: str = "powershell"
    APEX: str = "apex"
    VERILOG: str = "verilog"
    COMMON_LISP: str = "common lisp"
    ERLANG: str = "erlang"
    JULIA: str = "julia"
    PROLOG: str = "prolog"
    VUE: str = "vue"
    CPP: str = "c++"
    C_SHARP: str = "c#"
    F_SHARP: str = "f#"
