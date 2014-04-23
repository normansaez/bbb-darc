# Python stubs generated by omniidl from bbbserver.idl

import omniORB, _omnipy
from omniORB import CORBA, PortableServer
_0_CORBA = CORBA

_omnipy.checkVersion(3,0, __file__)


#
# Start of module "BBBServer"
#
__name__ = "BBBServer"
_0_BBBServer = omniORB.openModule("BBBServer", r"bbbserver.idl")
_0_BBBServer__POA = omniORB.openModule("BBBServer__POA", r"bbbserver.idl")


# typedef ... list
class list:
    _NP_RepositoryId = "IDL:BBBServer/list:1.0"
    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")
_0_BBBServer.list = list
_0_BBBServer._d_list  = (omniORB.tcInternal.tv_sequence, (omniORB.tcInternal.tv_string,0), 0)
_0_BBBServer._ad_list = (omniORB.tcInternal.tv_alias, list._NP_RepositoryId, "list", (omniORB.tcInternal.tv_sequence, (omniORB.tcInternal.tv_string,0), 0))
_0_BBBServer._tc_list = omniORB.tcInternal.createTypeCode(_0_BBBServer._ad_list)
omniORB.registerType(list._NP_RepositoryId, _0_BBBServer._ad_list, _0_BBBServer._tc_list)
del list

# interface Server
_0_BBBServer._d_Server = (omniORB.tcInternal.tv_objref, "IDL:BBBServer/Server:1.0", "Server")
omniORB.typeMapping["IDL:BBBServer/Server:1.0"] = _0_BBBServer._d_Server
_0_BBBServer.Server = omniORB.newEmptyClass()
class Server :
    _NP_RepositoryId = _0_BBBServer._d_Server[1]

    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")

    _nil = CORBA.Object._nil


_0_BBBServer.Server = Server
_0_BBBServer._tc_Server = omniORB.tcInternal.createTypeCode(_0_BBBServer._d_Server)
omniORB.registerType(Server._NP_RepositoryId, _0_BBBServer._d_Server, _0_BBBServer._tc_Server)

# Server operations and attributes
Server._d_led_on = (((omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), omniORB.tcInternal.tv_boolean, omniORB.tcInternal.tv_float, omniORB.tcInternal.tv_long), ((omniORB.tcInternal.tv_string,0), ), None)
Server._d_led_off = (((omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), omniORB.tcInternal.tv_boolean, omniORB.tcInternal.tv_float, omniORB.tcInternal.tv_long), ((omniORB.tcInternal.tv_string,0), ), None)
Server._d_motor_move = (((omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long), (omniORB.tcInternal.tv_long, ), None)
Server._d_motor_move_skip_sensor = (((omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long), (omniORB.tcInternal.tv_long, ), None)
Server._d_set_to_zero = (((omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long, omniORB.tcInternal.tv_long), (omniORB.tcInternal.tv_long, ), None)
Server._d_flush_all_leds = ((), (omniORB.tcInternal.tv_long, ), None)
Server._d_get_motor_cur_pos = (((omniORB.tcInternal.tv_string,0), ), (omniORB.tcInternal.tv_long, ), None)
Server._d_get_motor_cmd_pos = (((omniORB.tcInternal.tv_string,0), ), (omniORB.tcInternal.tv_long, ), None)
Server._d_get_stars_status_keys = ((), (omniORB.typeMapping["IDL:BBBServer/list:1.0"], ), None)
Server._d_get_stars_status_value = (((omniORB.tcInternal.tv_string,0), ), (omniORB.typeMapping["IDL:BBBServer/list:1.0"], ), None)

# Server object reference
class _objref_Server (CORBA.Object):
    _NP_RepositoryId = Server._NP_RepositoryId

    def __init__(self):
        CORBA.Object.__init__(self)

    def led_on(self, *args):
        return _omnipy.invoke(self, "led_on", _0_BBBServer.Server._d_led_on, args)

    def led_off(self, *args):
        return _omnipy.invoke(self, "led_off", _0_BBBServer.Server._d_led_off, args)

    def motor_move(self, *args):
        return _omnipy.invoke(self, "motor_move", _0_BBBServer.Server._d_motor_move, args)

    def motor_move_skip_sensor(self, *args):
        return _omnipy.invoke(self, "motor_move_skip_sensor", _0_BBBServer.Server._d_motor_move_skip_sensor, args)

    def set_to_zero(self, *args):
        return _omnipy.invoke(self, "set_to_zero", _0_BBBServer.Server._d_set_to_zero, args)

    def flush_all_leds(self, *args):
        return _omnipy.invoke(self, "flush_all_leds", _0_BBBServer.Server._d_flush_all_leds, args)

    def get_motor_cur_pos(self, *args):
        return _omnipy.invoke(self, "get_motor_cur_pos", _0_BBBServer.Server._d_get_motor_cur_pos, args)

    def get_motor_cmd_pos(self, *args):
        return _omnipy.invoke(self, "get_motor_cmd_pos", _0_BBBServer.Server._d_get_motor_cmd_pos, args)

    def get_stars_status_keys(self, *args):
        return _omnipy.invoke(self, "get_stars_status_keys", _0_BBBServer.Server._d_get_stars_status_keys, args)

    def get_stars_status_value(self, *args):
        return _omnipy.invoke(self, "get_stars_status_value", _0_BBBServer.Server._d_get_stars_status_value, args)

    __methods__ = ["led_on", "led_off", "motor_move", "motor_move_skip_sensor", "set_to_zero", "flush_all_leds", "get_motor_cur_pos", "get_motor_cmd_pos", "get_stars_status_keys", "get_stars_status_value"] + CORBA.Object.__methods__

omniORB.registerObjref(Server._NP_RepositoryId, _objref_Server)
_0_BBBServer._objref_Server = _objref_Server
del Server, _objref_Server

# Server skeleton
__name__ = "BBBServer__POA"
class Server (PortableServer.Servant):
    _NP_RepositoryId = _0_BBBServer.Server._NP_RepositoryId


    _omni_op_d = {"led_on": _0_BBBServer.Server._d_led_on, "led_off": _0_BBBServer.Server._d_led_off, "motor_move": _0_BBBServer.Server._d_motor_move, "motor_move_skip_sensor": _0_BBBServer.Server._d_motor_move_skip_sensor, "set_to_zero": _0_BBBServer.Server._d_set_to_zero, "flush_all_leds": _0_BBBServer.Server._d_flush_all_leds, "get_motor_cur_pos": _0_BBBServer.Server._d_get_motor_cur_pos, "get_motor_cmd_pos": _0_BBBServer.Server._d_get_motor_cmd_pos, "get_stars_status_keys": _0_BBBServer.Server._d_get_stars_status_keys, "get_stars_status_value": _0_BBBServer.Server._d_get_stars_status_value}

Server._omni_skeleton = Server
_0_BBBServer__POA.Server = Server
omniORB.registerSkeleton(Server._NP_RepositoryId, Server)
del Server
__name__ = "BBBServer"

#
# End of module "BBBServer"
#
__name__ = "bbbserver_idl"

_exported_modules = ( "BBBServer", )

# The end.
