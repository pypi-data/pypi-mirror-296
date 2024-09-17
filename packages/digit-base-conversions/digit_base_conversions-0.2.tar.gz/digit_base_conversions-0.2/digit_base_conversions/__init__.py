def first_numbers_in_base(n,base,zerofill_to_length=0,most_signicant_digit_first=False):
    """
    :param n: number of numbers for which you want digits returned.
    :param base: base of the positional numeral system.
    :param zerofill_to_length: adds so many zeros to beginning of the list that represents the number if number were shorter than parameter zerofill_to_length otherwise.
    :param most_significant_digit_first: If True, positions are counted from the most significant digit.
    :return: list of lists of digits that represent number in postional system with the given base.
    """
    if most_signicant_digit_first:
        if zerofill_to_length==0:
            if n<2:
                if n:
                    yield [0]
                    #return [(0,)]
                return
            #numbers=[[0],[1]]
            yield [0]
            yield [1]
            base-=1
            l=-1
            num=[1]
            for i in range(n-2):
                if num[-1]==base:
                    num[-1]=0
                    for i in range(l,-1,-1):
                        if num[i]==base:
                            num[i]=0
                        else:
                            num[i]+=1
                            break
                    else:
                        num=[1]+num
                        l+=1
                else:
                    num[-1]+=1
                yield num.copy()
                #numbers.append(num.copy())  # replace tuple(num) with num.copy() if you want resutl to contain lists instead of tuples.
            return
            #return numbers
        else:
            if base==0 or n==0:
                return
                #return []
            number=[0]*zerofill_to_length
            #numbers=[number.copy()]
            yield number
            base=base-1
            n2=0
            n-=1
            while n2<n:
                for i in range(zerofill_to_length-1,-1,-1):
                    if number[i]==base:
                        number[i]=0
                    else:
                        number[i]+=1
                        yield number.copy()
                        #numbers.append(number.copy())
                        break
                else:
                    number=[1]+number
                    zerofill_to_length+=1
                    yield number.copy()
                    #numbers.append(number.copy())
                n2+=1
            return
            #return numbers
    else:
        if zerofill_to_length==0:
            if base==1:
                if n==0:
                    return
                elif n==1:
                    yield [0]
                else:
                    raise ValueError()
            if n<2:
                if n:
                    yield [0]
                    #return [[0]]
                return
                #return []
            #numbers=[[0],[1]]
            yield [0]
            yield [1]
            base-=1
            l=1
            num=[1]
            for i in range(n-2):
                if num[0]==base:
                    num[0]=0
                    for i in range(1,l):
                        if num[i]==base:
                            num[i]=0
                        else:
                            num[i]+=1
                            break
                    else:
                        num=num+[1]
                        l+=1
                else:
                    num[0]+=1
                #numbers.append(num.copy())  # replace tuple(num) with num.copy() if you want resutl to contain lists instead of tuples.
                yield num.copy()
            return
            #return numbers
        else:
            if base==0 or n==0:
                #return []
                #yield
                return
            number=[0]*zerofill_to_length
            #numbers=[number.copy()]
            yield number.copy()
            base=base-1
            n2=0
            n-=1
            while n2<n:
                for i in range(zerofill_to_length):
                    if number[i]==base:
                        number[i]=0
                    else:
                        number[i]+=1
                        yield number.copy()
                        #numbers.append(number.copy())
                        break
                else:
                    number=number+[1]
                    zerofill_to_length+=1
                    yield number.copy()
                    #numbers.append(number.copy())
                n2+=1
            return
            #return numbers
def number_to_list_of_digits(n,base,zerofill_to_length=0,most_signicant_digit_first=False):
    """
    :param n: a number that you want to convert to list of digits in a positional notation.
    :param base: base of the positional numeral system.
    :param zerofill_to_length: what is the minimum length that the list of digits should have.
    :param most_significant_digit_first: If True, positions are counted from the most significant digit.
    :return: list of digits that represent number in the positional notation system with given base.
    """
    if n!=int(n):
        raise TypeError("the number must be an integer.")
    digits=[]
    while n:
        digits=[n%base]+digits
        #digits.append(n%base)
        n//=base
    if len(digits)<zerofill_to_length:
        digits=[0]*(zerofill_to_length-len(digits))+digits
        #digits+=[0]*(zerofill_to_length-len(digits))
    #digits.reverse()
    if not most_signicant_digit_first:
        digits.reverse()
    return digits
def list_of_digits_to_number(digits,base,most_signicant_digit_first=False):
    """
    :param digits: list of digits that represent number in a positional numeral system.
    :param base: base of the positional numeral system.
    :param most_significant_digit_first: If True, positions are counted from the most significant digit.
    :return: the number that is represented with given the digits in the given base.
    """
    n=0
    m=1
    if most_signicant_digit_first:
        for i_digit in range(len(digits)-1,0,-1):
            n+=m*digits[i_digit]
            m*=base
        if digits:
            n+=m*digits[0]
    else:
        for i_digit in range(len(digits)-1):
            n+=m*digits[i_digit]
            m*=base
        if digits:
            n+=m*digits[-1]
    return n

def get_digit(number,base,position_of_the_digit,most_signicant_digit_first=False):
    """
    :param number: a number.
    :param base: base of the positional numeral system.
    :param position_of_the_digit: position of the digit in the positional numeral system.
    :param least_signicant_digit_first: Should the least significant digit be first or last in the returned list.
    :param most_significant_digit_first: If True, positions are counted from the most significant digit.
    :return: digit on postion position_of_the_digit in the positional notation of the number.
    """
    if most_signicant_digit_first:
        copy_of_the_number=number
        digits=-1
        while copy_of_the_number:
            digits+=1
            copy_of_the_number//=base
        if digits-position_of_the_digit>=0:
            return (number//base**(digits-position_of_the_digit))%base
        else:
            return (number*base**(position_of_the_digit-digits))%base
    else:
        if position_of_the_digit>=0:
            return (number//base**position_of_the_digit)%base
        else:
            return (number*base**(-position_of_the_digit))%base
def get_digit2(number,base,position_of_the_digit):
    """
    :param number: a number.
    :param base: base of the positional numeral system.
    :param position_of_the_digit: position of the digit in the positional numeral system.
    :return: digit on postion position_of_the_digit in the positional notation of the number.
    """
    m=base**position_of_the_digit
    return (number%(m*base))//m
def get_digit3(number,base,position_of_the_digit):
    """
    :param number: a number.
    :param base: base of the positional numeral system.
    :param position_of_the_digit: position of the digit in the positional numeral system.
    :return: digit on postion position_of_the_digit in the positional notation of the number.
    """
    for i in range(position_of_the_digit):
        number//=base
    return number%base