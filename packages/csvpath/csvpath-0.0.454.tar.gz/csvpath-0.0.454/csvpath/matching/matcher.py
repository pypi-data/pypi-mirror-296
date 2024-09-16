""" Matching is the core of CsvPath. """

from typing import Any, List
from .productions import Equality, Matchable
from .functions.function import Function
from .util.expression_encoder import ExpressionEncoder
from .util.exceptions import MatchException
from . import LarkParser, LarkTransformer


class Matcher:  # pylint: disable=R0902
    """Matcher implements the match component rules processing that
    is applied to files line-by-line. matchers are created at the
    beginning of a run and are reset and reused for every line.
    """

    # re: R0902: no obvious improvements

    def __init__(self, *, csvpath=None, data=None, line=None, headers=None, myid=None):
        if not headers:
            # this could be a dry-run or unit testing
            pass
        if not data:
            raise MatchException(f"Inputs needed: data: {data}, headers: {headers}")
        self.path = data
        self.csvpath = csvpath
        self._line = line
        self._id = f"{myid}"
        self.expressions = []
        self.if_all_match = []
        self.skip = False
        self.cachers = []
        if data is not None:
            self.parser = LarkParser()
            tree = self.parser.parse(data)
            if self.csvpath:
                self.csvpath.logger.debug("Raw parse tree: %s", tree)
            transformer = LarkTransformer(self)
            es = transformer.transform(tree)
            # print(tree.pretty())
            expressions = []
            for e in es:
                expressions.append([e, None])
            self.expressions = expressions
            self.check_valid()
        if self.csvpath:
            self.csvpath.logger.info("initialized Matcher")

    def __str__(self):
        return f"""{type(self)}:
            expressions: {self.expressions}
            line: {self.line}"""

    @property
    def line(self) -> List[List[Any]]:  # pylint: disable=C0116
        return self._line

    @line.setter
    def line(self, line: List[List[Any]]) -> None:
        self._line = line

    def to_json(self, e) -> str:  # pylint: disable=C0116
        return ExpressionEncoder().to_json(e)

    def dump_all_expressions_to_json(self) -> str:  # pylint: disable=C0116
        return ExpressionEncoder().valued_list_to_json(self.expressions)

    def reset(self):  # pylint: disable=C0116
        for expression in self.expressions:
            expression[1] = None
            expression[0].reset()

    def header_index(self, name: str) -> int:
        """returns the index of a header name in the current headers. remember that
        a header_reset() can change the indexes mid file."""
        return self.csvpath.header_index(name)

    def header_name(self, i: int) -> str:
        """returns the name of a header given an index into the current headers.
        remember that a header_reset() can change the indexes mid file."""
        if not self.csvpath.headers:
            return None
        if i < 0 or i >= len(self.csvpath.headers):
            return None
        return self.csvpath.headers[i]

    def header_value(self, name: str) -> Any:
        """returns the value of a header name in the current line for the current
        headers. remember that a header_reset() can change the indexes mid file."""
        n = self.header_index(name)
        ret = None
        if n is None:
            pass
        else:
            ret = self.line[n]
        return ret

    def _do_lasts(self) -> None:
        for et in self.expressions:
            e = et[0]
            self._find_and_actvate_lasts(e)

    def _find_and_actvate_lasts(self, e) -> None:
        self.csvpath.logger.debug("Looking for last()s to activate")
        cs = e.children[:]
        while len(cs) > 0:
            c = cs.pop()
            if (
                isinstance(c, Equality)
                and c.op == "->"
                and c.left
                and isinstance(c.left, Function)
                and c.left.name == "last"
            ):
                c.matches(skip=[])
            elif isinstance(c, Function) and c.name == "last":
                c.matches(skip=[])
            else:
                cs += c.children

    def _cache_me(self, matchable: Matchable) -> None:
        self.cachers.append(matchable)

    def clear_caches(self) -> None:
        for _ in self.cachers:
            _.clear_caches()
        self.cachers = []

    def matches(self, *, syntax_only=False) -> bool:
        """this is the main work of the Matcher. we enumerate the self.expressions.
        if all evaluate to True in an AND operation we return True."""
        #
        # is this a blank last line? if so, we just want to activate any/all
        # last() in the csvpath.
        #
        if self.csvpath.line_monitor.is_last_line_and_blank(self.line):
            # if self.csvpath.line_monitor.is_last_line_and_empty(self.line):
            self.csvpath.logger.debug(
                "Is last line and blank. Doing lasts and then returning True"
            )
            self._do_lasts()
            return True
        ret = True
        failed = False
        self.csvpath.logger.debug(
            "beginning to match against line[%s]: %s",
            self.csvpath.line_monitor.physical_line_number,
            str(self.line),
        )
        for i, et in enumerate(self.expressions):
            self.csvpath.logger.debug(
                "Beginning to consider expression: et[%s]: %s: %s", i, et[0], et[1]
            )
            if self.csvpath and self.csvpath.stopped:
                #
                # stopped is like a system halt. this csvpath is calling it
                # quits on this CSV file. we don't continue to match the row
                # so we may miss out on some side effects. we just return
                # because the function already let the CsvPath know to stop.
                #
                pln = self.csvpath.line_monitor.physical_line_number
                self.csvpath.logger.debug("Stopped at line %s", pln)
                return False
            if self.skip is True:
                #
                # skip is like the continue statement in a python loop
                # we're not only not matching, we don't want any side effects
                # we might gain from continuing to check for a match;
                # but we also don't want to stop the run or fail validation
                #
                pln = self.csvpath.line_monitor.physical_line_number
                self.csvpath.logger.debug("Skipping at line %s", pln)
                self.skip = False
                return False
            if et[1] is True:
                ret = True
            elif et[1] is False:
                ret = False
            elif not et[0].matches(skip=[]) and not syntax_only:
                et[1] = False
                ret = False
            else:
                et[1] = True
                ret = True
            if not ret:
                failed = True
            #
            # if we're failed we need to (re)set ret in case this is the final iteration.
            #
            if failed:
                ret = False
        if ret is True:
            self.csvpath.logger.debug("Setting any vars deferred till match")
            self.do_set_if_all_match()
        else:
            pass
        #
        # here we could be set to do an OR, not an AND.
        # we would do that only in the case that the answer was False. if so, we
        # would recheck all self.expressions[.][1] for a True. if at least one
        # were found, we would respond True; else, False.
        #
        pln = self.csvpath.line_monitor.physical_line_number
        self.csvpath.logger.debug("Match result for line %s: %s", pln, ret)
        return ret

    def check_valid(self) -> None:  # pylint: disable=C0116
        for _ in self.expressions:
            _[0].check_valid()

    def do_set_if_all_match(self) -> None:  # pylint: disable=C0116
        for _ in self.if_all_match:
            name = _[0]
            value = _[1]
            tracking = _[2]
            self.set_variable(name, value=value, tracking=tracking)
        self.if_all_match = []

    def set_if_all_match(self, name: str, value: Any, tracking=None) -> None:
        """registers a variable set to happen only after the line's consideration
        is complete and it is found to match. this is used for setting variables
        when they have 'onmatch'; however, more recently we handle onmatch in
        another way. you can see that in Matchable."""
        self.if_all_match.append((name, value, tracking))

    def get_variable(self, name: str, *, tracking=None, set_if_none=None) -> Any:
        """see CsvPath.get_variable"""
        if self.csvpath is None:
            return None
        return self.csvpath.get_variable(
            name, tracking=tracking, set_if_none=set_if_none
        )

    def set_variable(self, name: str, *, value: Any, tracking=None) -> None:
        """see CsvPath.set_variable"""
        return self.csvpath.set_variable(name, value=value, tracking=tracking)

    def last_header_index(self) -> int:  # pylint: disable=C0116
        if self.line and len(self.line) > 0:
            return len(self.line) - 1
        return None

    def last_header_name(self) -> str:  # pylint: disable=C0116
        if self.csvpath.headers and len(self.csvpath.headers) > 0:
            return self.csvpath.headers[self.last_header_index()]
        return None
