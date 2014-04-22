#include <Python.h>
#include "c_driver.h"

static char py_handle_gpio_doc[] = "Change gpio status\narguments: int handle_gpio(int status, char *pin_name)\n";
static char py_move_motor_doc[] = "Moves motor";
static char py_flush_all_doc[] = "Flush all";

static PyObject *py_handle_gpio(PyObject *self, PyObject *args){
    int logic_status;
    char *pin_step;
    char *tmp;
    PyObject *ret;

    if ( !PyArg_ParseTuple(args,"is:handle_gpio",&logic_status,&pin_step)) {
        return NULL;
    }
    tmp = (char *)malloc(strlen(pin_step)+1);
    strcpy(tmp,pin_step);
    ret =  Py_BuildValue("i", handle_gpio(logic_status,tmp));
    return ret;
}

static PyObject *py_move_motor(PyObject *self, PyObject *args){
    int steps;
    char *pin_step;
    char *tmp;
    PyObject *ret;

    if ( !PyArg_ParseTuple(args,"is:move_motor",&steps,&pin_step)) {
        return NULL;
    }
    tmp = (char *)malloc(strlen(pin_step)+1);
    strcpy(tmp,pin_step);
    ret =  Py_BuildValue("i", move_motor(steps,tmp));
    return ret;
}

static PyObject *py_flush_all(PyObject *self, PyObject *args){
    if ( !PyArg_ParseTuple(args,"")) {
        return NULL;
    }
    flush_all();
    return Py_None;
}


static PyMethodDef c_drivermethods[] = {
    {"handle_gpio",py_handle_gpio, METH_VARARGS,py_handle_gpio_doc},
    {"move_motor",py_move_motor, METH_VARARGS,py_move_motor_doc},
    {"flush_all",py_flush_all, METH_VARARGS, py_flush_all_doc},
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

