#!/bin/bash
for f in *.xyz
do
	babel -ixyz $f -omop "${f%%.*}".mop
	# tail -n +3 $f > "${f%%.*}".gjf
	# echo "" >> "${f%%.*}".gjf
done

array=(*.mop)

echo "#!/bin/bash" >> all.script
echo "#" >> all.script

for i in ${array[@]} 
do

echo "#!/bin/bash" >> ${i%%.*}.pbs
echo "#PBS -S /bin/bash" >> ${i%%.*}.pbs
echo -en  '\n' >> ${i%%.*}.pbs
echo "#PBS -q mjshort" >> ${i%%.*}.pbs
echo "#PBS -l nodes=1:ppn=1" >> ${i%%.*}.pbs
# echo "#PBS -e error.error" >> ${i%%.*}.pbs
# echo "#PBS -o error.output" >> ${i%%.*}.pbs
echo "#PBS -l walltime=4:00:00" >> ${i%%.*}.pbs
echo "#PBS -l mem=200MB" >> ${i%%.*}.pbs
# echo "#PBS -l cput=10000:00:00" >> ${i%%.*}.pbs
echo -en  '\n' >> ${i%%.*}.pbs
echo "export LD_LIBRARY_PATH=/opt/mopac:$LD_LIBRARY_PATH" >> ${i%%.*}.pbs
echo -en  '\n' >> ${i%%.*}.pbs
echo "cd \$PBS_O_WORKDIR" >> ${i%%.*}.pbs
echo "/opt/mopac/MOPAC2016.exe ${i%%.*}.mop << EOF" >> ${i%%.*}.pbs
echo -en  '\n' >> ${i%%.*}.pbs
echo "EOF" >> ${i%%.*}.pbs

echo "qsub ${i%%.*}.pbs" >> all.script
done

sed -i '1c\PM7 THREADS=1 CHARGE=1 PRECISE CYCLES=3000 DISP' *.mop
