#!/bin/bash
if [ -z "$1" ]; then
	echo "Nazwa pliku mol musi byc podana jako pierwszy parametr"
	exit
fi

if [ -z "$2" ]; then
	echo "Nazwa pliku dal musi byc podana jako drugi parametr"
	exit
fi

mol=$1  # plik mol jako pierwszy parametr
dal=$2	# plik dal jako drugi parametr

functionals=("B97-D" "B3LYP" "BP86" "CAMB3LYP" "CAMB3LYP alpha=0.190 beta=0.460 mu=0.450" "KT2" "PBE0" "PBE")
folder_names=()
index=0

for f in "${functionals[@]}"
do
	# IFS=', ' read -r -a array <<< "$string"
	name=$(echo -e "${f}" | tr -d '[:space:]')
	folder_names[index]=$name
	(( index++ ))
done


index=0

echo "#!/bin/bash" > all.script
echo "#" >> all.script

for f in "${functionals[@]}"
do
	mkdir "${folder_names[index]}"
	cp "${dal}" "${folder_names[index]}"/"${dal}"
	cp "${mol}" "${folder_names[index]}"/"${mol}"
	#cd "${folder_names[index]}"

	sed -i "s/B3LYP/${f}/g" "${folder_names[index]}"/"${dal}"

	echo "#!/bin/bash" >> "${folder_names[index]}"/dalton.pbs
	echo "#PBS -S /bin/bash" >> "${folder_names[index]}"/dalton.pbs
	echo -en  '\n' >> "${folder_names[index]}"/dalton.pbs
	echo "#PBS -q verylong" >> "${folder_names[index]}"/dalton.pbs
	echo "#PBS -l nodes=1:ppn=8:dalton" >> "${folder_names[index]}"/dalton.pbs
	echo "#PBS -e ${folder_names[index]}/error" >> "${folder_names[index]}"/dalton.pbs
	echo "#PBS -o ${folder_names[index]}/output" >> "${folder_names[index]}"/dalton.pbs
	echo "#PBS -l walltime=720:00:00" >> "${folder_names[index]}"/dalton.pbs
	echo "#PBS -l mem=16500MB" >> "${folder_names[index]}"/dalton.pbs
	# echo "#PBS -l cput=10000:00:00" >> "${folder_names[index]}"/dalton.pbs
	echo -en  '\n' >> "${folder_names[index]}"/dalton.pbs
	echo -en  'export OMP_NUM_THREADS=1' >> "${folder_names[index]}"/dalton.pbs
	echo -en  'export MKL_NUM_THREADS=1' >> "${folder_names[index]}"/dalton.pbs	
	echo -en  '\n' >> "${folder_names[index]}"/dalton.pbs
	echo "module load openmpi-1.8-x86_64" >> "${folder_names[index]}"/dalton.pbs
	echo -en  '\n' >> "${folder_names[index]}"/dalton.pbs
	echo "cd \$PBS_O_WORKDIR/${folder_names[index]}" >> "${folder_names[index]}"/dalton.pbs
	echo -en  '\n' >> "${folder_names[index]}"/dalton.pbs
	echo "dalton_path=/opt/dalton/2016.2-gnu-openmpi" >> "${folder_names[index]}"/dalton.pbs
	echo "dal=${dal}" >> "${folder_names[index]}"/dalton.pbs
	echo "mol=${mol}" >> "${folder_names[index]}"/dalton.pbs
	echo -en  '\n' >> "${folder_names[index]}"/dalton.pbs
	echo "exec=\$dalton_path/dalton" >> "${folder_names[index]}"/dalton.pbs
	echo -en  '\n' >> "${folder_names[index]}"/dalton.pbs
	echo "\$exec -mb 16000 -N 8 \$dal \$mol >> \$PBS_O_WORKDIR/${folder_names[index]}/result.OUT" >> "${folder_names[index]}"/dalton.pbs

	echo -en  '\n' >> "${folder_names[index]}"/dalton.pbs

	echo "qsub ${folder_names[index]}/dalton.pbs" >> all.script

	(( index++ ))
done

#bash all.script
