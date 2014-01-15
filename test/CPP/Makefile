all: motor
	@echo "Making tests for motors"
#cpp:
#	g++ -g -Wall -o testCPP testCPP.cpp -I.
c:
	gcc -g -Wall -o testC100Khz testC100KHz.c -I.
motor:
	gcc -g -Wall -o motor motor.c -I.
clean:
	rm -fr testCPP testC testC100KHz motor testC100Khz testC100Khz *~
