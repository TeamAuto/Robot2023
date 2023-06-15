""" Auteur: Luca Freund
    Date:   23.02.2023

    Ce code permet de communiquer avec les servos dynamixel
"""

#Définition des Library
import pyads
import time
from TeamAuto_PyADS_Module import *
from dynamixel_sdk import *
from TeamAuto_U2D2_Module import *

#Declaration de variable utiles
DoneInfo = False
MoveInit = False
DoneHoming = False
AttendRun = False
HomingPosition0 = False
Move = 0
CodeErreur = 0
Erreur = 0

plc = Plc()
Servo = Dxl()

#Connection à l'automate + lecture de l'etat actuelle
plc.Connection("XXX.XXX.XXX.XXX.XXX.XXX")
Etat_PLC = plc.EtatActuelle()
MachineState, ADSErreur = Etat_PLC

if ADSErreur != 0 or MachineState != 5:
    print("Erreur")

#Creation des listes pour la lecture et écriture des variables sur l'automate
NomServoList = ["ServoGateauxDevant", "ServoGateauxMillieu", "ServoGateauxArriere", "ServoTuyeauG", "ServoTuyeauD", "ServoDeposeCerise", "ServoStockage", "ServoOuvertureAvantGauche", "ServoOuvertureAvantDroite", "ServoOuvertureArriereGauche", "ServoOuvertureArriereDroite"]
ListValeurNom = plc.CreationVariableList("ServoDynamixel", NomServoList)
Nom_ID, Nom_ModeRotation, Nom_PosMin, Nom_PosMax, Nom_PosInit, Nom_MoveInit, Nom_HomingONOFF, Nom_HomingBasHaut, Nom_CapteurHoming, Nom_VitesseHoming, Nom_ForceHoming, Nom_PositionApresHoming, Nom_MoveRun, Nom_ModeRun, Nom_Prioritaire, Nom_PositionOrdre, Nom_Vitesse, Nom_Syncro, Nom_Force, Nom_PositionReel, Nom_Position0, Nom_HomingDone, Nom_Etat, Nom_CodeErreur, Nom_Movement, Nom_EnCycle = ListValeurNom

#Définition de multiple variable
Val_PosInit = [0 for i in range((len(Nom_ID)))]
Val_PosInitStock =  [0 for i in range((len(Nom_ID)))]
Val_Move = [0 for i in range((len(Nom_ID)))]
Val_Force = [0 for i in range((len(Nom_ID)))]
Val_MoveRun = [0 for i in range((len(Nom_ID)))]
Val_HomingBasHaut = [0 for i in range((len(Nom_ID)))]
Val_VitesseHoming = [0 for i in range((len(Nom_ID)))]
Val_ForceHoming = [0 for i in range((len(Nom_ID)))]
Val_PositionApresHoming = [0 for i in range((len(Nom_ID)))]
Val_PositionOrdre = [0 for i in range((len(Nom_ID)))]
Val_PositionReel = [0 for i in range((len(Nom_ID)))]
Val_PositionHomingMin = [0 for i in range((len(Nom_ID)))]
Val_ModeRun = [0 for i in range((len(Nom_ID)))]
Val_PositionOrdrePrecedent = [0 for i in range((len(Nom_ID)))]
Val_CodeErreur = [0 for i in range((len(Nom_ID)))]
Val_Syncro = [False for i in range((len(Nom_ID)))]
Val_Prioritaire = [False for i in range((len(Nom_ID)))]
Val_MoveRun = [False for i in range((len(Nom_ID)))]
Val_HomingDone = [False for i in range((len(Nom_ID)))]
Val_CapteurHoming = [False for i in range((len(Nom_ID)))]
Val_MovePrecedent = [False for i in range((len(Nom_ID)))]


Val_EnCycle = plc.Lit_Variable_List_Bool(Nom_EnCycle)

while Val_EnCycle[0]:

    Val_EnCycle = plc.Lit_Variable_List_Bool(Nom_EnCycle)
    Val_Etat = plc.Lit_Variable_List_Int(Nom_Etat)

    if Val_Etat[0] == 0:
    #Etat Init
        print("Etat Init")
    if Val_Etat[0] == 10:
    #Etat PreSetup, Lit la position actuelle du Servo
        print("Etat PreSetup")
        Val_ID = plc.Lit_Variable_List_Int(Nom_ID)
        Erreur, Val_PositionReel = Servo.LirePostionList(Val_ID)
        Val_Nom_PositionReel = plc.FusionNomValeur(Nom_PositionReel, Val_PositionReel)
        plc.Ecrit_Variable_List(Val_Nom_PositionReel)
        Val_Etat = [20 for i in range((len(Nom_ID)))]
        Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
        plc.Ecrit_Variable_List(Val_Nom_Etat)

    if Val_Etat[0] == 20:
    #Etat Setup, Lit les différents reglages définit sur l'automate et écrit sur les servos
        print("Etat Setup")
        Val_ModeRotation = plc.Lit_Variable_List_Int(Nom_ModeRotation)
        Val_PosMin = plc.Lit_Variable_List_Int(Nom_PosMin)
        Val_PosMax = plc.Lit_Variable_List_Int(Nom_PosMax)
        for i in range(len(Val_ID)):
            Erreur = Servo.TorqueOFF(Val_ID[i])
        for i in range(len(Val_ID)):
            Erreur = Servo.ModeRot(Val_ID[i], Val_ModeRotation[i])
            Erreur = Servo.PositionMin(Val_ID[i], Val_PosMin[i])
            Erreur = Servo.PositionMax(Val_ID[i], Val_PosMax[i])
	for i in range(len(Val_ID)):
            Erreur = Servo.TorqueON(Val_ID[i])

        Val_Etat = [30 for i in range((len(Nom_ID)))]
        Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
        plc.Ecrit_Variable_List(Val_Nom_Etat)

    if Val_Etat[0] == 30:
    #Position Init, mouvement en relatif, (Ne connait pas le point 0) + retourne info importante des servos à l'automate (Force, Position Reel et si le servo est en mouvement)
        print("Position Init")
        if DoneInfo == False:
            Val_Vitesse = plc.Lit_Variable_List_Int(Nom_Vitesse)
            for i in range(len(Val_ID)):
                Val_PosInit[i] = plc.Lit_Variable(Nom_PosInit[i])
                Val_PosInitStock[i] = Val_PositionReel[i] + Val_PosInit[i]
                print(Val_PosInit[i])
                Erreur = Servo.EcrireVitesse(Val_ID[i], Val_Vitesse[i])
                Erreur = Servo.StockPosition(Val_ID[i], Val_PosInitStock[i])
            DoneInfo = True
        elif DoneInfo == True:
            Val_MoveInit = plc.Lit_Variable(Nom_MoveInit[0])
            print(Val_MoveInit)
            if Val_MoveInit == True:
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
                        Val_Etat = [35 for i in range((len(Nom_ID)))]
                        Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
                        plc.Ecrit_Variable_List(Val_Nom_Etat)

    if Val_Etat[0] == 35:
    #Homing, Définit le point 0 pour les servos en multi-turn, il y a 4 sortes d'homing différents:
    # Homing 10: Homing Sens Horaire, Homing Force, dès que le servo dépasse la force max définie, le servo s'arrête, le point 0 est définit
    # Homing 15: Homing Sens Horaire, Attend que le capteur homing soit à 1, cette information est lue sur l'automate
    # Homing 20: Homing Sens Anti-Horaire, Homing Force, dès que le servo dépasse la force max définie, le servo s'arrête, le point 0 est définit
    # Homing 25: Homing Sens Anti-Horaire, Attend que le capteur homing soit à 1, cette information est lue sur l'automate
    # Après avoir réaliser l'homing le servo va effectuer un mouvement.
    # PS: L'optimisation du code arrive avec la prochaine version
        Val_MoveRun[0] = plc.Lit_Variable(Nom_MoveRun[0])
        print("Homing")
        print(Val_MoveRun[0])
        print(AttendRun)
        if AttendRun == True and Val_MoveRun[0] == True:
            time.sleep(0.5)
            Val_Etat = [40 for i in range((len(Nom_ID)))]
            Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
            plc.Ecrit_Variable_List(Val_Nom_Etat)
        elif not AttendRun:
            for i in range(len(Val_ID)):
                Val_HomingONOFF = plc.Lit_Variable(Nom_HomingONOFF[i])
                if i == len(Val_ID) -1:
                    print("Fin Homing")
                    AttendRun = True
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
                            print(Val_Force[i])
                            print(Val_ForceHoming[i])
                            if Val_Force[i] > Val_ForceHoming[i] and not Val_Force[i] > 60000:
                                HomingPosition0 = True
                                print("je suis 10")

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
                            if Val_Force[i] < Val_ForceHoming[i] and not Val_Force[i] < -60000:
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
    # Mode Run
    # Lecture Automate (Mode de Rotation, Position Ordre, Vitesse, Mode Syncro):
    # Ecriture sur les servos (Position Ordre, Vitesse)
    # Lecture sur les servos (Position Réel, Force, En mouvement?)
    # Ecriture sur l'automate (Position Réel, Force, En mouvement?)
    # 3 modes de rotation différents :
    #   1: Seulement le servo qui est en rotation est interogé
    #   2: Servo avec la variable bPrioritaire sont interogé
    #   3: Chaque servo est interogé (Très lent 70ms par servo)
    #   PS: optimisation arrive avec la prochaine version
        print("Run")
        Val_ModeRun = plc.Lit_Variable_List_Int(Nom_ModeRun)
        print(Val_ModeRun[0])
        if Val_ModeRun[0] == 3:
            Val_Syncro[i] = plc.Lit_Variable_List_Bool(Nom_Syncro)
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


        elif Val_ModeRun[0] == 2:
            for i in range(len(Val_ID)):
                Val_Prioritaire[i] = plc.Lit_Variable(Nom_Prioritaire[i])
                if Val_Prioritaire[i] == True:
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


        elif Val_ModeRun[0] == 1:
            for i in range(len(Val_ID)):
                Val_PositionOrdre[i] = plc.Lit_Variable(Nom_PositionOrdre[i])
                Erreur, Val_Move[i] = Servo.EnMouvement(Val_ID[i])

                if Val_PositionOrdre[i] != Val_PositionOrdrePrecedent[i] or Val_Move[i] == True or Val_MovePrecedent[i] == True:
                    Val_Vitesse[i] = plc.Lit_Variable(Nom_Vitesse[i])

                    Erreur = Servo.EcrireVitesse(Val_ID[i], Val_Vitesse[i])
                    Erreur = Servo.PositionGoal(Val_ID[i], Val_PositionOrdre[i])

                    Erreur, Val_Move[i] = Servo.EnMouvement(Val_ID[i])
                    Erreur, Val_PositionReel[i] = Servo.LirePosition(Val_ID[i])
                    Erreur, Val_Force[i] = Servo.ForceActuelle(Val_ID[i])

                    plc.Ecrit_Variable(Nom_Movement[i], Val_Move[i])
                    plc.Ecrit_Variable(Nom_PositionReel[i], Val_PositionReel[i])
                    plc.Ecrit_Variable(Nom_Force[i], Val_Force[i])

                    Val_PositionOrdrePrecedent[i] = Val_PositionOrdre[i]
                    Val_MovePrecedent[i] = Val_Move[i]

    if Val_Etat[0] == 50 or Erreur == True:
    #Mode Stop/Erreur
        print("Stop/Erreur")
        if Erreur == True:
            CodeErreur = [10 for i in range((len(Nom_ID)))]
            Val_Nom_Etat = plc.FusionNomValeur(Nom_Etat, Val_Etat)
            plc.Ecrit_Variable_List(Val_Nom_Etat)

    if Val_Etat[0] == 60:
    #Mode Fin Match
        print("Fin du Match")
	for i in range(len(Val_ID)):
       		Servo.TorqueOFF(Val_ID)
        Servo.FermeturePort()
else:
    print("Erreur Inconue, boucle while generale ce lance pas")
