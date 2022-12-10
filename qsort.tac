GLOBAL Var name: n value: 5
GLOBAL Array name: a size: 20
GLOBAL Var name: state value: 0
main:
    _T0 = GLOBAL_VAR n
    _T1 = LOAD _T0, 0
    PARAM _T1
    _T2 = CALL initArr
    _T4 = GLOBAL_VAR n
    _T5 = LOAD _T4, 0
    PARAM _T5
    _T6 = CALL isSorted
    _T3 = _T6
    _T7 = 0
    _T8 = GLOBAL_VAR n
    _T9 = LOAD _T8, 0
    _T10 = 1
    _T11 = (_T9 - _T10)
    PARAM _T7
    PARAM _T11
    _T12 = CALL qsort
    _T14 = GLOBAL_VAR n
    _T15 = LOAD _T14, 0
    PARAM _T15
    _T16 = CALL isSorted
    _T13 = _T16
    _T17 = 0
    _T18 = (_T3 == _T17)
    _T19 = 1
    _T20 = (_T13 == _T19)
    _T21 = (_T18 && _T20)
    _T22 = ! _T21
    if (_T22 == 0) branch _L1
    _T23 = 1
    return _T23
_L1:
    _T24 = 0
    return _T24
qsort:
    _T2 = _T0
    _T3 = _T1
    _T5 = GLOBAL_VAR a
    _T6 = (_T0 + _T1)
    _T7 = 2
    _T8 = (_T6 / _T7)
    _T9 = 0
    _T10 = 1
    _T11 = (_T8 * _T10)
    _T9 = (_T9 + _T11)
    _T12 = 4
    _T9 = (_T9 * _T12)
    _T9 = (_T9 + _T5)
    _T13 = LOAD _T9, 0
    _T4 = _T13
    _T15 = 1
    _T14 = _T15
_L2:
    _T16 = (_T2 <= _T3)
    if (_T16 == 0) branch _L4
_L5:
    _T17 = GLOBAL_VAR a
    _T18 = 0
    _T19 = 1
    _T20 = (_T2 * _T19)
    _T18 = (_T18 + _T20)
    _T21 = 4
    _T18 = (_T18 * _T21)
    _T18 = (_T18 + _T17)
    _T22 = LOAD _T18, 0
    _T23 = (_T22 < _T4)
    if (_T23 == 0) branch _L7
    _T24 = 1
    _T25 = (_T2 + _T24)
    _T2 = _T25
_L6:
    branch _L5
_L7:
_L8:
    _T26 = GLOBAL_VAR a
    _T27 = 0
    _T28 = 1
    _T29 = (_T3 * _T28)
    _T27 = (_T27 + _T29)
    _T30 = 4
    _T27 = (_T27 * _T30)
    _T27 = (_T27 + _T26)
    _T31 = LOAD _T27, 0
    _T32 = (_T31 > _T4)
    if (_T32 == 0) branch _L10
    _T33 = 1
    _T34 = (_T3 - _T33)
    _T3 = _T34
_L9:
    branch _L8
_L10:
    _T35 = (_T2 > _T3)
    if (_T35 == 0) branch _L11
    branch _L4
_L11:
    _T37 = GLOBAL_VAR a
    _T38 = 0
    _T39 = 1
    _T40 = (_T2 * _T39)
    _T38 = (_T38 + _T40)
    _T41 = 4
    _T38 = (_T38 * _T41)
    _T38 = (_T38 + _T37)
    _T42 = LOAD _T38, 0
    _T36 = _T42
    _T43 = GLOBAL_VAR a
    _T44 = 0
    _T45 = 1
    _T46 = (_T3 * _T45)
    _T44 = (_T44 + _T46)
    _T47 = 4
    _T44 = (_T44 * _T47)
    _T44 = (_T44 + _T43)
    _T48 = LOAD _T44, 0
    _T49 = GLOBAL_VAR a
    _T50 = 0
    _T51 = 1
    _T52 = (_T2 * _T51)
    _T50 = (_T50 + _T52)
    _T53 = 4
    _T50 = (_T50 * _T53)
    _T50 = (_T50 + _T49)
    _T54 = LOAD _T50, 0
    _T54 = _T48
    STORE _T54, 0(_T50)
    _T55 = GLOBAL_VAR a
    _T56 = 0
    _T57 = 1
    _T58 = (_T3 * _T57)
    _T56 = (_T56 + _T58)
    _T59 = 4
    _T56 = (_T56 * _T59)
    _T56 = (_T56 + _T55)
    _T60 = LOAD _T56, 0
    _T60 = _T36
    STORE _T60, 0(_T56)
    _T61 = 1
    _T62 = (_T2 + _T61)
    _T2 = _T62
    _T63 = 1
    _T64 = (_T3 - _T63)
    _T3 = _T64
_L3:
    branch _L2
_L4:
    _T65 = (_T2 < _T1)
    if (_T65 == 0) branch _L12
    PARAM _T2
    PARAM _T1
    _T66 = CALL qsort
_L12:
    _T67 = (_T3 > _T0)
    if (_T67 == 0) branch _L13
    PARAM _T0
    PARAM _T3
    _T68 = CALL qsort
_L13:
    return
rand:
    _T0 = GLOBAL_VAR state
    _T1 = LOAD _T0, 0
    _T2 = 64013
    _T3 = (_T1 * _T2)
    _T4 = 1531011
    _T5 = (_T3 + _T4)
    _T6 = 32768
    _T7 = (_T5 % _T6)
    _T8 = GLOBAL_VAR state
    _T9 = LOAD _T8, 0
    _T9 = _T7
    _T10 = GLOBAL_VAR state
    STORE _T9, 0(_T10)
    _T11 = GLOBAL_VAR state
    _T12 = LOAD _T11, 0
    _T13 = 1000
    _T14 = (_T12 % _T13)
    return _T14
initArr:
    _T2 = 0
    _T1 = _T2
_L14:
    _T3 = (_T1 < _T0)
    if (_T3 == 0) branch _L16
    _T4 = CALL rand
    _T5 = GLOBAL_VAR a
    _T6 = 0
    _T7 = 1
    _T8 = (_T1 * _T7)
    _T6 = (_T6 + _T8)
    _T9 = 4
    _T6 = (_T6 * _T9)
    _T6 = (_T6 + _T5)
    _T10 = LOAD _T6, 0
    _T10 = _T4
    STORE _T10, 0(_T6)
    _T11 = 1
    _T12 = (_T1 + _T11)
    _T1 = _T12
_L15:
    branch _L14
_L16:
    return
isSorted:
    _T2 = 0
    _T1 = _T2
_L17:
    _T3 = 1
    _T4 = (_T0 - _T3)
    _T5 = (_T1 < _T4)
    if (_T5 == 0) branch _L19
    _T6 = GLOBAL_VAR a
    _T7 = 0
    _T8 = 1
    _T9 = (_T1 * _T8)
    _T7 = (_T7 + _T9)
    _T10 = 4
    _T7 = (_T7 * _T10)
    _T7 = (_T7 + _T6)
    _T11 = LOAD _T7, 0
    _T12 = GLOBAL_VAR a
    _T13 = 1
    _T14 = (_T1 + _T13)
    _T15 = 0
    _T16 = 1
    _T17 = (_T14 * _T16)
    _T15 = (_T15 + _T17)
    _T18 = 4
    _T15 = (_T15 * _T18)
    _T15 = (_T15 + _T12)
    _T19 = LOAD _T15, 0
    _T20 = (_T11 > _T19)
    if (_T20 == 0) branch _L20
    _T21 = 0
    return _T21
_L20:
    _T22 = 1
    _T23 = (_T1 + _T22)
    _T1 = _T23
_L18:
    branch _L17
_L19:
    _T24 = 1
    return _T24
