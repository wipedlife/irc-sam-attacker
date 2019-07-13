function generate {
	nick=`curl -i https://www.fakenamegenerator.com/gen-male-gr-gr.php | grep "<h3>"`
	nick=`echo $nick | cut -c5-`
	nick=`echo $nick | awk '{print $1}'`
	echo $nick
}

function loop {
	echo $(generate) > Nicks
	for i in {0..$1};do
		echo $(generate) >> Nicks
	done;
	sleep 6m
}
if [[ $# < 1 ]];then
 echo "$0 count"
 exit 1
fi
loop $1


