import sys;
import math;

import cProfile

def profiler( func ):
    def wrapper( args, **argv ):
        profile_filename = "{}.prof".format(func.__name__);
        profiler = cProfile.Profile();
        result = profiler.rucall(func, *args, **argv);
        profiler.dump_stats(profile_name);
        return result;
    return wrapper;

def is_prime( number ):
    for i in xrange(2, (int) (math.sqrt(number)) + 1):
        if number % i == 0:
            return False;
    return True;

def get_prime_numbers( number ):
    prime_numbers = list();
    for num in xrange(2, number):
        if is_prime(num):
            prime_numbers.append(num);
    return prime_numbers;

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Err");
        sys.exit(1);
    number = int(sys.argv[1]);
    prime_numbers = profiler(get_prime_numbers)(number);
    print(prime_numbers);
