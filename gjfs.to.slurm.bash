#!/bin/bash

array=(*.gjf)

echo "#!/bin/bash" >> all.script
echo "#" >> all.script

for i in ${array[@]} 
do

echo "#!/bin/bash -l" >> ${i%%.*}.slurm
echo "#SBATCH -J ${i%%.*}" >> ${i%%.*}.slurm
echo "#SBATCH -A cukry" >> ${i%%.*}.slurm
echo -en  '\n' >> ${i%%.*}.slurm
echo "#SBATCH -p plgrid" >> ${i%%.*}.slurm
echo "#SBATCH -N 1" >> ${i%%.*}.slurm
echo "#SBATCH --ntasks-per-node=24" >> ${i%%.*}.slurm
echo "#SBATCH --output='${i%%.*}.cliout'" >> ${i%%.*}.slurm
echo "#SBATCH --error='${i%%.*}.err'" >> ${i%%.*}.slurm
echo "#SBATCH --time=72:00:00" >> ${i%%.*}.slurm
echo "#SBATCH --mem=33GB" >> ${i%%.*}.slurm
echo -en  '\n' >> ${i%%.*}.slurm
echo "module load apps/gaussian/g16.A.03" >> ${i%%.*}.slurm
echo "echo 'Temporary files stored in' \$GAUSS_SCRDIR" >> ${i%%.*}.slurm
echo -en  '\n' >> ${i%%.*}.slurm
echo "cp ${i%%.*}.gjf \$GAUSS_SCRDIR/${i%%.*}.gjf" >> ${i%%.*}.slurm

if [ -f "${i%%.*}.chk" ]
then
echo "cp ${i%%.*}.chk \$GAUSS_SCRDIR/${i%%.*}.chk" >> ${i%%.*}.slurm
fi

echo "cd \$GAUSS_SCRDIR" >> ${i%%.*}.slurm
echo "g16 ${i%%.*}.gjf" >> ${i%%.*}.slurm
echo -en  '\n' >> ${i%%.*}.slurm
echo "cp ${i%%.*}.log \$SLURM_SUBMIT_DIR/${i%%.*}.log" >> ${i%%.*}.slurm
echo "cp ${i%%.*}.chk \$SLURM_SUBMIT_DIR/${i%%.*}.chk" >> ${i%%.*}.slurm
echo -en  '\n' >> ${i%%.*}.slurm
echo "rm -rf \$GAUSS_SCRDIR" >> ${i%%.*}.slurm
echo -en  '\n' >> ${i%%.*}.slurm

echo "sbatch ${i%%.*}.slurm" >> all.script
done

