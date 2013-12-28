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
Server._d_led_on = (((omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0)), ((omniORB.tcInternal.tv_string,0), ), None)
Server._d_led_off = (((omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0)), ((omniORB.tcInternal.tv_string,0), ), None)
Server._d_motor_move = (((omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0)), ((omniORB.tcInternal.tv_string,0), ), None)

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

    __methods__ = ["led_on", "led_off", "motor_move"] + CORBA.Object.__methods__

omniORB.registerObjref(Server._NP_RepositoryId, _objref_Server)
_0_BBBServer._objref_Server = _objref_Server
del Server, _objref_Server

# Server skeleton
__name__ = "BBBServer__POA"
class Server (PortableServer.Servant):
    _NP_RepositoryId = _0_BBBServer.Server._NP_RepositoryId


    _omni_op_d = {"led_on": _0_BBBServer.Server._d_led_on, "led_off": _0_BBBServer.Server._d_led_off, "motor_move": _0_BBBServer.Server._d_motor_move}

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