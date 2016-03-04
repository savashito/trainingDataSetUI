import exampleCtrl
import projectCtrl 
import classCtrl
project = projectCtrl.getProject("Craters")
_class = classCtrl.getClass("craters")
l,listExample  =  exampleCtrl.listExamples(_class)
print l