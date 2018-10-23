#!/bin/sh

##############################################
### EXAMPLE TO RUN MANY JOBS WITH QSUB     ###
### CREATE THE qsub FILES INTO A LOOP      ###
##############################################

for i in `seq 1 2`;
do
  file_qsub=<path_for_qsub_files>/file_qsub_$i.qs
  out_file=<path_for_output>/out_$i
  err_file=<path_for_output>/err_$i

cat <<EOT >> $file_qsub
#!/bin/bash
#PBS -N $i
#PBS -l walltime=01:00:00
#PBS -l nodes=1:ppn=1
#PBS -q Unicog_short  
#PBS -o $out_file
#PBS -e $err_file
<script_to_launch>
EOT

qsub $file_qsub

done

