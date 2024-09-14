from __future__ import annotations

from typing import Dict, List, Optional, Tuple, Union

from netqasm.lang.instr.flavour import Flavour, VanillaFlavour
from netqasm.lang.operand import Template
from netqasm.lang.parsing.text import parse_text_subroutine

from qoala.lang import hostlang as hl
from qoala.lang.hostlang import IqoalaSingleton, IqoalaValue, IqoalaVar, IqoalaVector
from qoala.lang.program import LocalRoutine, ProgramMeta, QoalaProgram
from qoala.lang.request import (
    CallbackType,
    EprRole,
    EprType,
    QoalaRequest,
    RequestRoutine,
    RequestVirtIdMapping,
)
from qoala.lang.routine import RoutineMetadata

LHR_OP_NAMES: Dict[str, hl.ClassicalIqoalaOp] = {
    cls.OP_NAME: cls  # type: ignore
    for cls in [
        hl.SendCMsgOp,
        hl.ReceiveCMsgOp,
        hl.AddCValueOp,
        hl.MultiplyConstantCValueOp,
        hl.BitConditionalMultiplyConstantCValueOp,
        hl.AssignCValueOp,
        hl.RunSubroutineOp,
        hl.RunRequestOp,
        hl.ReturnResultOp,
        hl.BusyOp,
        hl.JumpOp,
        hl.BranchIfEqualOp,
        hl.BranchIfNotEqualOp,
        hl.BranchIfLessThanOp,
        hl.BranchIfGreaterThanOp,
    ]
}


class EndOfTextException(Exception):
    """ "
    This exception is raised when the parser unexpectedly reaches the end of the text.
    """

    pass


class QoalaParseError(Exception):
    """
    This exception is raised when the parser encounters an error in the text.
    """

    pass


def is_valid_name(name: str) -> bool:
    """Check if a string is a valid variable name.

    :param name: Name to check.

    :return: True if the string is a valid name, False otherwise. Acceptable names can only contain
    letters(a-z, A-Z), numbers(0-9) or underscores(_). Name must start with a letter, and cannot be
    a reserved keyword.

    """
    return name.isidentifier() and name[0].isalpha() and name not in LHR_OP_NAMES.keys()


class IqoalaMetaParser:
    """
    This class parses the Qoala program's metadata. The metadata is given in the following format:

    META_START
        name: <program name>
        parameters: <parameter 1>, <parameter 2>, ...
        csockets: <socket ID 1> -> <remote node name 1>, <socket ID 2> -> <remote node name 2>, ...
        epr_sockets: <socket ID 1> -> <remote node name 1>, <socket ID 2> -> <remote node name 2>, ...
    META_END

    The order of the metadata lines must be "name", "parameters", "csockets", "epr_sockets". The "name" line must
    have a single value, and the "parameters", "csockets", "epr_sockets" lines can have multiple values. Name,
    parameters, remote node names must be valid variable names.

    :param text: Text to parse.
    """

    def __init__(self, text: str) -> None:
        self._text = text
        lines = [line.strip() for line in text.split("\n")]
        self._lines = [line for line in lines if len(line) > 0]
        self._lineno: int = 0

    def _next_line(self) -> None:
        self._lineno += 1

    def _read_line(self) -> str:
        """
        Reads the next non-empty line in the text.

        :return: The next non-empty line in the text.
        :raises EndOfTextException: If the end of the text is reached unexpectedly.
        """
        while True:
            if self._lineno >= len(self._lines):
                raise EndOfTextException
            line = self._lines[self._lineno]
            self._next_line()
            if len(line) > 0:
                return line
            # if no non-empty line, will always break on EndOfLineException

    def _parse_meta_line(self, key: str, line: str) -> List[str]:
        """
        Parses a single line of the metadata.

        :param key: The key of the metadata line. For example, "name" or "parameters".
        :param line: The line to parse.
        :return: List of comma-separated values in the line.
        :raises QoalaParseError: If line does not have a single colon, or if the line does not
        start with the given key.
        """

        if line.count(":") != 1:
            raise QoalaParseError("Qoala Program Meta lines must have a single colon.")
        split = line.split(":")

        if split[0] != key:
            raise QoalaParseError(
                f"Qoala Program Meta line expected to start with {key}, but found {split[0]}."
            )
        if len(split) == 1 or len(split[1]) == 0:
            return []
        values = split[1].split(",")
        return [v.strip() for v in values]

    def _parse_meta_mapping(self, values: List[str]) -> Dict[int, str]:
        """
        Parses a mapping in the metadata. For example, the mapping from socket IDs to remote
        node names.

        :param values: List of key-value pairs separated by "->".
        :return: Dictionary of key-value pairs.

        :raises QoalaParseError: If the mapping does not have a single arrow "->" between the
        key and value, or if the key is not an integer.
        """
        result_dict = {}
        for v in values:
            if v.count("->") != 1:
                raise QoalaParseError(
                    "Qoala Program Meta mapping must have a single arrow '->' between socket ID and "
                    "remote node name."
                )
            key_value = [x.strip() for x in v.split("->")]
            try:
                socket_id = int(key_value[0])
            except ValueError:
                raise QoalaParseError(
                    "Qoala Program Meta socket ID must be an integer."
                )
            result_dict[socket_id] = key_value[1]
        return result_dict

    def parse(self) -> ProgramMeta:
        """
        Primary method of the class. Parses the metadata.

        :return: ProgramMeta object containing the metadata information given in the text.

        :raises QoalaParseError: If the text is not in the correct format. See the class
        description for the correct format.

        :raises EndOfTextException: If the end of the text is reached unexpectedly.
        """
        try:
            start_line = self._read_line()
            if start_line != "META_START":
                raise QoalaParseError("Qoala Program Meta must start with META_START.")

            name_values = self._parse_meta_line("name", self._read_line())
            if len(name_values) != 1:
                raise QoalaParseError(
                    "Qoala Program Meta name must have a single value."
                )
            name = name_values[0].strip()
            if not is_valid_name(name):
                raise QoalaParseError(
                    f"Value {name} in Qoala Program Meta is not a valid program name."
                )

            parameters = self._parse_meta_line("parameters", self._read_line())
            for param in parameters:
                if not is_valid_name(param):
                    raise QoalaParseError(
                        f"Value {param} in Qoala Program Meta is not a valid parameter name."
                    )

            csockets_map = self._parse_meta_line("csockets", self._read_line())
            csockets = self._parse_meta_mapping(csockets_map)
            for node_name in csockets.values():
                if not is_valid_name(node_name):
                    raise QoalaParseError(
                        f"Value {node_name} in Qoala Program Meta is not a valid remote node name."
                    )
            epr_sockets_map = self._parse_meta_line("epr_sockets", self._read_line())
            epr_sockets = self._parse_meta_mapping(epr_sockets_map)
            for node_name in epr_sockets.values():
                if not is_valid_name(node_name):
                    raise QoalaParseError(
                        f"Value {node_name} in Qoala Program Meta is not a valid remote node name."
                    )

            end_line = self._read_line()
            if end_line != "META_END":
                raise QoalaParseError("Qoala Program Meta must start with META_END.")
        except EndOfTextException:
            raise QoalaParseError("Qoala Program Meta finished unexpectedly.")

        return ProgramMeta(name, parameters, csockets, epr_sockets)


class IqoalaInstrParser:
    """
    This class parses instructions in a single block of a Qoala program. The instructions are given in the following
    format:

    <result> = <operation>(<argument 1>, <argument 2>, ...): <attribute>

    Tuple format is: tuple<value 1>; <value 2>; ...> i.e. tuple<x; y>
    Vector format is: <vector name><vector size> i.e. my_vec<5>
    Vector indexing format is: <vector name>[<index>] i.e. my_vec[3]
    singleton format is: <singleton name> i.e. x

    Both vectors and singletons are passed similarly as an argument. In order to differentiate between them, the
    parser internally stores the defined vectors. Also, all variable names must be valid variable names.

    :param text: Text to parse.
    :param defined_vectors: Dictionary of defined vectors. The keys are the names of the vectors, and the values
    are the vectors themselves. For each Qoala Program it is stored in HostCodeParser and passed to the
    IqoalaInstrParser.

    """

    def __init__(
        self, text: str, defined_vectors: Optional[Dict[str, hl.IqoalaVector]] = None
    ) -> None:
        self._text = text
        lines = [line.strip() for line in text.split("\n")]
        self._lines = [line for line in lines if len(line) > 0]
        self._lineno: int = 0
        self._defined_vectors: Dict[str, hl.IqoalaVector] = {}
        if defined_vectors is not None:
            self._defined_vectors = defined_vectors

    def _next_line(self) -> None:
        self._lineno += 1

    def _read_line(self) -> str:
        """
        Reads the next non-empty line in the text.

        :return: The next non-empty line in the text.
        :raises EndOfTextException: If the end of the text is reached unexpectedly.
        """
        while True:
            if self._lineno >= len(self._lines):
                raise EndOfTextException
            line = self._lines[self._lineno]
            self._next_line()
            if len(line) > 0:
                return line
            # if no non-empty line, will always break on EndOfLineException

    def _parse_var(self, var_str: str, is_result=False) -> IqoalaVar:
        """
        Parses a variable in the instruction. The variable can be a singleton, a vector, a tuple, or a vector
        element.

        :param var_str: The variable to parse.
        :param is_result: True if the variable is a result variable, False otherwise. It is used to ensure that
        vectors are defined only as result variables.

        :return: Variable parsed into its corresponding IqoalaVar object. For example, tuples are parsed into
        IqoalaTuple objects, and vectors are parsed into IqoalaVector objects.

        :raises QoalaParseError: If the variable is not in the correct format. See the class description for the
        correct format, or if a vector is defined as a non-result variable, or if a vector is indexed before
        being defined.
        """
        if var_str.startswith("tuple"):
            if var_str[5] != "<" or not var_str.endswith(">"):
                raise QoalaParseError(
                    "Iqoala tuple must start with 'tuple<' and end with '>'."
                )
            if var_str.count("<") > 1 or var_str.count(">") > 1:
                raise QoalaParseError(
                    "Iqoala tuple must have a single '<' and a single '>'."
                )
            tup_values_str = var_str[6:-1]
            if len(tup_values_str) == 0:
                tup_values = []
            else:
                tup_values = [x.strip() for x in tup_values_str.split(";")]
            for tup_value in tup_values:
                if not is_valid_name(tup_value):
                    raise QoalaParseError(
                        f"Value {tup_value} is not a valid variable name."
                    )
            return hl.IqoalaTuple(tup_values)
        elif "<" in var_str:
            if not is_result:
                raise QoalaParseError(
                    "Iqoala vector size cannot be specified for non-result variables."
                )
            if var_str.startswith("<"):
                raise QoalaParseError("Iqoala vector must start with a name.")
            if not var_str.endswith(">"):
                raise QoalaParseError("Iqoala vector must end with a '>'.")
            if var_str.count("<") != 1 or var_str.count(">") != 1:
                raise QoalaParseError(
                    "Iqoala vector must have a single '<' and a single '>'."
                )
            vec_split = var_str.split("<")
            vec_name = vec_split[0]
            if not is_valid_name(vec_name):
                raise QoalaParseError(f"Value {vec_name} is not a valid variable name.")
            vec_size_str = vec_split[1][:-1]  # strip last ">"
            vec_size: IqoalaValue  # Template is not used insde the blocks
            try:
                vec_size = int(vec_size_str)
            except ValueError:
                if not is_valid_name(vec_size_str):
                    raise QoalaParseError(
                        f"Value {vec_size_str} is not a valid variable name."
                    )
                vec_size = vec_size_str
            return hl.IqoalaVector(vec_name, vec_size)
        elif "[" in var_str:
            if var_str.startswith("["):
                raise QoalaParseError("Iqoala vector indexing must start with a name.")
            if not var_str.endswith("]"):
                raise QoalaParseError("Iqoala vector indexing must end with a ']'.")
            if var_str.count("[") != 1 or var_str.count("]") != 1:
                raise QoalaParseError(
                    "Iqoala vector indexing must have a single '[' and a single ']'."
                )
            vec_split = var_str.split("[")
            vec_name = vec_split[0]
            if not is_valid_name(vec_name):
                raise QoalaParseError(f"Value {vec_name} is not a valid variable name.")
            if vec_name not in self._defined_vectors:
                raise QoalaParseError(
                    f"Iqoala vector {vec_name} must be defined before indexing."
                )
            index_str = vec_split[1][:-1]  # strip last "]"
            index: int
            try:
                index = int(index_str)
            except ValueError:
                raise QoalaParseError("Iqoala vector indexing must be an integer.")
            return hl.IqoalaVectorElement(vec_name, index)
        else:
            if not is_valid_name(var_str):
                raise QoalaParseError(f"Value {var_str} is not a valid variable name.")
            if var_str in self._defined_vectors:
                return self._defined_vectors[var_str]
            return IqoalaSingleton(var_str)

    def _parse_lhr(self) -> hl.ClassicalIqoalaOp:
        """
        Parses a single instruction in the Qoala program. The instruction format is given in the class description.

        :return: The parsed instruction in the form of a ClassicalIqoalaOp object.

        :raises QoalaParseError: If the instruction is not in the correct format. See the class description for
        the correct format.
        """
        line = self._read_line()

        attr: Optional[hl.IqoalaValue]

        assign_parts = [x.strip() for x in line.split("=")]
        if len(assign_parts) > 2:
            raise QoalaParseError("Iqoala instruction can have at most one '='.")
        if len(assign_parts) == 1:
            value = assign_parts[0]
            result = None
        elif len(assign_parts) == 2:
            value = assign_parts[1]
            result = self._parse_var(assign_parts[0], is_result=True)
            if isinstance(result, hl.IqoalaVector):
                self._defined_vectors[result.name] = result
        value_parts = [x.strip() for x in value.split(":")]
        if len(value_parts) > 2:
            raise QoalaParseError("Iqoala instruction can have at most one ':'.")
        if len(value_parts) == 2:
            value = value_parts[0].strip()
            attr_str = value_parts[1].strip()
            try:
                attr = int(attr_str)
            except ValueError:
                attr = attr_str
        else:
            value = value_parts[0]
            attr = None

        op_parts = [x.strip() for x in value.split("(")]
        if value.startswith("("):
            raise QoalaParseError("Iqoala instruction must have a name before '('.")
        if value.count("(") != 1 or value.count(")") != 1:
            raise QoalaParseError(
                "Iqoala instruction must have a single '(' and a single ')'."
            )
        if not value.endswith(")"):
            raise QoalaParseError(
                "In Iqoala instruction, operation must end with ')' or it must have a ')' "
                "before attributes."
            )
        op = op_parts[0]
        arguments = op_parts[1].rstrip(")")
        if len(arguments) == 0:
            raw_args = []
        else:
            raw_args = [x.strip() for x in arguments.split(",")]

        args = [self._parse_var(arg) for arg in raw_args]

        lhr_op = LHR_OP_NAMES[op].from_generic_args(result, args, attr)  # type: ignore
        return lhr_op

    def parse(self) -> List[hl.ClassicalIqoalaOp]:
        """
        Primary method of the class. Parses the instructions in a single block.

        :return: List of parsed instructions.

        :raises EndOfTextException: If the end of the text is reached unexpectedly.
        """
        instructions: List[hl.ClassicalIqoalaOp] = []

        try:
            while True:
                instr = self._parse_lhr()
                instructions.append(instr)
        except EndOfTextException:
            pass

        return instructions


class HostCodeParser:
    """
    This class parses the blocks of a Qoala program. The blocks are given in the following format:

    ^<block name>{type: <block type>, [<other block name> : <deadline>, ...]}:
        <instruction 1>
        <instruction 2>
        ...

    The block name must be a valid variable name. The block type must be one of the following: 'CL', 'CC', 'QL', 'QC'.
    The block type is case-insensitive. The block deadline is optional. It internally stores the defined vectors, and
    passes them to the IqoalaInstrParser for each block.

    :param text: Text to parse.
    """

    def __init__(self, text: str) -> None:
        self._text = text
        lines = [line.strip() for line in text.split("\n")]
        self._lines = [
            line for line in lines if len(line) > 0 and not line.startswith("//")
        ]
        self._lineno: int = 0
        self._defined_vectors: Dict[str, hl.IqoalaVector] = {}  # name -> vector

    def get_block_texts(self) -> List[str]:
        """
        Gets the text of each block in the Qoala program. Both the block header and the block instructions are
        included in the text.

        :return: List of block texts.
        :raises QoalaParseError: If the Qoala program does not have any blocks.
        """
        block_start_lines: List[int] = []

        for i, line in enumerate(self._lines):
            if line.startswith("^"):
                block_start_lines.append(i)

        if len(block_start_lines) == 0:
            raise QoalaParseError("Qoala program must have at least one block.")

        block_texts: List[str] = []
        for i in range(len(block_start_lines) - 1):
            start = block_start_lines[i]
            end = block_start_lines[i + 1]
            text = self._lines[start:end]
            block_texts.append("\n".join([line for line in text]))

        last = block_start_lines[-1]
        last_text = self._lines[last:]
        block_texts.append("\n".join([line for line in last_text]))

        return block_texts

    def _parse_deadlines(self, text: str) -> Dict[str, int]:
        """
        Parses the deadlines of a block. The deadline format is given in the class description.

        :param text: Text to parse.
        :return: Dictionary of block names and their corresponding deadlines.
        """
        open_bracket = text.find("[")
        assert open_bracket >= 0
        close_bracket = text.find("]")
        assert close_bracket >= 0
        items = text[open_bracket + 1 : close_bracket].split(",")
        deadlines = {}
        for item in items:
            blk, dl = [i.strip() for i in item.split(":")]
            deadlines[blk] = int(dl)
        return deadlines

    def _parse_block_annotations(
        self, annotations: str
    ) -> Tuple[hl.BasicBlockType, Optional[Dict[str, int]]]:
        """
        Parses the annotations of a block which are the block type and deadlines. The annotations format is given
        in the class description.

        :param annotations: Annotations text to parse.
        :return: Tuple containing the block type and the deadlines.
        :raises QoalaParseError: If the annotations are not in the correct format. See the class description for
        the correct format.
        """
        annotations_parts = annotations.split(",")
        if annotations_parts[0].count("=") != 1:
            raise QoalaParseError("Block type annotation must have exactly one '='.")
        type_annotation_parts = [x.strip() for x in annotations_parts[0].split("=")]
        if type_annotation_parts[0] != "type":
            raise QoalaParseError("Block type annotation must start with 'type'.")
        raw_typ = type_annotation_parts[1][-2:]
        try:
            typ = hl.BasicBlockType[raw_typ.upper()]
        except KeyError:
            raise QoalaParseError(
                "Invalid block type. Block type must be one of the "
                "following: 'CL', 'CC', 'QL', 'QC' (case insensitive)."
            )
        if len(annotations_parts) == 1:  # no deadline
            deadlines = None
        else:
            deadlines_str = annotations_parts[1].strip()
            deadlines = self._parse_deadlines(deadlines_str[12:])
        return typ, deadlines

    def _parse_block_header(
        self, line: str
    ) -> Tuple[str, hl.BasicBlockType, Optional[Dict[str, int]]]:
        """
        Parses the header of a block. Header contains the block name, block type, and block deadlines. The header
        format is given in the class description.

        :param line: Header text to parse.
        :return: Tuple containing the block name, block type, and block deadlines.
        :raises QoalaParseError: If the header is not in the correct format. See the class description for the
        correct format.
        """
        # return (block name, block type, block deadline)
        if not line.startswith("^"):
            raise QoalaParseError("Block header must start with '^'.")

        if line.count("{") != 1 or line.count("}") != 1:
            raise QoalaParseError(
                "Block header must have a single '{' and a single '}'."
            )

        header_parts = [x.strip() for x in line.split("{")]

        name = header_parts[0][1:].strip()  # trim '^' at start
        if not is_valid_name(name):
            raise QoalaParseError(f"Value {name} is not a valid block name.")

        close_brace = header_parts[1].find("}")
        # Since we already checked that there is only one '{' and '}' in the header,
        # close_brace == -1 means '}' occured before '{'
        if close_brace == -1:
            raise QoalaParseError("'}' must occur after '{' in block header.")

        annotations_str = header_parts[1][:close_brace]
        if header_parts[1][close_brace + 1 :] != ":":
            raise QoalaParseError("Block header must end with ':'.")
        typ, deadline = self._parse_block_annotations(annotations_str)
        return name, typ, deadline

    def parse_block(self, text: str) -> hl.BasicBlock:
        """
        Parses a single block of the Qoala program. The block format is given in the class description.

        :param text: Text to parse.
        :return: Parsed block.
        """
        lines = [line.strip() for line in text.split("\n")]
        lines = [line for line in lines if len(line) > 0]
        name, typ, deadline = self._parse_block_header(lines[0])
        instr_lines = lines[1:]
        instrs = IqoalaInstrParser(
            "\n".join(instr_lines), self._defined_vectors
        ).parse()

        return hl.BasicBlock(name, typ, instrs, deadline)

    def parse(self) -> List[hl.BasicBlock]:
        """
        Primary method of the class. Parses all the blocks of the Qoala program.

        :return: List of parsed blocks.
        """
        block_texts = self.get_block_texts()
        return [self.parse_block(text) for text in block_texts]


class LocalRoutineParser:
    """
    This class parses all subroutines in a Qoala program. The subroutine is given in the following format:

    SUBROUTINE <subroutine name>
        params: <param 1>, <param 2>, ...
        returns: <return 1>, <return 2>, ...
        uses: <used qubit id 1>, <used qubit id 2>, ...
        keeps: <kept qubit id 1>, <kept qubit id 2>, ...
        request: <request name 1>, <request name 2>, ...
      NETQASM_START
        <netqasm code>
      NETQASM_END

    The metadata lines must be in the given order. NetQasm code is parsed into NetQasm's Subroutine object using
    its own parser. Subroutine name, parameters, return values, request names must be valid variable names. Values
    for params, returns, uses, keeps, request are optional.

    :param text: Text of all subroutines in a Qoala program to parse.
    :param flavour: Flavour of the Qoala program. It is used to parse the NetQasm code.
    """

    def __init__(self, text: str, flavour: Optional[Flavour] = None) -> None:
        self._text = text
        lines = [line.strip() for line in text.split("\n")]
        self._lines = [line for line in lines if len(line) > 0]
        self._lineno: int = 0
        if flavour is None:
            flavour = VanillaFlavour()
        self._flavour = flavour

    def _next_line(self) -> None:
        self._lineno += 1

    def _read_line(self) -> str:
        """
        Reads the next non-empty line in the text.

        :return: The next non-empty line in the text.
        :raises EndOfTextException: If the end of the text is reached unexpectedly.
        """
        while True:
            if self._lineno >= len(self._lines):
                raise EndOfTextException
            line = self._lines[self._lineno]
            self._next_line()
            if len(line) > 0:
                return line
            # if no non-empty line, will always break on EndOfLineException

    def _parse_subrt_meta_line(self, key: str, line: str) -> List[str]:
        """
        Parses a single line of the subroutine's metadata.

        :param key: The key of the subroutine's metadata line. For example, "params" or "returns".
        :param line: The line to parse.
        :return: List of comma-separated values in the line.
        :raises QoalaParseError: If line does not have a single colon, or if the line does not
        start with the given key.
        """
        if line.count(":") != 1:
            raise QoalaParseError("SubRoutine Meta lines must have a single colon.")
        split = line.split(":")

        if split[0] != key:
            raise QoalaParseError(
                f"SubRoutine Meta line expected to start with {key}, but found {split[0]}."
            )

        if len(split) == 1:
            return []
        if len(split[1]) == 0:
            return []
        values = split[1].split(",")
        return [v.strip() for v in values]

    def _parse_subrt_meta_line_with_vecs(
        self, key: str, line: str
    ) -> List[Union[str, IqoalaVector]]:
        """
        Parses a single line of the subroutine's metadata where the values can be vectors. It is used for the
        "returns" line.

        :param key: The key of the subroutine's metadata line.
        :param line: The line to parse.
        :return: List of comma-separated values in the line.
        :raises QoalaParseError: If the line is not in the given format, or if the key of the line does not match
        with the given key, or if the vectors are not in the correct format, or the variable names are not valid.
        """
        if line.count(":") != 1:
            raise QoalaParseError("SubRoutine Meta lines must have a single colon.")
        split = line.split(":")

        if split[0] != key:
            raise QoalaParseError(
                f"SubRoutine Meta line expected to start with {key}, but found {split[0]}."
            )
        if len(split) == 1:
            return []
        if len(split[1]) == 0:
            return []
        values_str = split[1].split(",")
        values_str = [v.strip() for v in values_str]
        values: List[Union[str, IqoalaVector]] = []
        for v in values_str:
            if "<" in v:
                if v.startswith("<"):
                    raise QoalaParseError("Iqoala vector must start with a name.")
                if not v.endswith(">"):
                    raise QoalaParseError("Iqoala vector must end with a '>'.")
                if v.count("<") != 1 or v.count(">") != 1:
                    raise QoalaParseError(
                        "Iqoala vector must have a single '<' and a single '>'."
                    )
                vec_split = v.split("<")
                vec_name = vec_split[0]
                if not is_valid_name(vec_name):
                    raise QoalaParseError(
                        f"Value {vec_name} is not a valid variable name."
                    )
                vec_size_str = vec_split[1][:-1].strip()  # strip last ">"
                vec_size: IqoalaValue
                if vec_size_str.startswith("{") and vec_size_str.endswith("}"):
                    vec_size_str = vec_size_str.strip("{}").strip()
                    if not is_valid_name(vec_size_str):
                        raise QoalaParseError(
                            f"Value {vec_size_str} is not a valid name for a template. "
                        )

                    vec_size = Template(vec_size_str)
                else:
                    try:
                        vec_size = int(vec_size_str)
                    except ValueError:
                        raise QoalaParseError(
                            "An integer or a template(using '{' and '{') must be provided "
                            f"as the size of an Iqoala vector {vec_name}."
                        )
                values.append(IqoalaVector(vec_name, vec_size))
            else:
                if not is_valid_name(v):
                    raise QoalaParseError(f"Value {v} is not a valid variable name.")
                values.append(v)
        return values

    def _parse_subroutine(self) -> LocalRoutine:
        """
        Parses a single subroutine in the Qoala program. The subroutine format is given in the class description.

        :return: Parsed subroutine.
        :raises QoalaParseError: If the subroutine is not in the correct format. See the class description for
        the correct format.
        :raises EndOfTextException: If the end of the text is reached unexpectedly.
        """
        name_line = self._read_line()
        if not name_line.startswith("SUBROUTINE "):
            raise QoalaParseError("SubRoutine Meta must start with 'SUBROUTINE'.")
        name = name_line[len("SUBROUTINE") + 1 :].strip()
        if not is_valid_name(name):
            raise QoalaParseError(f"Value {name} is not a valid SubRoutine name.")
        params_line = self._parse_subrt_meta_line("params", self._read_line())
        for param in params_line:
            if not is_valid_name(param):
                raise QoalaParseError(
                    f"SubRoutine {name}: value {param} is not a valid name for a parameter."
                )
        # TODO: use params line?

        return_vars = self._parse_subrt_meta_line_with_vecs(
            "returns", self._read_line()
        )
        assert all(" " not in v for v in return_vars if isinstance(v, str))

        uses_line = self._parse_subrt_meta_line("uses", self._read_line())
        try:
            uses = [int(u) for u in uses_line]
        except ValueError:
            raise QoalaParseError(
                f"SubRoutine {name}: 'uses' line values must be a comma separated list of integers."
            )
        keeps_line = self._parse_subrt_meta_line("keeps", self._read_line())
        try:
            keeps = [int(k) for k in keeps_line]
        except ValueError:
            raise QoalaParseError(
                f"SubRoutine {name}: 'keeps' line values must be a comma separated list of integers."
            )
        metadata = RoutineMetadata(qubit_use=uses, qubit_keep=keeps)

        request_line = self._parse_subrt_meta_line("request", self._read_line())
        if len(request_line) > 1:
            raise QoalaParseError(
                "SubRoutine request can have have at most one request."
            )
        request_name = None if len(request_line) == 0 else request_line[0]
        if request_name is not None and not is_valid_name(request_name):
            raise QoalaParseError(
                f"SubRoutine {name}: value {request_name} is not a valid name for a request."
            )

        start_line = self._read_line()
        if start_line != "NETQASM_START":
            raise QoalaParseError("SubRoutine must start with 'NETQASM_START'.")
        subrt_lines = []
        while True:
            try:
                line = self._read_line()
            except EndOfTextException:
                raise QoalaParseError("SubRoutine must end with 'NETQASM_END'.")
            if line == "NETQASM_END":
                break
            subrt_lines.append(line)
        subrt_text = "\n".join(subrt_lines)

        subrt = parse_text_subroutine(subrt_text, flavour=self._flavour)

        # Check that all templates are declared as params to the subroutine
        if any(arg not in params_line for arg in subrt.arguments):
            raise QoalaParseError(
                "All SubRoutine arguments must be declared in 'params'."
            )
        return LocalRoutine(name, subrt, return_vars, metadata, request_name)

    def parse(self) -> Dict[str, LocalRoutine]:
        """
        Primary method of the class. Parses all the subroutines in the Qoala program.

        :return: Dictionary of subroutine names and their corresponding LocalRoutine objects.
        :raises QoalaParseError: If the subroutine is not in the correct format. See the class description for
        the correct format.
        """
        subroutines: Dict[str, LocalRoutine] = {}
        try:
            while True:
                try:
                    subrt = self._parse_subroutine()
                    subroutines[subrt.name] = subrt
                except AssertionError:
                    raise QoalaParseError
        except EndOfTextException:
            return subroutines


class RequestRoutineParser:
    """
    This class parses all request routines in a Qoala program. The request routine is given in the following
    format:

    REQUEST <req name>
      callback_type: <callback type>
      callback: <callback name>
      return_vars: <return var 1>, <return var 2>, ...
      remote_id: <remote id>
      epr_socket_id: <epr socket id>
      num_pairs: <num pairs>
      virt_ids: <virt id mapping>
      timeout: <timeout>
      fidelity: <fidelity>
      typ: <epr type>
      role: <epr role>

    The metadata lines must be in the given order. callback_type and callback are optional. But if callback is
    specified, then callback_type must also be specified. Other lines are required.
    req_name, callback_name and variable names in return_vars must be valid variable names.
    Callback type must be one of the following: 'sequential', 'wait_all' (case-insensitive).
    virt_ids must follow the format given in its description. typ must be one of the following:
    create_keep, measure_directly, or remote_state_prep (case-insensitive). role must be one of the following:
    create or keep(case-insensitive). remote_id, epr_socket_id, num_pairs must be integers. timeout and fidelity
    must be floats. Fidelity also needs to be between 0 and 1.

    :param text: Text of all request routines in a Qoala program to parse.
    """

    def __init__(self, text: str) -> None:
        self._text = text
        lines = [line.strip() for line in text.split("\n")]
        self._lines = [line for line in lines if len(line) > 0]
        self._lineno: int = 0

    def _next_line(self) -> None:
        self._lineno += 1

    def _read_line(self) -> str:
        """
        Reads the next non-empty line in the text.

        :return: The next non-empty line in the text.
        :raises EndOfTextException: If the end of the text is reached unexpectedly.
        """
        while True:
            if self._lineno >= len(self._lines):
                raise EndOfTextException
            line = self._lines[self._lineno]
            self._next_line()
            if len(line) > 0:
                return line
            # if no non-empty line, will always break on EndOfLineException

    def _parse_request_line(self, key: str, line: str) -> List[str]:
        """
        Parses a single line of the request routine's metadata.

        :param key: The key of the request routine's metadata line. For example, "callback_type" or "callback".
        :param line: The line to parse.
        :return: List of comma-separated values in the line.
        :raises QoalaParseError: If line does not have a single colon, or if the line does not
        start with the given key.
        """
        if line.count(":") != 1:
            raise QoalaParseError("SubRoutine Meta lines must have a single colon.")
        split = line.split(":")

        if split[0] != key:
            raise QoalaParseError(
                f"SubRoutine Meta line expected to start with {key}, but found {split[0]}."
            )
        if len(split) == 1:
            return []
        if len(split[1]) == 0:
            return []
        values = split[1].split(",")
        return [v.strip() for v in values]

    def _parse_request_line_with_vecs(
        self, key: str, line: str
    ) -> List[Union[str, IqoalaVector]]:
        """
        Parses a single line of the request routine's metadata where the values can be vectors. It is used for the
        "return_vars" line.

        :param key: The key of the request routine's metadata line.
        :param line: The line to parse.
        :return: List of comma-separated values in the line.
        :raises QoalaParseError: If the line is not in the given format, or if the key of the line does not match
        with the given key, or if the vectors are not in the correct format, or the variable names are not valid.
        """
        if line.count(":") != 1:
            raise QoalaParseError("SubRoutine Meta lines must have a single colon.")
        split = line.split(":")

        if split[0] != key:
            raise QoalaParseError(
                f"SubRoutine Meta line expected to start with {key}, but found {split[0]}."
            )
        if len(split) == 1:
            return []
        if len(split[1]) == 0:
            return []
        values_str = split[1].split(",")
        values_str = [v.strip() for v in values_str]
        values: List[Union[str, IqoalaVector]] = []
        for v in values_str:
            if "<" in v:
                if v.startswith("<"):
                    raise QoalaParseError("Iqoala vector must start with a name.")
                if not v.endswith(">"):
                    raise QoalaParseError("Iqoala vector must end with a '>'.")
                if v.count("<") != 1 or v.count(">") != 1:
                    raise QoalaParseError(
                        "Iqoala vector must have a single '<' and a single '>'."
                    )
                vec_split = v.split("<")
                vec_name = vec_split[0]
                if not is_valid_name(vec_name):
                    raise QoalaParseError(
                        f"Value {vec_name} is not a valid variable name."
                    )
                vec_size_str = vec_split[1][:-1].strip()  # strip last ">"
                vec_size: IqoalaValue
                if vec_size_str.startswith("{") and vec_size_str.endswith("}"):
                    vec_size_str = vec_size_str.strip("{}").strip()
                    if not is_valid_name(vec_size_str):
                        raise QoalaParseError(
                            f"Value {vec_size_str} is not a valid name for a template. "
                        )

                    vec_size = Template(vec_size_str)
                else:
                    try:
                        vec_size = int(vec_size_str)
                    except ValueError:
                        raise QoalaParseError(
                            "An integer or a template(using '{' and '{') must be provided "
                            f"as the size of an Iqoala vector {vec_name}."
                        )
                values.append(IqoalaVector(vec_name, vec_size))
            else:
                if not is_valid_name(v):
                    raise QoalaParseError(f"Value {v} is not a valid variable name.")
                values.append(v)
        return values

    def _parse_single_int_value(self, key: str, line: str) -> Union[int, Template]:
        """
        Parses a single line of the request routine's metadata where the value is an integer or a template.
        Template values must be in the format {<template name>}. For example, {n}. The template name must be a valid
        variable name.

        :param key: The key of the request routine's metadata line.
        :param line: The line to parse.
        :return: The parsed value.
        :raises QoalaParseError: If the value is not in the correct format.
        """
        strings = self._parse_request_line(key, line)
        if len(strings) != 1:
            raise QoalaParseError(
                f"One single integer or a template value is allowed in Request Routine Meta line for {key}."
            )
        value = strings[0]
        if value.startswith("{") and value.endswith("}"):
            value = value.strip("{}").strip()
            if not is_valid_name(value):
                raise QoalaParseError(
                    f"Value {value} is not a valid name for a template."
                )
            return Template(value)
        try:
            return int(value)
        except ValueError:
            raise QoalaParseError(f"Value for {key} must be an integer or a template.")

    def _parse_optional_str_value(self, key: str, line: str) -> Optional[str]:
        strings = self._parse_request_line(key, line)
        if len(strings) == 0:
            return None
        if len(strings) != 1:
            raise QoalaParseError(
                f"At most one value is allowed in Request Routine Meta line for {key}."
            )
        return strings[0]

    def _parse_single_float_value(self, key: str, line: str) -> Union[float, Template]:
        """
        Parses a single line of the request routine's metadata where the value is an float or a template.
        Template values must be in the format {<template name>}. For example, {n}. The template name must be a valid
        variable name.

        :param key: The key of the request routine's metadata line.
        :param line: The line to parse.
        :return: The parsed value.
        :raises QoalaParseError: If the value is not in the correct format.
        """
        strings = self._parse_request_line(key, line)
        if len(strings) != 1:
            raise QoalaParseError(
                f"One single floating point value is allowed in Request Routine Meta line for {key}."
            )
        value = strings[0]
        if value.startswith("{") and value.endswith("}"):
            value = value.strip("{}").strip()
            if not is_valid_name(value):
                raise QoalaParseError(
                    f"Value {value} is not a valid name for a template."
                )
            return Template(value)
        try:
            return float(value)
        except ValueError:
            raise QoalaParseError(f"Value for {key} must be a float or a template.")

    def _parse_epr_create_role_value(self, key: str, line: str) -> EprRole:
        """
        Parses EPR role line of the request routine's metadata.

        :param key: The key of the request routine's metadata line.
        :param line: The line to parse.
        :return: The parsed value.
        :raises QoalaParseError: If the value is not one of the following: 'CREATE' or 'RECEIVE' (case-insensitive).
        """
        strings = self._parse_request_line(key, line)
        if len(strings) != 1:
            raise QoalaParseError(
                "There must be a single value in Request Routine Meta line for EPR Role."
            )
        try:
            return EprRole[strings[0].upper()]
        except KeyError:
            raise QoalaParseError(
                "Value in Request Routine Meta line for EPR Role must be either"
                " 'CREATE' or 'RECEIVE' "
                "(case insensitive)."
            )

    def _parse_epr_create_type_value(self, key: str, line: str) -> EprType:
        """
        Parses EPR type line of the request routine's metadata.

        :param key: The key of the request routine's metadata line.
        :param line: The line to parse.
        :return: The parsed value.
        :raises QoalaParseError: If the value is not one of the following: 'CREATE_KEEP', 'MEASURE_DIRECTLY', or
        'REMOTE_STATE_PREP' (case-insensitive).
        """
        strings = self._parse_request_line(key, line)
        if len(strings) != 1:
            raise QoalaParseError(
                "There must be a single value in Request Routine Meta line for EPR Type."
            )
        try:
            return EprType[strings[0].upper()]
        except KeyError:
            raise QoalaParseError(
                "Value in Request Routine Meta line for EPR Type must be one of the following:"
                " 'CREATE_KEEP', 'MEASURE_DIRECTLY', 'REMOTE_STATE_PREP' "
                "(case insensitive)."
            )

    def _parse_virt_ids(self, key: str, line: str) -> RequestVirtIdMapping:
        """
        Parses virt_ids line of the request routine's metadata. See the RequestVirtIdMapping class for the format.

        :param key: The key of the request routine's metadata line.
        :param line: The line to parse.
        :return: The parsed value.
        :raises QoalaParseError: If the value is not in the correct format.
        """
        if line.count(":") != 1:
            raise QoalaParseError("SubRoutine Meta lines must have a single colon.")
        split = line.split(":")

        if split[0] != key:
            raise QoalaParseError(
                f"SubRoutine Meta line expected to start with {key}, but found {split[0]}."
            )
        return RequestVirtIdMapping.from_str(split[1].strip())

    def _parse_callback_type(self, key: str, line: str) -> Optional[CallbackType]:
        """
        Parses Callback type line of the request routine's metadata.

        :param key: The key of the request routine's metadata line.
        :param line: The line to parse.
        :return: The parsed value.
        :raises QoalaParseError: If the value is not one of the following: 'SEQUENTIAL' or
        'WAIT_ALL' (case-insensitive).
        """
        values = self._parse_request_line(key, line)
        if len(values) == 0:
            return None
        if len(values) != 1:
            raise QoalaParseError(
                "There must be a single value in Request Routine Meta line for Callback Type."
            )
        try:
            return CallbackType[values[0].upper()]
        except KeyError:
            raise QoalaParseError(
                "If specified, value in Request Routine Meta line for Callback Type "
                "must be one of the following:"
                " 'SEQUENTIAL', 'WAIT_ALL'"
                "(case insensitive)."
            )

    def _parse_request(self) -> RequestRoutine:
        """
        Parses a single request routine in the Qoala program. The subroutine format is given in the class description.

        :return: Parsed subroutine.
        :raises QoalaParseError: If the request routine is not in the correct format. See the class description for
        the correct format.
        :raises EndOfTextException: If the end of the text is reached unexpectedly.
        """
        name_line = self._read_line()
        if not name_line.startswith("REQUEST "):
            raise QoalaParseError("Request Routine Meta must start with 'REQUEST'.")
        name = name_line[len("REQUEST") + 1 :].strip()
        if not is_valid_name(name):
            raise QoalaParseError(f"Value {name} is not a valid Request Routine name.")

        callback_type = self._parse_callback_type("callback_type", self._read_line())

        callback = self._parse_optional_str_value("callback", self._read_line())
        if callback is not None and not is_valid_name(callback):
            raise QoalaParseError(
                f"Request {name}: Value {callback} is not a valid callback name."
            )

        if callback is not None and callback_type is None:
            raise QoalaParseError(
                "If callback is specified, callback_type must also be specified."
            )
        # If both callback and callback_type are not specified, set callback_type to WAIT_ALL
        if callback_type is None:
            callback_type = CallbackType.WAIT_ALL

        return_vars = self._parse_request_line_with_vecs(
            "return_vars", self._read_line()
        )
        assert all(" " not in v for v in return_vars if isinstance(v, str))

        remote_id = self._parse_single_int_value("remote_id", self._read_line())
        epr_socket_id = self._parse_single_int_value("epr_socket_id", self._read_line())
        num_pairs = self._parse_single_int_value("num_pairs", self._read_line())
        virt_ids = self._parse_virt_ids("virt_ids", self._read_line())
        timeout = self._parse_single_int_value("timeout", self._read_line())
        fidelity = self._parse_single_float_value("fidelity", self._read_line())
        typ = self._parse_epr_create_type_value("typ", self._read_line())
        role = self._parse_epr_create_role_value("role", self._read_line())

        request = QoalaRequest(
            name=name,
            remote_id=remote_id,
            epr_socket_id=epr_socket_id,
            num_pairs=num_pairs,
            virt_ids=virt_ids,
            timeout=timeout,
            fidelity=fidelity,
            typ=typ,
            role=role,
        )
        return RequestRoutine(name, request, return_vars, callback_type, callback)

    def parse(self) -> Dict[str, RequestRoutine]:
        """
        Primary method of the class. Parses all the request routines in the Qoala program.

        :return: Dictionary of subroutine names and their corresponding LocalRoutine objects.
        :raises QoalaParseError: If the request routine is not in the correct format. See the class description for
        the correct format.
        """
        requests: Dict[str, RequestRoutine] = {}
        try:
            while True:
                request = self._parse_request()
                requests[request.name] = request
        except EndOfTextException:
            return requests


class QoalaParser:
    """
    Parses whole Qoala program by using the other parsers in this module. There are two ways to pass text to the parser.
    The first way is to pass the whole text of the Qoala program to the constructor. The second way is to pass the
    text of each section of the Qoala program to the constructor separately. These sections are meta, host, subroutines,
    and requests. If the whole text is passed to the constructor, then the text of each section must not be passed
    separately. If the text of each section is passed separately, then the whole text must not be passed to the
    constructor.

    :param text: Text of the whole Qoala program.
    :param meta_text: Text of the meta section of the Qoala program.
    :param host_text: Text of the host section of the Qoala program.
    :param subrt_text: Text of the subroutines section of the Qoala program.
    :param req_text: Text of the requests section of the Qoala program.
    :param flavour: NetQasm Flavour of the Qoala program. Flavour information is required to parse the subroutines
    section.
    :raises QoalaParseError: If text and any of meta_text, host_text, subrt_text, req_text are provided at the same
    time, or if text is not provided and any of meta_text, host_text, subrt_text, req_text are not provided.
    """

    def __init__(
        self,
        text: Optional[str] = None,
        meta_text: Optional[str] = None,
        host_text: Optional[str] = None,
        subrt_text: Optional[str] = None,
        req_text: Optional[str] = None,
        flavour: Optional[Flavour] = None,
    ) -> None:
        if text is not None:
            if any(t is not None for t in (meta_text, host_text, subrt_text, req_text)):
                raise QoalaParseError(
                    "If text is provided to QoalaParser none of meta_text, "
                    "host_text, subrt_text, req_text must be provided."
                )
            meta_text, host_text, subrt_text, req_text = self._split_text(text)
        else:
            if (
                meta_text is None
                or host_text is None
                or subrt_text is None
                or req_text is None
            ):
                raise QoalaParseError(
                    "If text is not provided to QoalaParser, then all of meta_text, "
                    "host_text, subrt_text, req_text must be provided."
                )

        self._meta_text = meta_text
        self._host_text = host_text
        self._subrt_text = subrt_text
        self._req_text = req_text
        self._meta_parser = IqoalaMetaParser(meta_text)
        self._host_parser = HostCodeParser(host_text)
        self._subrt_parser = LocalRoutineParser(subrt_text, flavour)
        self._req_parser = RequestRoutineParser(req_text)

    def _split_text(self, text: str) -> Tuple[str, str, str, str]:
        """
        Splits the text of the whole Qoala program into its sections.

        :param text: Text of the whole Qoala program.
        :return: Tuple of meta, host, subroutines, and requests sections of the Qoala program.
        """
        lines = [line.strip() for line in text.split("\n")]
        meta_end_line: int
        first_subrt_line: Optional[int] = None
        first_req_line: Optional[int] = None
        for i, line in enumerate(lines):
            if "META_END" in line:
                meta_end_line = i
                break
        for i, line in enumerate(lines):
            if "SUBROUTINE" in line:
                first_subrt_line = i
                break
        for i, line in enumerate(lines):
            if "REQUEST" in line:
                first_req_line = i
                break

        meta_text = "\n".join(lines[0 : meta_end_line + 1])
        host_end_line: Optional[int] = None
        if first_subrt_line is None and first_req_line is None:
            # no subroutines and no requests
            subrt_text = ""
            req_text = ""
        elif first_subrt_line is not None and first_req_line is None:
            # subroutines but no requests
            subrt_text = "\n".join(lines[first_subrt_line:])
            req_text = ""
            host_end_line = first_subrt_line
        elif first_subrt_line is None and first_req_line is not None:
            # no subroutines but only requests
            subrt_text = ""
            req_text = "\n".join(lines[first_req_line:])
            host_end_line = first_req_line
        else:
            # subroutines and requests
            subrt_text = "\n".join(lines[first_subrt_line:first_req_line])
            req_text = "\n".join(lines[first_req_line:])
            host_end_line = first_subrt_line
        if host_end_line is not None:
            host_text = "\n".join(lines[meta_end_line + 1 : host_end_line])
        else:
            host_text = "\n".join(lines[meta_end_line + 1 :])

        return meta_text, host_text, subrt_text, req_text

    def parse(self) -> QoalaProgram:
        """
        Primary method of the class. Parses the whole Qoala program by calling respective parsers for each section.

        :return: Parsed Qoala program.
        :raises QoalaParseError: If the name of the subroutines or request routines in the host instructions are not in
        the program.
        """
        blocks = self._host_parser.parse()
        subroutines = self._subrt_parser.parse()
        requests = self._req_parser.parse()
        meta = self._meta_parser.parse()

        # Check that all references to subroutines (in RunSubroutineOp instructions)
        # and to requests (in RunRequestOp instructions) are valid.
        for block in blocks:
            for instr in block.instructions:
                if isinstance(instr, hl.RunSubroutineOp):
                    subrt_name = instr.subroutine
                    if subrt_name not in subroutines:
                        raise QoalaParseError(
                            f"Block {block.name} references unknown subroutine {subrt_name}"
                        )
                elif isinstance(instr, hl.RunRequestOp):
                    req_name = instr.req_routine
                    if req_name not in requests:
                        raise QoalaParseError(
                            f"Block {block.name} references unknown request routine {req_name}"
                        )

        return QoalaProgram(meta, blocks, subroutines, requests)
