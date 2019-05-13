#!/bin/bash

array=(*.gjf)

echo "#!/bin/bash" >> all.script
echo "#" >> all.script

for i in ${array[@]} 
do

echo "#!/bin/bash -l" >> ${i%%.*}.pbs
echo "#PBS -S /bin/bash" >> ${i%%.*}.pbs
echo "#PBS -q short" >> ${i%%.*}.pbs
echo -en  '\n' >> ${i%%.*}.pbs

echo "#PBS -l nodes=1:ppn=8" >> ${i%%.*}.pbs
echo "#PBS -l walltime=48:0:0" >> ${i%%.*}.pbs
echo "#PBS -l mem=4200MB" >> ${i%%.*}.pbs
echo "#PBS -l cput=10000:00:00" >> ${i%%.*}.pbs

echo -en  '\n' >> ${i%%.*}.pbs
echo "module load gaussian/g16.A" >> ${i%%.*}.pbs
echo "cd \$PBS_O_WORKDIR" >> ${i%%.*}.pbs

echo -en  '\n' >> ${i%%.*}.pbs
echo "g16 ${i%%.*}.gjf" >> ${i%%.*}.pbs

echo -en  '\n' >> ${i%%.*}.pbs

echo "qsub ${i%%.*}.pbs" >> all.script
done

bash all.script
