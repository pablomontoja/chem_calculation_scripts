#!/usr/bin/python
import sys, os, getopt, math, operator

R_CONST = 0.0083144598 # kJ/mol*K
T_CONST = 298.15 # K
RT_CONST = R_CONST*T_CONST

class Calculation:   

   def __init__(self, filepath):
    self.filename = os.path.basename(filepath)
    self.filepath = os.path.abspath(filepath)
    self.extrainfo = []
    self.atomsandbasisset = []
    self.ratio = ""
    self.value = 0
    self.diff = 0

   def extractDateTimeInfo(self, lineslist):
    self.enddatetime = lineslist[-1].split(':', 1)[1]
    self.startdatetime = lineslist[0].split(':', 1)[1]

   def extractAtomsAndBasisSet(self, index, filepath):
    f = open(filepath,'r')
    lines = f.readlines()[index:]
    for line in lines:
      if line.strip() == 'Symmetry Coordinates':
        break
      if line.strip() != '':
        self.atomsandbasisset.append(line.strip())

   def extractTypeOfCalculation(self, index, filepath):
    f = open(filepath,'r')
    lines = f.readlines()[index:index+2]
    self.typeofcalculation = lines[1].rstrip('\n')

   def extractFInalDftEnergy(self, line):
    self.finaldftenergy = float(line.split(':', 1)[1])

   def extractNuclearRepulsionEnergy(self, line):
    self.nuclearrepulsionenergy = line.split(':', 1)[1]

   def addExtraInfo(self, line):
    self.extrainfo.append(line)

   def setHostName(self, line):
    self.hostname = line.split(':', 1)[1]

   def printInfo(self):
    print "**********************************************************************"
    print "FILENAME: " + self.filename
    print "FILEPATH: " + self.filepath
    print "START DATETIME: " + self.startdatetime
    print "END DATETIME: " + self.enddatetime
    print "NUCLEAR REPULSION ENERGY: " + self.nuclearrepulsionenergy
    print "TYPE OF CALCULATION: " + self.typeofcalculation
    print "FINAL DFT ENERGY: " + str(self.finaldftenergy)
    print '\n'.join(self.extrainfo)
    print "HOST NAME:" + self.hostname
    print "----------------------------------------------------------------------"
    print '\n'.join(self.atomsandbasisset)
    print "----------------------------------------------------------------------"
    print "**********************************************************************"


class ConformerTools:

	def __init__(self, allConformers):
		self.listofenergies = []
		self.exponentofenergies = []
		for conf in allConformers:
			self.listofenergies.append(self.convertHartreeTokJPerMole(conf.finaldftenergy))

		self.listofenergies.sort()
		self.lowestconfenergy = self.listofenergies[0]
		for conf in allConformers:
			self.exponentofenergies.append(math.exp( -(self.convertHartreeTokJPerMole(conf.finaldftenergy)-self.lowestconfenergy)/RT_CONST) )

		self.sumofenergyexponents = sum(self.exponentofenergies)

		for conf in allConformers:
			self.setRatio(conf)


	def setRatio(self, conf):
		value = 100*(math.exp( -(self.convertHartreeTokJPerMole(conf.finaldftenergy)-self.lowestconfenergy)/RT_CONST))/self.sumofenergyexponents
		conf.ratio = str(value) + "%"
		conf.value = value/100
		conf.diff = self.convertHartreeTokJPerMole(conf.finaldftenergy)-self.lowestconfenergy

		#return str(value) + "%"

	def convertHartreeTokJPerMole(self, value):
		return value*2625.500


def usage():
  print 'Usage: '+sys.argv[0]+' [-i <inputfile>] [options]'

def main(argv):
	try:
		opts, args = getopt.getopt(argv[1:], "hi:", ["help", "input="])
	except getopt.GetoptError as err:
		print str(err)
		sys.exit(2)

	inputfilelist = []
	calculationsList = []

	if not opts:
		for file in os.listdir(os.path.dirname(os.path.abspath(__file__))):
			if file.endswith(".log"):
				inputfilelist.append(file)		
	else:
	    for o, a in opts:
	    	if o in ("-h", "--help"):
	    		usage()
	    		sys.exit()
	    	elif o in ("-i", "--input"):
	    		inputfilelist.append(a)
	    	else:
	    		assert False, "unhandled option"

	for file in inputfilelist:
		calc = Calculation(file)
		datetimelist = []

		searchfile = open(file, "r")

		for index, line in enumerate(searchfile):
		    if "Date and time (Linux)" in line: datetimelist.append(line.rstrip('\n'))
		    if "MPI run using" in line: calc.addExtraInfo(line.rstrip('\n').split('*')[1].lstrip())
		    if "Atoms and basis sets" in line: calc.extractAtomsAndBasisSet(index, file)
		    if "Nuclear repulsion energy" in line: calc.extractNuclearRepulsionEnergy(line.rstrip('\n'))
		    if "This is a DFT calculation of type" in line: calc.extractTypeOfCalculation(index, file)
		    if "Final DFT energy" in line: calc.extractFInalDftEnergy(line.rstrip('\n'))
		    if "Total CPU  time used in DALTON" in line: calc.addExtraInfo(line.rstrip('\n'))
		    if "Host name" in line: calc.setHostName(line.rstrip('\n'))

		searchfile.close()

		calc.extractDateTimeInfo(datetimelist)
		calc.printInfo()
		datetimelist = []
		calculationsList.append(calc)

		# CONFROMERS PART
		calculationsList.sort(key=operator.attrgetter('finaldftenergy'))
		calculateConformers = ConformerTools(calculationsList)
		
		print "                                                                      "
		print "                                                                      "
		print "                                                                      "
		print "                                                                      "
		print "**********************************************************************"
		print "--------------------------CONFORMERS INFO-----------------------------"
    	print "**********************************************************************"
    	print "filename" + "   :   " + "final dft energy" + "   :   " + "ratio (%)" + "   :   " + "diff (kJ/mol)"

    	for conf in calculationsList:
			print conf.filename + "   :   " + str(conf.finaldftenergy) + "   :   " + str(conf.ratio) + "   :   " + str(conf.diff)



def printConformers(calcList):
	pass


if __name__ == "__main__":
    main(sys.argv)
