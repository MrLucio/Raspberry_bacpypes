#!/usr/bin/env python

import os
import random
import time

from bacpypes.debugging import bacpypes_debugging, ModuleLogger
from bacpypes.consolelogging import ConfigArgumentParser

from bacpypes.core import run

from bacpypes.primitivedata import Real,Boolean
from bacpypes.object import AnalogValueObject,AveragingObject, Property, register_object_type
from bacpypes.errors import ExecutionError

from bacpypes.app import BIPSimpleApplication
from bacpypes.local.device import LocalDeviceObject

class RealProperty(Property):
    def __init__(self, identifier):
	Property.__init__(self,identifier,Real,default=0.0,optional=False,mutable=False)
    def ReadProperty(self, obj, arrayIndex=None):
	global args
	global realValue
	print(realValue)
	return realValue

class BooleanProperty(Property):
    def __init__(self, identifier):
	Property.__init__(self,identifier,Boolean,default=0.0,optional=False,mutable=False)
    def ReadProperty(self,obj,arrayIndex=None):
	global args
	global booleanValue
	return booleanValue


class MyAnalogValueObject(AnalogValueObject):
    properties = [RealProperty('presentValue'),BooleanProperty('outOfService')]
    def __init__(self, **kwargs):
	AnalogValueObject.__init__(self, **kwargs)
register_object_type(MyAnalogValueObject)

class MyAveragingObject(AveragingObject):
    properties = [RealProperty('minimumValue'),RealProperty('averageValue'),RealProperty('maximumValue')]
    def __init__(self, **kwargs):
	AveragingObject.__init__(self, **kwargs)
register_object_type(MyAveragingObject)


def main():
    global args
    parser = ConfigArgumentParser(description=__doc__)

    args = parser.parse_args()

    this_device = LocalDeviceObject(ini=args.ini)

    this_application = BIPSimpleApplication(this_device, args.ini.address)

    global realValue
    global booleanValue
    booleanValue=False
    realValue=int(input("Inserire un numero "))

    analog = MyAnalogValueObject(objectIdentifier=('analogValue',123),objectName='hea')
    averaging = MyAveragingObject(objectIdentifier=('averaging',70),objectName='averagingTest')

    this_application.add_object(analog)
    this_application.add_object(averaging)

    run()

if __name__=='__main__':
    main()

