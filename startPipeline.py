import sys
import pdb

from os import sep
import projectCtrl 
sys.path.append('E:/Savage/craterRepo/craters/bayesCraterModeling')
from pythonUtil.directories import currentAlbedoName,currentDTMName,resultsFolder,currentPDSName
from pythonUtil.directories import albedoFoler,DTMFolder,PDSFolder


# albedoFoler = "E:\\Savage\\readIMG\\albedo"
# DTMFolder = "E:\\Savage\\readIMG\\dtm"
# PDSFolder = "E:\\Savage\\readIMG\\pds"
# # Here we will output DTM and images crops for GPU
# tempFolder = "E:\\Savage\\readIMG\\temp"

# from pythonMCMC.CraterRequest import CraterRequest
import pythonUtil.readDTM as readDTM
import pythonUtil.readPDS as readPDS
from pythonUtil.profileCrater import savePlotProfile
# savePlotProfile0
# import imageUtil
from MLProject import MLProject
import mlUtil.mlUtil as mlUtil
import imageUtil
from heatmap import Heatmap
from pythonMCMC.CraterRequest import CraterRequest

# from pythonMCMC.maximumLikelihood import optimize
from pythonMCMC.MCMCoptimization import optimize


from scipy import signal

circles = [(96.372826086956522, 405.85760869565217), (171.21416434033256, 67.414127928146627), (240.00039192631786, 310.98628257887515), (270.5, 174.5), (271.5, 428.5), (271.5, 591.5), (303.5, 1047.5), (379.09751037344398, 195.3440211241041), (402.10163736512487, 574.60737191579267), (377.29591836734693, 853.40816326530614), (365.0, 1031.5), (428.5, 746.0), (492.0, 79.0), (685.48985951597092, 156.76142846372295), (607.62601496576974, 321.70975959242156), (735.06600496277918, 596.57882547559961), (814.67647058823525, 981.14705882352939), (850.5, 349.0), (1087.8495024875622, 1310.1119402985075), (1084.141975308642, 980.64197530864203),(1103.5, 222.0), (1263.7127659574469, 1037.372340425532), (1285.5, 1103.5), (1326.5619658119658, 1338.6303418803418), (1482.3355704697988, 1014.0342281879194)]



circles = circles[0:3]
for c in circles:
	# c = circles[0]
	crater = optimize( c[1],c[0])
	# optimize( None,None)
	exit()
exit()




mlProject = MLProject("Craters")
c = mlProject.getCraters()

# crater = craterRequest.getCrater()#optimize(0,0)
# bumps =  craterRequest.getBumps()
# mlProject.insertCrater(pds,crater,bumps)
# exit()
# Load full dtm
# dtm = readDTM.loadRawIMG(DTMFolder+sep+currentDTMName)
# readDTM.saveMatIMG(dtm,currentDTMName)
# scipy.misc.imresize(arr, size,
# exit()

# print c # c.lat,c.lon
# exit()
craterRequest = CraterRequest()

# '''
# bestFit = mlUtil.findBestSVMHyperparameters(mlProject,False)
# clfs = mlUtil.getClasifiersForProject(mlProject,bestFit,False)
# heatmap = Heatmap (clfs,mlProject)
# '''


# craterDetector.load(mlProject)
# imageine this is an iteration
# Read files from folder
# conver image to PNG
# currentAlbedoName = "ESP_025459_1895_RED_D_01_ORTHO.png"
# currentDTMName = "DTEED_025459_1895_026514_1895_A01.IMG"
# currentPDSName = "ESP_025459_1895_RED.LBL"


# Load full dtm
dtm = readDTM.loadRawIMG(DTMFolder+sep+currentDTMName)
# readDTM.saveMatIMG(dtm,currentDTMName)

# read pds object
pds = readPDS.loadPDS(PDSFolder+sep+currentPDSName)
#load full image
#albedo,albedoInfo = imageUtil.loadImage(albedoFoler+sep+currentAlbedoName)# imageCtrl.getImage(currentAlbedoName,project,albedoFoler)
mlProject.loadImage(albedoFoler+sep+currentAlbedoName)
mlProject.loadDTM(dtm)

# mlProject.scaleImageAndDTM()
# mlProject.loadPDS(pds)

cropsX,cropsY = mlProject.getGPUCrops()

# exit()
for cropIndexY in cropsY:
	for cropIndexX in cropsX:
		# cropIndexX,cropIndexY = 0,0 #0.3,0.4
		# cropIndexX,cropIndexY = 7.2,3.2
		
		# Big good crater
		# cropIndexX,cropIndexY = 1.2,1.9

		# # Very big bad Crater
		# cropIndexX,cropIndexY = 7,1.7
		
		# bad fit crater
		# cropIndexX,cropIndexY = 4.75,2.1
		# second bad fit crater
		# cropIndexX,cropIndexY = 0.45,1.3
		# Zunil secondary
		# cropIndexX,cropIndexY = 2,1
		
		# ESP_029468_1920_RED
		cropIndexX,cropIndexY = 3.7,2.75
		# cropIndexX,cropIndexY = 0,2.65
		# cropIndexX,cropIndexY = 2.8,2.35
		cropAlbedo = mlProject.getGPUCrop(cropIndexX,cropIndexY)
		cropDTM = readDTM.detrain(mlProject.getGPUCrop(cropIndexX,cropIndexY,True))
		mlProject.setCropRawDataGray(cropAlbedo)
		pds.setCropIndex(cropIndexX,cropIndexY)

		craterRequest.loadRawDTM(cropDTM)
		craterRequest.loadRawImg(cropAlbedo)
		craterRequest.loadRawPDS(pds)
		exit()
		# pds.printPDS()
		# pds = craterRequest.getPDS()
		# pds.printPDS()
		# plot profile
		# crater = optimize(0,0)
		crater = craterRequest.getCrater()#optimize(0,0)
		bumps =  craterRequest.getBumps()
		mlProject.insertCrater(pds,crater,bumps)
		# mlProject.getCraters()
		# 
		savePlotProfile(cropDTM)
		# imageUtil.plotProfiles(crater,bumps,cropDTM)

		# # pdb.set_trace()
		sys.exit()
		# pdb.set_trace()
		# mlProject.displayImage() currentAlbedoName
		# craterRequest.loadCrop(crop) currentDTMName
		mlProject.displayImage(cropAlbedo,"Gray scale",True,None)
		mlProject.displayImage(cropDTM,"DTM",lbl_colorbar=['%0.2f [m]','%0.2f [m]'])
		heatmap.setOutputName(resultsFolder(),cropIndexX,cropIndexY)
		heatmap.generateComposite()
		circles = heatmap.plotComposite()
		exit()
		print circles
		# exit()
		circles = [(96.372826086956522, 405.85760869565217), (171.21416434033256, 67.414127928146627), (240.00039192631786, 310.98628257887515), (270.5, 174.5), (271.5, 428.5), (271.5, 591.5), (303.5, 1047.5), (379.09751037344398, 195.3440211241041), (402.10163736512487, 574.60737191579267), (377.29591836734693, 853.40816326530614), (365.0, 1031.5), (428.5, 746.0), (492.0, 79.0), (685.48985951597092, 156.76142846372295), (607.62601496576974, 321.70975959242156), (735.06600496277918, 596.57882547559961), (814.67647058823525, 981.14705882352939), (850.5, 349.0), (1087.8495024875622, 1310.1119402985075), (1084.141975308642, 980.64197530864203),(1103.5, 222.0), (1263.7127659574469, 1037.372340425532), (1285.5, 1103.5), (1326.5619658119658, 1338.6303418803418), (1482.3355704697988, 1014.0342281879194)]
		for c in circles:
			optimize( c[1],c[0])
		mlProject.show()
		
		exit()
		# exit()
		heatmap.generateComposite()
		# mlProject.displayImage(cropAlbedo,"currentAlbedoName")
		# mlProject.displayImage(cropDTM,"currentAlbedoName")
		circles = heatmap.plotComposite()
		print circles
		exit()
		craterRequest.sendCraterCandidates(circles)
		# craterRequest.sendHeatmap(circles)
		# circles = heatmap.getCentroids()
		exit()

		craterRequest.loadRawDTM(cropDTM)
		craterRequest.loadRawImg(cropAlbedo)
		craterRequest.setCentroids(circles)

