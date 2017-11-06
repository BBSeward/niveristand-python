import os
from niveristand import exceptions as nivsexceptions
from niveristand import internal
from niveristand.datatypes import DataType
from niveristand.datatypes import Double
from niveristand.datatypes import Int32
from NationalInstruments.VeriStand.RealTimeSequenceDefinitionApi import Expression  # noqa: I100
from NationalInstruments.VeriStand.RealTimeSequenceDefinitionApi import LocalDeclaration  # noqa: I100
from NationalInstruments.VeriStand.RealTimeSequenceDefinitionApi import RealTimeSequence  # noqa: I100
from NationalInstruments.VeriStand.Data import DoubleValue  # noqa: I100
from NationalInstruments.VeriStand.Data import I32Value  # noqa: I100
from System.IO import IOException

internal.dummy()
_lv_cnt = 0


def add_local_variable(rt_seq, name, value):
    global _lv_cnt
    if name is None:
        name = ''
    name = 'lv_' + name + '_' + str(_lv_cnt)
    _lv_cnt += 1
    converted_value = _convert_value_to_datavalue(value)
    local_declaration = LocalDeclaration(name, converted_value)
    rt_seq.Variables.LocalVariables.AddLocalVariable(local_declaration)
    return name


def add_assignment(block, dest_name, source_name):
    block.AddStatement(Expression('%s = %s' % (dest_name, source_name)))


def create_real_time_sequence():
    return RealTimeSequence()


def save_real_time_sequence(rtseq, filepath):
    try:
        rtseq.SaveSequence(os.path.join(filepath))
    except(IOException) as e:
        raise IOError(e.Message)


def _convert_value_to_datavalue(nivsvalue):
    if isinstance(nivsvalue, Double):
        return DoubleValue(nivsvalue.value)
    if isinstance(nivsvalue, Int32):
        return I32Value(nivsvalue.value)
    if isinstance(nivsvalue, DataType):
        raise nivsexceptions.VeristandNotImplementedError()
    raise nivsexceptions.UnexpectedError("Unable to convert value for type %s"
                                         % type(nivsvalue))
