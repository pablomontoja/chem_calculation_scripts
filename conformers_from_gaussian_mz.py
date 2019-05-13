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
		self.termination = ""
		self.thermochemistry = ""
		self.zpe = 0.000
		self.energy_correction = 0.000
		self.enthalpy_correction = 0.000
		self.free_energy_correction = 0.000
		self.corrected_zpe=0.000
		self.corrected_energy=0.000
		self.corrected_enthalpy=0.000
		self.corrected_free_energy=0.000
		self.counterpoise_corrected_energy=0.000
		self.cavity_surface_area=0.000

		self.scfenergies = []
		#self.cp_lastscfenergy = 0.000
		#self.cp_lastscfinkjpermole = 0.000
		self.cp_with_freq = 0

		file = open(filename, "r")
		for index, line in enumerate(file):
			if "#" and "freq" and "Counterpoise" in line: self.cp_with_freq = 1
			if "#" and "freq" and "counterpoise" in line: self.cp_with_freq = 1
			if "SCF Done" in line: self.extractEnergy(line.rstrip('\n'))
			if "Normal termination" in line: self.termination = "Normal termination"
			if "Thermochemistry" in line: self.thermochemistry = "Thermo"
			if "Zero-point correction" in line: self.zpe = float(line.rstrip('\n').split("=")[1].strip().split(" ")[0])
			if "Thermal correction to Energy" in line: self.energy_correction = float(line.rstrip('\n').split("=")[1].strip())
			if "Thermal correction to Enthalpy" in line: self.enthalpy_correction = float(line.rstrip('\n').split("=")[1].strip())
			if "Thermal correction to Gibbs Free Energy" in line: self.free_energy_correction = float(line.rstrip('\n').split("=")[1].strip())
			#if "Sum of electronic and zero-point Energies" in line: self.corrected_zpe = float(line.rstrip('\n').split("=")[1].strip())
			if "Sum of electronic and zero-point Energies" in line: self.corrected_zpe = self.lastscfenergy + self.zpe
			#if "Sum of electronic and thermal Energies" in line: self.corrected_energy = float(line.rstrip('\n').split("=")[1].strip())
			if "Sum of electronic and thermal Energies" in line: self.corrected_energy = self.lastscfenergy + self.energy_correction
			#if "Sum of electronic and thermal Enthalpies" in line: self.corrected_enthalpy = float(line.rstrip('\n').split("=")[1].strip())
			if "Sum of electronic and thermal Enthalpies" in line: self.corrected_enthalpy = self.lastscfenergy + self.enthalpy_correction
			if "Counterpoise corrected energy" in line: self.counterpoise_corrected_energy = float(line.rstrip('\n').split("=")[1].strip() )
			if "Sum of electronic and thermal Free Energies" in line:
				self.corrected_free_energy = self.lastscfenergy + self.free_energy_correction
				self.lastscfinkjpermoleFreeEnergy = self.convertHartreeTokJPerMole(self.corrected_free_energy)
			if "Cavity surface area" in line: self.cavity_surface_area = float(line.rstrip('\n').split("=")[1].strip().split(" ")[0].strip())

	def extractEnergy(self, line):
		self.scfenergies.append(float(line.rstrip('\n').split("=")[1].strip().split(" ")[0]))
		if len(self.scfenergies) >= 5 and self.cp_with_freq == 1 :
		 	#self.cp_lastscfenergy = self.scfenergies[-5]
		 	#self.cp_lastscfinkjpermole = self.convertHartreeTokJPerMole(self.scfenergies[-5])
		 	self.lastscfenergy = self.scfenergies[-5]
			self.lastscfinkjpermole = self.convertHartreeTokJPerMole(self.lastscfenergy)
		else:
			self.lastscfenergy = float(line.rstrip('\n').split("=")[1].strip().split(" ")[0])
			self.lastscfinkjpermole = self.convertHartreeTokJPerMole(self.lastscfenergy)

	def convertHartreeTokJPerMole(self, value):
		return value*2625.500


class ConformerTools:

	def __init__(self, allConformers):
		self.eqv_counterpoise_corrected_energy=0.000
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
			procent = float(conf.ratio.split("%")[0])
			#print conf.ratio
			self.eqv_counterpoise_corrected_energy = self.eqv_counterpoise_corrected_energy + (procent*conf.counterpoise_corrected_energy/100)


	def setRatio(self, conf):
		value = 100*(math.exp( -(conf.lastscfinkjpermole-self.lowestconfenergy)/RT_CONST))/self.sumofenergyexponents
		
		conf.ratio = str(value) + "%"
		conf.value = value/100
		conf.diff = conf.lastscfinkjpermole-self.lowestconfenergy		

		#return str(value) + "%"

	def convertHartreeTokJPerMole(self, value):
		return value*2625.500





class FreeEnergyConformerTools:
	def __init__(self, allConformers):
		self.listofenergies = []
		self.exponentofenergies = []
		self.eqv_zpe=0.000
		self.eqv_energy_correction=0.000
		self.eqv_enthalpy_correction=0.000
		self.eqv_free_energy_correction=0.000
		self.eqv_lastscfenergy=0.000
		self.eqv_counterpoise_corrected_energy=0.000

		for conf in allConformers:
			self.listofenergies.append(conf.lastscfinkjpermoleFreeEnergy)

		self.listofenergies.sort()
		self.lowestFreEnergyConfEnergy = self.listofenergies[0]

		for conf in allConformers:
			self.exponentofenergies.append(math.exp( -(conf.lastscfinkjpermoleFreeEnergy-self.lowestFreEnergyConfEnergy)/RT_CONST) )

		self.sumofenergyexponents = sum(self.exponentofenergies)

		for conf in allConformers:
			self.setRatio(conf)
			procent = float(conf.ratio.split("%")[0])
			self.eqv_zpe = self.eqv_zpe + (procent*conf.zpe/100)
			self.eqv_energy_correction = self.eqv_energy_correction + (procent*conf.energy_correction/100)
			self.eqv_enthalpy_correction = self.eqv_enthalpy_correction + (procent*conf.enthalpy_correction/100)
			self.eqv_free_energy_correction = self.eqv_free_energy_correction + (procent*conf.free_energy_correction/100)
			self.eqv_lastscfenergy = self.eqv_lastscfenergy + (procent*conf.lastscfenergy/100)			
			self.eqv_counterpoise_corrected_energy = self.eqv_counterpoise_corrected_energy + (procent*conf.counterpoise_corrected_energy/100)

	def setRatio(self, conf):
		value = 100*(math.exp( -(conf.lastscfinkjpermoleFreeEnergy-self.lowestFreEnergyConfEnergy)/RT_CONST))/self.sumofenergyexponents
		conf.ratio = str(value) + "%"
		conf.value = value/100
		conf.diff = conf.lastscfinkjpermoleFreeEnergy-self.lowestFreEnergyConfEnergy

	def convertHartreeTokJPerMole(self, value):
		return value*2625.500






listofconformers = []

for file in os.listdir(os.path.dirname(os.path.abspath(__file__))):
	if file.endswith(".log"):
		listofconformers.append(Conformer(file))


listofconformers.sort(key=operator.attrgetter('lastscfenergy'))
calculateConformers = ConformerTools(listofconformers)

# for conf in listofconformers:
	# print conf.filename + "   :   " + str(conf.lastscfenergy) + "   :   " + str(round(float(conf.ratio.split('%')[0]),2)) + "%   :   " + str(conf.diff) + "   :   " + str(conf.termination) + "   :   " + str(conf.thermochemistry) + "   : CP=" + str(conf.counterpoise_corrected_energy)


freeEnergyConformers = [ x for x in listofconformers if x.thermochemistry == 'Thermo' ]
freeEnergyConformers.sort(key=operator.attrgetter('corrected_free_energy'))
# print "--------------------------------------CP EQUIVALENT ---------------------------------------"
# print calculateConformers.eqv_counterpoise_corrected_energy
# print "-------------------------------------------------------------------------------------------"

if len(freeEnergyConformers) != 0:
	print "---------------------------------------------------------------------------------------"
	print "---------------------------------------------------------------------------------------"
	calculateFreeEnergyConformers = FreeEnergyConformerTools(freeEnergyConformers)

	for conf in freeEnergyConformers:
		print conf.filename + "\t|\tE0= " + str(conf.lastscfenergy) + "\t|\tEcp= " + str(conf.counterpoise_corrected_energy) + "\t|\tZPE= " + str(conf.zpe) + "\t|\tHterm= " + str(conf.enthalpy_correction)  + "\t|\tGterm= " + str(conf.free_energy_correction) + "\t|\tH=" + str(conf.corrected_enthalpy) + "\t|\tG=" + str(conf.corrected_free_energy) + "   :   " + str(round(float(conf.ratio.split('%')[0]),2)) + "%   :   " + str(conf.diff)

	# print "---------------------------------------------------------------------------------------"
	# print "--------------------------------------EQUIVALENT---------------------------------------"
	# print "---------------------------------------------------------------------------------------"
	# print "Input=EQUIVALENT_OF_CONFORMERS"
	# print "Zero-point correction=" + str(calculateFreeEnergyConformers.eqv_zpe) + " (Hartree/Particle)"
	# print "Thermal correction to Energy=" + str(calculateFreeEnergyConformers.eqv_energy_correction)
	# print "Thermal correction to Enthalpy=" + str(calculateFreeEnergyConformers.eqv_enthalpy_correction)
	# print "Thermal correction to Gibbs Free Energy=" + str(calculateFreeEnergyConformers.eqv_free_energy_correction)
	# print "SCF Done:E(RwB97XD) =  " + str(calculateFreeEnergyConformers.eqv_lastscfenergy)
	# print "Counterpoise corrected energy =  " + str(calculateFreeEnergyConformers.eqv_counterpoise_corrected_energy)
	# print "---------------------------------------------------------------------------------------"
	# print "EQUIVALENT_OF_CONFORMERS"
	# print str(calculateFreeEnergyConformers.eqv_zpe)
	# print str(calculateFreeEnergyConformers.eqv_energy_correction)
	# print str(calculateFreeEnergyConformers.eqv_enthalpy_correction)
	# print str(calculateFreeEnergyConformers.eqv_free_energy_correction)
	# print str(calculateFreeEnergyConformers.eqv_lastscfenergy)
	# print str(calculateFreeEnergyConformers.eqv_counterpoise_corrected_energy)



