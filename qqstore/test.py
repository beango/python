#-*- coding: UTF-8 -*-
#!/usr/bin/env python  
#coding:utf-8  
import sys,binascii
import protobuf
reload(sys)
sys.setdefaultencoding('utf-8')


#print binascii.unhexlify("00 17 04 47 00 00 00 00 0A 0F 39 31 35 33 30 30")#"00 17 04 47 00 00 00 00 0A 0F 39 31 35 33 30 30"
b = bytearray(b'\x00\x1B\x04\x34\x00\x00\x00\x00\x0A\x11\x32\x34\x39\x37\x37\x31')
print repr(str(b))

'''
\x00\x1B\x04\x34\x00\x00\x00\x00\x0A\x11\x32\x34\x39\x37\x37\x31
4季，61H，20级=26
4季，46H，20级=20
4季，32H，20级=14
3季，25H，7级 =10
2季，24H，10级=11
var _loc_9:* = NaN;
var _loc_15:* = 0;
var _loc_16:* = 0;
if (param1 == 0)
{
    return 0;
}
if (param3 == 7)
{
    return 7;
}
var _loc_6:* = getCropByID(param1.toString());
if (getCropByID(param1.toString()) == null)
{
    return 0;
}
var _loc_7:* = _loc_6["cropGrow"];      "21600,43200,64800,86400,108000,2000000000"
if (_loc_6["cropGrow"] == "")
{
    return 0;
}
var _loc_8:* = _loc_7.split(",");   "21600,43200,64800,86400,108000,2000000000"
if (CommonData.serverTime)
{
    _loc_9 = CommonData.serverTime;
}
else
{
    _loc_9 = StartupData.serverTime;
}
var _loc_10:* = _loc_9;             2012/12/31
var _loc_11:* = _loc_9 - param2;    当前时间-种植时间
var _loc_12:* = _loc_8.length;      6
var _loc_13:* = 0;
var _loc_14:* = _loc_12 - 1;        5
while (_loc_14 >= 0)
{
    
    if (param4 == 3 && _loc_6["isRed"] != "3" || param4 == 2 && _loc_6["isRed"] != "2" && _loc_6["isRed"] != "3")
    {
        if (_loc_14 < _loc_12 - 2)
        {
            _loc_13 = Math.floor(_loc_8[_loc_14] * 0.8) as int;
        }
        else
        {
            _loc_13 = Math.floor(_loc_8[_loc_14] * 0.8) as int;
            _loc_15 = _loc_13 % 600;
            if (_loc_13 > _loc_15)
            {
                _loc_13 = _loc_13 - _loc_15;
            }
        }
    }
    else
    {
        _loc_13 = _loc_8[_loc_14];"2000000000,108000,86400,64800,43200,21600"
    }
    if (_loc_11 >= _loc_13)已经种植时间
    {
        _loc_16 = _loc_14 + 1;
        if (param5 > 0)
        {
            if (_loc_16 < 3)
            {
                return 3;
            }
        }
        return _loc_16;
    }
    _loc_14 = _loc_14 - 1;
}
return 0;
'''