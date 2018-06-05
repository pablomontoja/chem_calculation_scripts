#!/usr/bin/python
import sys, os, operator, math

R_CONST = 0.0083144598 # kJ/mol*K
T_CONST = 298.15 # K
RT_CONST = R_CONST*T_CONST

class Conformer:	 

   def __init__(self, filename):
   	self.filename = filename
   	self.ratio = 0.000
   	self.value = 0.000
   	self.diff = 0.000
	ind = 0
	file = open(filename, "r")
	for index, line in enumerate(file):
		if "FINAL HEAT OF FORMATION" in line:
			self.extractEnergy(line.rstrip('\n'))
			ind = 1
	if ind == 0:
		print "ERROR IN FILE: "+filename
		print "You must move the file somewhere else."
		print "						"
		exit()

   def extractEnergy(self, line):
   	self.lastscfenergy = float(line.rstrip('\n').split("=")[2].strip().split(" ")[0])
   	#print self.lastscfenergy
   	self.lastscfinkjpermole = self.lastscfenergy

   def convertHartreeTokJPerMole(self, value):
		return value*2625.500


class ConformerTools:

	def __init__(self, allConformers):
		self.listofenergies = []
		self.exponentofenergies = []
		for conf in allConformers:
			self.listofenergies.append(conf.lastscfinkjpermole)

		self.listofenergies.sort()
		self.lowestconfenergy = self.listofenergies[0]
		for conf in allConformers:
			self.exponentofenergies.append(math.exp( -(conf.lastscfinkjpermole-self.lowestconfenergy)/RT_CONST) )

		self.sumofenergyexponents = sum(self.exponentofenergies)

		for conf in allConformers:
			self.setRatio(conf)


	def setRatio(self, conf):
		value = 100*(math.exp( -(conf.lastscfinkjpermole-self.lowestconfenergy)/RT_CONST))/self.sumofenergyexponents
		conf.ratio = str(value) + "%"
		conf.value = value/100
		conf.diff = conf.lastscfinkjpermole-self.lowestconfenergy

		#return str(value) + "%"

	def convertHartreeTokJPerMole(self, value):
		return value*2625.500

   # def printInfo(self):
   # 	print "**********************************************************************"
   # 	print "FILENAME: " + self.filename
   # 	print "FILEPATH: " + self.filepath
   # 	print "START DATETIME: " + self.startdatetime
   # 	print "END DATETIME: " + self.enddatetime
   # 	print "NUCLEAR REPULSION ENERGY: " + self.nuclearrepulsionenergy
   # 	print "FINAL DFT ENERGY: " + self.finaldftenergy
   # 	print "----------------------------------------------------------------------"
   # 	print "TYPE OF CALCULATION: " + self.typeofcalculation   	
   # 	print '\n'.join(self.typeofcalculationinfo)
   # 	print "----------------------------------------------------------------------"   	
   # 	print '\n'.join(self.extrainfo)
   # 	print "HOST NAME:" + self.hostname
   # 	print "----------------------------------------------------------------------"
   # 	print '\n'.join(self.atomsandbasisset)
   # 	print "----------------------------------------------------------------------"
   # 	print "**********************************************************************"

listofconformers = []

for file in os.listdir(os.path.dirname(os.path.abspath(__file__))):
	if file.endswith(".out"):
		listofconformers.append(Conformer(file))

# print listofconformers[0].filename
# print listofconformers[0].lastscfenergy

listofconformers.sort(key=operator.attrgetter('lastscfenergy'))
calculateConformers = ConformerTools(listofconformers)

for conf in listofconformers:
	if conf.diff < 22:
		print conf.filename + "   :   " + str(conf.lastscfenergy) + "   :   " + str(conf.ratio) + "   :   " + str(conf.diff)
		command = "babel -imopout "+conf.filename+" -oxyz "+conf.filename.split(".")[0]+"_wB97XD_631gd.xyz"
		os.system(command)
		command2 = "tail -n +3 "+conf.filename.split(".")[0]+"_wB97XD_631gd.xyz"+" > "+conf.filename.split(".")[0]+"_wB97XD_631gd.gjf"
		os.system(command2)
		command3 = "echo -en '\\n' >> "+conf.filename.split(".")[0]+"_wB97XD_631gd.gjf"
		os.system(command3)
		command4 = "rm "+conf.filename.split(".")[0]+"_wB97XD_631gd.xyz"
		os.system(command4)







# calc = Conformer(sys.argv[1])
# datetimelist = []

# searchfile = open(sys.argv[1], "r")

# for index, line in enumerate(searchfile):
#     if "Date and time (Linux)" in line: datetimelist.append(line.rstrip('\n'))
#     if "MPI run using" in line: calc.addExtraInfo(line.rstrip('\n').split('*')[1].lstrip())
#     if "Atoms and basis sets" in line: calc.extractAtomsAndBasisSet(index, sys.argv[1])
#     if "Nuclear repulsion energy" in line: calc.extractNuclearRepulsionEnergy(line.rstrip('\n'))
#     if "This is a DFT calculation of type" in line: 
#     	calc.extractTypeOfCalculation(index, sys.argv[1])
#     	calc.istypeofcalculationadded = True
#     if "Final DFT energy" in line: calc.extractFinalDftEnergy(line.rstrip('\n'))
#     if "Total CPU  time used in DALTON" in line: calc.addExtraInfo(line.rstrip('\n'))
#     if "Host name" in line: calc.setHostName(line.rstrip('\n'))

# searchfile.close()

# calc.extractDateTimeInfo(datetimelist)
# calc.printInfo()






 #   def extractDateTimeInfo(self, lineslist):
 #   	self.enddatetime = lineslist[-1].split(':', 1)[1]
 #   	self.startdatetime = lineslist[0].split(':', 1)[1]

 #   def extractAtomsAndBasisSet(self, index, filepath):
 #   	f = open(filepath,'r')
 #   	lines = f.readlines()[index:]
 #   	for line in lines:
 #   		if line.strip() == 'Symmetry Coordinates':
 #   			break
 #   		if line.strip() != '':
 #   			self.atomsandbasisset.append(line.strip())

 #   def extractTypeOfCalculation(self, index, filepath):
 #   	if self.istypeofcalculationadded == True:
 #   		return
 #   	f = open(filepath,'r')
 #   	lines = f.readlines()[index:index+6]
 #   	self.typeofcalculation = lines[0].rstrip('\n').split(':', 1)[1]
	# #self.typeofcalculationinfo.append(str(index))
 #   	for line in lines[1:]:
 #   		if line.strip() == '':
 #   			break
 #   		if line.strip() != '':
 #   			self.typeofcalculationinfo.append(line.strip())
   	

 #   def extractFinalDftEnergy(self, line):
 #   	self.finaldftenergy = line.split(':', 1)[1]

 #   def extractNuclearRepulsionEnergy(self, line):
 #   	self.nuclearrepulsionenergy = line.split(':', 1)[1]

 #   def addExtraInfo(self, line):
 #   	self.extrainfo.append(line)

 #   def setHostName(self, line):
 #   	self.hostname = line.split(':', 1)[1]