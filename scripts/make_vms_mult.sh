VCS_PID=`pgrep vcsim`

for i in {1..100};
do
	python3.5 add_vm.py -s 127.0.0.1 -o 8989 -u user -p pass -d DC0 -c C0 -v vm_$i -n 100;
	echo $i `ps u \`pgrep vcsim\` && ifconfig lo | grep "RX\ bytes" | sed "s/RX\ bytes:\([0-9]*\).*/\1/g"` | awk '{print $1,$15,$16,$17,$22,$24}' >> out.txt;
done


