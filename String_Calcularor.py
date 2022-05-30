class StringCalculator:

    
    def __init__(self, list_example):
        self.list_example = list_example
        self.true_list = list()

#It needs for BOT. Without bot it can be commented    
    def clear_list(self):
        self.list_example = ""
        self.true_list = []

    def is_float(self, n):  #It is function for checking that value is float
        try:
            float(n)
        except ValueError:
            return False
        return True
    
    def string_to_list_with_numbers_and_opperands(self):  #it is function for transformation string to list
        self.list_example = self.list_example.replace(",", ".") #change , to .
        number = ""
        count = 0
        for i in self.list_example:

            if i == "0" and count == len(self.list_example) - 1:     
                self.true_list.append(i) #Add not digit to the list
                count = count + 1

            elif i == "0" and self.list_example[count+1].isdigit() and (self.list_example[count-1] == "+" or self.list_example[count-1] == "-" or self.list_example[count-1] == "*" or self.list_example[count-1] == "/"): #Return Error for situation f.e. 05
                return "Error 0"
        
            elif i.isdigit(): #If i is digit that temporary variable get value
                number = str(number) + i
                count = count + 1

            elif count == 0 and (i == "." or i == "+" or i == "-" or i == "*" or i == "/"): #Return error if first symbol is operand
                return "Error 1"

            elif count == len(self.list_example) - 1 and (i == "." or i == "+" or i == "-" or i == "*" or i == "/"): #Return Error if the last symbol is operand
                return "Error 2"

            elif i == "." and (self.list_example[count-1] == "." or self.list_example[count+1] == "."): #Return Error if there is double point at the string
                return "Error 3"

            elif i == "." and (self.list_example[count+1] == "+" or self.list_example[count+1] == "-" or self.list_example[count+1] == "*" or self.list_example[count+1] == "/"): #Return Error if after point there is the operand
                return "Error 4" 

            elif (i == "+" or i == "-" or i == "*" or i == "/") and (self.list_example[count+1] == "+" or self.list_example[count+1] == "-" or self.list_example[count+1] == "*" or self.list_example[count+1] == "/"): #Return Error if there is double operand
                return "Error 5"

            elif i == "." and self.list_example[count+1].isdigit():  #Make float digit
                number = str(number) + i
                count = count + 1

            else:
                self.true_list.append(number) #Add digit to the list
                number = ""       
                self.true_list.append(i) #Add not digit to the list
                count = count + 1

        if number != "":
            self.true_list.append(number) #if digit is the last symbol at the string
        
        if len(self.true_list) < 3:    #Check: list has minimum 3 symbols
            return "Error 6" 

        return self.true_list

    def check_allow_symbols(self):  #Function for checking the list
        if (self.true_list[0].isdigit() or self.is_float(self.true_list[0])) and (self.true_list[len(self.true_list)-1].isdigit() or self.is_float(self.true_list[len(self.true_list)-1])):  #Check first and the last symbol they must be a numbers

            allow_symbols = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "+", "-", "*", "/", "."]   #Allow symbols at the list
            allow = False  #flag for unrnown symbols
            unknown_symbols = list()
            count = 0

            for i in self.true_list: #i - value at the list 

                if i == "0" and self.true_list[count-1] == "/":  #Must not divide on the zero
                    return "Error 7"

                for l in list(i):  #l - symbol at the i value

                    for j in allow_symbols: #j - allow symbol

                        if j == l: #If all symbols (l) is in the allow symbols list: allow flag = True
                            allow = True

                    if allow == False: #Add unknown symbols to the list
                        unknown_symbols.append(l)

                    allow = False #Change flag at the end of iteration 

                count = count + 1

            if len(unknown_symbols) != 0: #Return unknown symbols
                return unknown_symbols 

        else: #Return Error if the first or the last symbols is not digit
            return "Error 8" 

    def first_priority_actions(self, true_list): #Creating a list with computed multiplication and division values
        self.true_list = true_list
        value_first_priority = 0 #Result of operation multiplication and division
        count = 0
        stay = 0 #Index for insert a result of multiplication or division

        for i in self.true_list: 

            if (i.isdigit() or self.is_float(i)) and (self.true_list[count-1] == "+" or self.true_list[count-1] == "-") and count == len(self.true_list)-1: #If the last opperand is + or -
                break

            elif (i.isdigit() or self.is_float(i)) and (self.true_list[count-1] == "*" or self.true_list[count-1] == "/") and count == len(self.true_list)-1: #If the last opperand is * or /

                if self.true_list[count-1] == "/":

                    if i.isdigit():
                        value_first_priority = value_first_priority / int(self.true_list.pop(count))

                    else:
                        value_first_priority = value_first_priority / float(self.true_list.pop(count))

                elif self.true_list[count-1] == "*":

                    if i.isdigit():
                        value_first_priority = value_first_priority * int(self.true_list.pop(count))

                    else:
                        value_first_priority = value_first_priority * float(self.true_list.pop(count))
    
                self.true_list.pop(count-1)
                self.true_list.insert(stay, str(value_first_priority))
                stay = 0 #when we insert value, index is zero again
                value_first_priority = 0
                count = count

            elif (i.isdigit() or self.is_float(i)) and (self.true_list[count+1] == "+" or self.true_list[count+1] == "-") and count == 0: #If the first opperand is + or -
                count = count + 1
                continue

            elif (i.isdigit() or self.is_float(i)) and (self.true_list[count+1] == "*" or self.true_list[count+1] == "/") and count == 0: #If the first opperand is * or /

                if i.isdigit():
                    value_first_priority = int(self.true_list.pop(count))

                else:
                    value_first_priority = float(self.true_list.pop(count))

                stay = count
                count = count + 1
        
            elif (i.isdigit() or self.is_float(i)) and (self.true_list[count+1] == "+" or self.true_list[count+1] == "-") and (self.true_list[count-1] == "+" or self.true_list[count-1] == "-"):
                count = count + 1
                continue

            elif (i.isdigit() or self.is_float(i)) and (self.true_list[count-1] == "+" or self.true_list[count-1] == "-") and (self.true_list[count+1] == "*" or self.true_list[count+1] == "/"):

                if i.isdigit():
                    value_first_priority = int(self.true_list.pop(count))

                else:
                    value_first_priority = float(self.true_list.pop(count))

                stay = count
                count = count + 1

            elif (i.isdigit() or self.is_float(i)) and (self.true_list[count-1] == "*" or self.true_list[count-1] == "/") and (self.true_list[count+1] == "*" or self.true_list[count+1] == "/"):

                if self.true_list[count-1] == "/":

                    if i.isdigit():
                        value_first_priority = value_first_priority / int(self.true_list.pop(count))

                    else:
                        value_first_priority = value_first_priority / float(self.true_list.pop(count))

                elif self.true_list[count-1] == "*":

                    if i.isdigit():
                        value_first_priority = value_first_priority * int(self.true_list.pop(count))

                    else:
                        value_first_priority = value_first_priority * float(self.true_list.pop(count))
         
                self.true_list.pop(count-1)
                self.true_list.insert(stay, str(value_first_priority))
                stay = 0
                value_first_priority = 0
                count = count
    
            elif (i.isdigit() or self.is_float(i)) and (self.true_list[count-1] == "*" or self.true_list[count-1] == "/") and (self.true_list[count+1] == "+" or self.true_list[count+1] == "-"):

                if self.true_list[count-1] == "/":

                    if i.isdigit():
                        value_first_priority = value_first_priority / int(self.true_list.pop(count))

                    else:
                        value_first_priority = value_first_priority / float(self.true_list.pop(count))

                elif self.true_list[count-1] == "*":

                    if i.isdigit():
                        value_first_priority = value_first_priority * int(self.true_list.pop(count))

                    else:
                        value_first_priority = value_first_priority * float(self.true_list.pop(count))
      
                self.true_list.pop(count-1)
                self.true_list.insert(stay, str(value_first_priority))
                stay = 0
                value_first_priority = 0
                count = count + 1

            else:
                count = count + 1

        if "*" in self.true_list:
            return self.first_priority_actions(self.true_list) #Python cannot completely change the list while it is in a loop, so we use recursion  

        elif "/" in self.true_list:
            return self.first_priority_actions(self.true_list)

        else:
            return self.true_list

    def second_priority_actions(self, list_example): #Computing addition and subtraction
        count = 0
        result = 0

        for i in list_example:

            if (i.isdigit() or self.is_float(i)) and count == 0:  #all actions are like for first_priority_actions method

                if i.isdigit():
                    result = int(i)

                elif self.is_float(i):
                    result = float(i)

                count = count + 1
                continue

            elif (i.isdigit() or self.is_float(i)) and list_example[count-1] == "+" and count == len(list_example) - 1:

                if i.isdigit():
                    result = result + int(i)

                else:
                    result = result + float(i)

                return result

            elif (i.isdigit() or self.is_float(i)) and list_example[count-1] == "-" and count == len(list_example) - 1:

                if i.isdigit():
                    result = result - int(i)

                else:
                    result = result - float(i)

                return result

            elif (i.isdigit() or self.is_float(i)) and list_example[count-1] == "+":

                if i.isdigit():
                    result = result + int(i)

                else:
                    result = result + float(i)

            elif (i.isdigit() or self.is_float(i)) and list_example[count-1] == "-":

                if i.isdigit():
                    result = result - int(i)

                else:
                    result = result - float(i)
                    
            count = count + 1

    def calculate(self):
        result_of_string_to_the_list = self.string_to_list_with_numbers_and_opperands()
        if result_of_string_to_the_list == "Error 1":
            return "The first symbol must be digit, please reenter"

        elif result_of_string_to_the_list == "Error 2":
            return "The last symbol must be digit, please reenter"

        elif result_of_string_to_the_list == "Error 3":
            return "You entered double point, please reenter"

        elif result_of_string_to_the_list == "Error 4":
            return "You entered opperand after point, please reenter"

        elif result_of_string_to_the_list == "Error 5":
            return "You entered double opperand, please reenter"

        elif result_of_string_to_the_list == "Error 6":
            return "You entered entered less then 3 symbols, please reenter"

        elif result_of_string_to_the_list == "Error 0":
            return "You entered entered zero befor digit without point, please reenter"
        
        else:
            result_of_checking = self.check_allow_symbols()
            if result_of_checking == "Error 7":
                return "Can not divide on Zero"
            
            elif result_of_checking == "Error 8":
                return "The first or the last symbol is not digit"

            elif result_of_checking == None:
                result_of_first_priotity_actions = self.first_priority_actions(self.true_list)
                if len(result_of_first_priotity_actions) != 1:
                    result_of_second_priority_actions = self.second_priority_actions(self.true_list)
                    return f"Result: {result_of_second_priority_actions}"
                else:
                    return f"Result: {result_of_first_priotity_actions}"
            
            else:
                return f"You entered unknown symbols: {result_of_checking}, please reenter"

        

if __name__ == '__main__':
    a = StringCalculator(str(input("Enter your example: ")))
    print(a.calculate())
