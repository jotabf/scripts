#1: Tipo de dado a ser mostrado
#2: Título do gráfico
#3: Arquivo de entrada
#4: Valor máximo

rm temp*
sed -i.orig 's/	/ /g' $3 	#Remove tab
cat $3 | tr -s ' ' > temp 	#Remove space
#sed -i -e '$a\' temp 		#Add new line


#GET THE MAX LINE
MAX=0
while read line; do 
	if [[ $line == *"$1"* || -z $1 ]]; then
		AUX=$(echo "$line"| wc -w)
		if (( $MAX < $AUX )); then
			MAX=$AUX;
		fi
	fi 
done < temp

#COMPLETE THE LINES WITH ZERO
while read line; do 
	if [[ $line == *"$1"* || -z $1 ]]; then
		LSI=$(echo "$line"| wc -w)
		(( DIF = $MAX - $LSI ))
		for (( i = 0; i < $DIF; i++ )); do
			line="$line 0.0";
		done
		printf '%s\n' "${line//$1/} " >> temp2 #Remove $1 from the line
	fi
done < temp
sed -i '/^$/d' temp2

#cat temp | grep $1 | awk -F $1 '{print $2}' > temp
python3 barras_empilhadas.py "temp2" "$2" $4 "$3"
rm temp*
rm *.orig

