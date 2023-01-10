import pyads
import time
from TeamAuto_PyADS_Module import *
from dynamixel_sdk import *
from TeamAuto_U2D2_Module import *

#Declaration de variable utiles
DoneInfo = False
MoveInit = False
DoneHoming = False
HomingPosition0 = False
Move = 0
time2 = 0
Val_Move = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Val_PosInitStock = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Val_Force = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Val_HomingBasHaut = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Val_VitesseHoming = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Val_ForceHoming = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Val_PositionApresHoming = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Val_PositionOrdre = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Val_HomingDone = [False, False, False, False, False, False, False, False, False, False, False]
Val_CapteurHoming = [False, False, False, False, False, False, False, False, False, False, False]
Val_Force = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Val_PositionHomingMin = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

plc = Plc()
Servo = Dxl()

plc.Connection("172.18.234.80.1.1")
Etat_PLC = plc.EtatActuelle()
MachineState, ADSErreur = Etat_PLC

if ADSErreur != 0 or MachineState != 5:
    print("Erreur")

NomServoList = ["ServoGateauxDevant", "ServoGateauxMillieu", "ServoGateauxArriere", "ServoTuyeauG", "ServoTuyeauD", "ServoDeposeCerise", "ServoStockage", "ServoOuvertureAvantGauche", "ServoOuvertureAvantDroite", "ServoOuvertureArriereGauche", "ServoOuvertureArriereDroite"]
ListValeurNom = plc.CreationVariableList("ServoDynamixel", NomServoList)
Nom_ID, Nom_ModeRotation, Nom_PosMin, Nom_PosMax, Nom_PosInit, Nom_MoveInit, Nom_HomingONOFF, Nom_HomingBasHaut, Nom_CapteurHoming, Nom_VitesseHoming, Nom_ForceHoming, Nom_PositionApresHoming, Nom_MoveRun, Nom_PositionOrdre, Nom_Vitesse, Nom_Syncro, Nom_Force, Nom_PositionReel, Nom_Position0, Nom_HomingDone, Nom_Etat, Nom_CodeErreur, Nom_Movement, Nom_EnCycle = ListValeurNom
print(Nom_CapteurHoming)

Val_EnCycle = plc.Lit_Variable_List_Bool(Nom_EnCycle)

while Val_EnCycle[0]:

    Val_EnCycle = plc.Lit_Variable_List_Bool(Nom_EnCycle)
    Val_Etat = plc.Lit_Variable_List_Int(Nom_Etat)

    if Val_Etat[0] == 0:
    #Etat Init
        print("Etat Init")
    if Val_Etat[0] == 10:
    #Etat PreSetup
        print("Etat PreSetup")
        Val_ID = plc.Lit_Variable_List_Int(Nom_ID)
        Erreur, Val_PositionReel = Servo.LirePostionList(Val_ID)
        Val_Nom_PositionReel = plc.FusionNomValeur(Nom_PositionReel, Val_PositionReel)
        plc.Ecrit_Variable_List(Val_Nom_PositionReel)

        Val_Etat = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
        Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
        plc.Ecrit_Variable_List(Val_Nom_Etat)
    if Val_Etat[0] == 20:
    #Etat Setup
        print("Etat Setup")
        Val_ModeRotation = plc.Lit_Variable_List_Int(Nom_ModeRotation)
        Val_PosMin = plc.Lit_Variable_List_Int(Nom_PosMin)
        Val_PosMax = plc.Lit_Variable_List_Int(Nom_PosMax)
        for i in range(len(Val_ID)):
            Erreur = Servo.TorqueOFF(Val_ID[i])
            Erreur = Servo.ModeRot(Val_ID[i], Val_ModeRotation[i])
            Erreur = Servo.PositionMin(Val_ID[i], Val_PosMin[i])
            Erreur = Servo.PositionMax(Val_ID[i], Val_PosMax[i])
            Erreur = Servo.TorqueON(Val_ID[i])

        Val_Etat = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
        Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
        plc.Ecrit_Variable_List(Val_Nom_Etat)

    if Val_Etat[0] == 30:
    #Position Init
        print("Position Init")
        if DoneInfo == False:
            Val_Vitesse = plc.Lit_Variable_List_Int(Nom_Vitesse)
            Val_PosInit = plc.Lit_Variable_List_Int(Nom_PosInit)

            for i in range(len(Val_ID)):
                Val_PosInitStock[i] = Val_PositionReel[i] + Val_PosInit[i]
                Erreur = Servo.EcrireVitesse(Val_ID[i], Val_Vitesse[i])
                Erreur = Servo.StockPosition(Val_ID[i], Val_PosInitStock[i])
            print(Val_PosInitStock)
            DoneInfo = True
        elif DoneInfo == True:
            Val_MoveInit = plc.Lit_Variable(Nom_MoveInit[0])
            print(Val_MoveInit)
            if Val_MoveInit == True:
                print(Val_MoveInit)
                print("je suis la.........................")
                Erreur = Servo.MoveSyncro()
                time.sleep(0.1)
                while not MoveInit:
                    for i in range(len(Val_ID)):
                        Erreur, Val_Move[i] = Servo.EnMouvement(Val_ID[i])
                        print(Val_Move[i])
                        Erreur, Val_PositionReel[i] = Servo.LirePosition(Val_ID[i])
                        Erreur, Val_Force[i] = Servo.ForceActuelle(Val_ID[i])
                        plc.Ecrit_Variable(Nom_Movement[i], Val_Move[i])
                        plc.Ecrit_Variable(Nom_PositionReel[i], Val_PositionReel[i])
                        plc.Ecrit_Variable(Nom_Force[i], Val_Force[i])
                    print(Val_Move)
                    if all(val == 0 for val in Val_Move):
                        print("je suis la")
                        MoveInit = True
                        Val_Etat = [35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35]
                        Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
                        plc.Ecrit_Variable_List(Val_Nom_Etat)


    if Val_Etat[0] == 35:
    #Homing
        time.sleep(0.5)
        print("Homing")
        for i in range(len(Val_ID)):
            Val_HomingONOFF = plc.Lit_Variable(Nom_HomingONOFF[i])
            if i == len(Val_ID) -1:
                print("Fin Homing")
                Val_Etat = [40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40]
                Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
                plc.Ecrit_Variable_List(Val_Nom_Etat)
            if Val_HomingONOFF == True:
                Val_HomingBasHaut[i] = plc.Lit_Variable(Nom_HomingBasHaut[i])
                Val_VitesseHoming[i] = plc.Lit_Variable(Nom_VitesseHoming[i])
                Val_ForceHoming[i] = plc.Lit_Variable(Nom_ForceHoming[i])
                Val_PositionApresHoming[i] = plc.Lit_Variable(Nom_PositionApresHoming[i])

                Erreur, Val_PositionReel[i] = Servo.LirePosition(Val_ID[i])
                Erreur = Servo.EcrireVitesse(Val_ID[i], Val_VitesseHoming[i])

                if Val_HomingBasHaut[i] == 10 or Val_HomingBasHaut[i] == 15:
                    Val_PositionOrdre[i] = Val_PositionReel[i] + 100000
                if Val_HomingBasHaut[i] == 20 or Val_HomingBasHaut[i] == 25:
                    Val_PositionOrdre[i] = Val_PositionReel[i] - 100000

                Erreur = Servo.PositionGoal(Val_ID[i], Val_PositionOrdre[i])

                while not Val_HomingDone[i]:
                    if Val_HomingBasHaut[i] == 10:
                        Val_Force[i] = 0
                        Erreur, Val_Force[i] = Servo.ForceActuelle(Val_ID[i])
                        if Val_Force[i] > Val_ForceHoming[i]:
                            HomingPosition0 = True

                    if Val_HomingBasHaut[i] == 15:
                        Val_Force[i] = 0
                        Val_CapteurHoming[i] = plc.Lit_Variable(Nom_CapteurHoming[i])
                        if Val_CapteurHoming[i] == True:
                            HomingPosition0 = True

                    if Val_HomingBasHaut[i] == 20:
                        Val_Force[i] = 65535
                        Erreur, Val_Force[i] = Servo.ForceActuelle(Val_ID[i])
                        Val_Force[i] = Val_Force[i] - 65535
                        print(Val_Force[i])
                        print(Val_ForceHoming[i])
                        if Val_Force[i] < Val_ForceHoming[i]:
                            HomingPosition0 = True
                            print("je suis 20")

                    if Val_HomingBasHaut[i] == 25:
                        Val_Force[i] = 65535
                        Val_CapteurHoming[i] = plc.Lit_Variable(Nom_CapteurHoming[i])
                        if Val_CapteurHoming[i] == True:
                            HomingPosition0 = True


                    while not Val_HomingDone[i] and HomingPosition0:
                        print("Move Init")
                        Erreur, Val_PositionReel[i] = Servo.LirePosition(Val_ID[i])
                        Val_PositionOrdre[i] = Val_PositionReel[i]
                        Val_PositionHomingMin[i] = Val_PositionReel[i]
                        Erreur = Servo.PositionGoal(Val_ID[i], Val_PositionOrdre[i])
                        if Val_HomingBasHaut[i] == 10 or Val_HomingBasHaut[i] == 15:
                            Val_PositionApresHoming[i] = Val_PositionApresHoming[i] *-1
                        Val_PositionOrdre[i] = Val_PositionReel[i] + Val_PositionApresHoming[i]
                        Erreur = Servo.EcrireVitesse(Val_ID[i], Val_Vitesse[i])
                        Erreur = Servo.PositionGoal(Val_ID[i], Val_PositionOrdre[i])
                        HomingPosition0 = False
                        Val_HomingDone[i] = True
                        plc.Ecrit_Variable(Nom_Position0[i], Val_PositionHomingMin[i])
                        plc.Ecrit_Variable(Nom_HomingDone[i], Val_HomingDone[i])

    if Val_Etat[0] == 40:
    #Mode Run
        print("Run")
        time2 = time2 + 1
        print(time2)
        Val_Syncro = plc.Lit_Variable_List_Bool(Nom_Syncro)
        if Val_Syncro[0]:
            #Mode Syncro
            for i in range(len(Val_ID)):
                Val_Vitesse[i] = plc.Lit_Variable(Nom_Vitesse[i])
                Val_PositionOrdre[i] = plc.Lit_Variable(Nom_PositionOrdre[i])

                Erreur = Servo.EcrireVitesse(Val_ID[i], Val_Vitesse[i])
                Erreur = Servo.StockPosition(Val_ID[i], Val_PositionOrdre[i])

            Erreur = Servo.MoveSyncro()

            for i in range(len(Val_ID)):
                Erreur, Val_Move[i] = Servo.EnMouvement(Val_ID[i])
                Erreur, Val_PositionReel[i] = Servo.LirePosition(Val_ID[i])
                Erreur, Val_Force[i] = Servo.ForceActuelle(Val_ID[i])

                plc.Ecrit_Variable(Nom_Movement[i], Val_Move[i])
                plc.Ecrit_Variable(Nom_PositionReel[i], Val_PositionReel[i])
                plc.Ecrit_Variable(Nom_Force[i], Val_Force[i])

        elif not Val_Syncro[0]:
            #Mode Normal
            for i in range(len(Val_ID)):
                Val_PositionOrdre[i] = plc.Lit_Variable(Nom_PositionOrdre[i])
                Val_Vitesse[i] = plc.Lit_Variable(Nom_Vitesse[i])

                Erreur = Servo.EcrireVitesse(Val_ID[i], Val_Vitesse[i])
                Erreur = Servo.PositionGoal(Val_ID[i], Val_PositionOrdre[i])

                Erreur, Val_Move[i] = Servo.EnMouvement(Val_ID[i])
                Erreur, Val_PositionReel[i] = Servo.LirePosition(Val_ID[i])
                Erreur, Val_Force[i] = Servo.ForceActuelle(Val_ID[i])

                plc.Ecrit_Variable(Nom_Movement[i], Val_Move[i])
                plc.Ecrit_Variable(Nom_PositionReel[i], Val_PositionReel[i])
                plc.Ecrit_Variable(Nom_Force[i], Val_Force[i])

    if Val_Etat[0] == 50:
    #Mode Stop/Erreur
        print("Stop/Erreur")
    if Val_Etat[0] == 60:
    #Mode Fin Match
        print("Fin du Match")
        portHandler.closePort()
else:
    print("ta foirer mon reuf")