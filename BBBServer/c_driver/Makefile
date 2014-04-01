all:
	python setup.py build_ext --inplace
c:
	gcc -c c_driver.c
	gcc c_driver.o main.c -o main
install:
	python setup.py install
clean:
	rm -fr *.so *.o *~ build main
