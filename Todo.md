Fix this error, it appears when we run the code with Hardanger file

Traceback (most recent call last):
  File "C:\Users\ayas\OneDrive - SINTEF\Projects\AquaGraph\src\xml_parser\aquagraphXMLParse.py", line 465, in <module>
    main(settings)
  File "C:\Users\ayas\OneDrive - SINTEF\Projects\AquaGraph\src\xml_parser\aquagraphXMLParse.py", line 341, in main
    CageObservation=madeby(theobservation,ThisSensor[unitName,sensortype])
TypeError: 'SensorClass' object is not subscriptable



This error appears when we run the code with Settefisk

Traceback (most recent call last):
  File "C:\Users\ayas\OneDrive - SINTEF\Projects\AquaGraph\src\xml_parser\aquagraphXMLParse.py", line 465, in <module>
    main(settings)
  File "C:\Users\ayas\OneDrive - SINTEF\Projects\AquaGraph\src\xml_parser\aquagraphXMLParse.py", line 363, in main
    if isevent==True:
UnboundLocalError: local variable 'isevent' referenced before assignment