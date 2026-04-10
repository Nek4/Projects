# Programm creator Nektarios Karagiannis
#client Vasileios Karaginnis
#The program is designed to save client data and estimate the average of many diferrent sums about 
# different injuries the programm will be used for research porpuses in wolrd company level
# Date 27/6/2022
# sum1, sum2 sum3, sum4, sum5, sum6, sum7, sum8, sum9, Ειναι int πληθοι για τραυματισμους


print ("Hello Sir!")
print ("would you like to continue?")
Answer = input("")

    
if Answer == "true":
    
    print("is The patient already registered????")
    PS = input ("")#patients status. if he is already listed
    if PS == "no":
        print("please state the patients name")
        NASU = input("")#NASU=NAME AND SURNAME

        print ("State the patients birth date")
        PABI = input()#PABI= PATIENTS BIRTH DATE

        print ("State the patients gemder")
        PAGE =  input("")#PAGE= PATIENTS GENDER

        print ("state your Diagnosis")
        PADI = input("")#PADI= PATIENTS DIAGNOSIS

        print("injury protocol")
        INPR = input("")#INPR= INJURY PROTOCOL

        print ("State where the injury is located")
        INLO = input("")#INLO =INJURY LOCATION

        NUVI = input("Whats the current number of visitations?")#NUVI= NYMBER OF VISITATIONS

    else :

        NASU = input ("Please state the patients name and surname")#name and surname


    if INLO=="Lumbar collumn":
        sum1+=1 

    elif  INLO is "Shoulder":
        sum2+=1

    elif INLO == "Elbow":
        sum3+=1

    elif INLO == "Wrist":
        sum4+=1

    elif INLO == "Fingers":
        sum5+=1

    elif INLO == "Knee":
        sum6+=1

    elif INLO == "Toes":
        sum7+=1

    elif INLO == "Hip":
        sum8+=1

    else : #Neck
        sum9+=1





