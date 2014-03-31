#include <Python.h>
#include "c_driver.h"

static char py_move_motor_doc[] = "Moves motor";
static PyObject * 
py_move_motor(PyObject *self, PyObject *args){
    int steps,gpio;
    if ( !PyArg_ParseTuple(args,"ii:move_motor",&steps,&gpio)) {
        return NULL;
    }
    return Py_BuildValue("i", move_motor(steps,gpio));
}



static PyMethodDef c_drivermethods[] = {
    {"move_motor",py_move_motor, METH_VARARGS, py_move_motor_doc},
    {NULL,NULL,0,NULL}
};

#if PY_MAJOR_VERSION < 3
void initc_driver(void){
    PyObject *mod;
    mod = Py_InitModule("c_driver", c_drivermethods);
    PyModule_AddIntMacro(mod,MAGIC);
}
#else
static struct PyModuleDef c_drivermodule = {
    PyModuleDef_HEAD_INIT,
    "c_driver", /*module name */
    "This is the module documentation",//NULL, /*documentation*/
    -1,
    c_drivermethods
};
PyMODINIT_FUNC
PyInit_c_driver(void) {
    PyObject *mod;
    mod = PyModule_Create( &c_drivermodule);
    PyModule_AddIntMacro(mod, MAGIC);
    return mod;
}

#endif

