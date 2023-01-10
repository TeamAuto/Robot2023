""" Auteur: Luca Freund
    Date:   14.12.2022

    Ce Moudule simplifie la communication entre l iPC et le code python
"""
import pyads
import time
import re
import ast
import json
"""
    Commande Simple pour l automate
"""
class Plc():
    def __init__(self):
        self.plc = None

    def Connection(self, AMSNETID):
        #Connection à l Ipc (AMSNETID ce trouve sur twincat3)
        self.plc = pyads.Connection(AMSNETID, pyads.PORT_TC3PLC1)
        self.plc.open()
        print(f"Connected?: {self.plc.is_open}")
        print(f"Local Address? : {self.plc.get_local_address()}")
        return

    def EtatActuelle(self):
        #Regarde etat actuelle ipc (5,0 est normal)
        retour = self.plc.read_state()
        return retour

    def Lit_Variable(self, Nom):
        #Lit une variable specifique
        Valeur = self.plc.read_by_name(Nom)
        return Valeur

    def Lit_Variable_List_Int(self, ListNom):
        #Lit une liste de variable et le stock dans un arrray
        # Ecrire en Amont (ListNom = ["Main.iTest", "Main.iTest2"])
        ListValeur = self.plc.read_list_by_name(ListNom)
        ListValeur = str(ListValeur)
        numbers = [int(x) for x in re.findall(r'\d+', ListValeur)]
        return numbers

    def Lit_Variable_List_Bool(self, ListNom):
        #Lit une liste de variable et le stock dans un arrray
        # Ecrire en Amont (ListNom = ["Main.iTest", "Main.iTest2"])
        ListValeur = self.plc.read_list_by_name(ListNom)
        ListValeur = str(ListValeur)
        data = ast.literal_eval(ListValeur)
        Liste = []
        for i in range(len(ListNom)):
            Liste.append(str((data[ListNom[i]])))
        return Liste

    def Ecrit_Variable(self, Nom, Valeur):
        #Ecrit une variable specifique
        self.plc.write_by_name(Nom, Valeur)
        return

    def Ecrit_Variable_List(self, ListNometVariable):
        #Ecrit une liste de Variable et Valeur en amont
        #test = 100
        #test1 = 3200
        #ListVariableValeur = {"Main.iTest": test, "Main.iTest2": test1}
        self.plc.write_list_by_name(ListNometVariable)
        return

    def CreationVariableList(self, NomPRG, NomServoList):
        # NomPRG = le nom ou les fbs des servo sont
        # Ecrire en Amont (NomServoList = ["ServoAvant", "ServoMillieu", ServoArriere])
        # Pour separer les differents variables utiliser sa : Nom_ID, Nom_ModeRotation, Nom_PosMin, Nom_PosMax, Nom_PosInit, Nom_Homing, Nom_HomingONOFF, Nom_HomingBasHaut, Nom_CapteurHoming, Nom_VitesseHoming, Nom_ForceHoming, Nom_MoveRun, Nom_PositionOrdre, Nom_Vitesse, Nom_Syncro, Nom_Force, Nom_PositionReel, Nom_Position0, Nom_HomingDone, Nom_Etat, Nom_CodeErreur, Nom_Movement = Nom_ListVariablesALL
        LongeurList = len(NomServoList)
        Nom_ID, Nom_ModeRotation, Nom_PosMin, Nom_PosMax, Nom_PosInit, Nom_Homing, Nom_HomingONOFF, Nom_HomingBasHaut, Nom_CapteurHoming, Nom_VitesseHoming, Nom_ForceHoming, Nom_PositionApresHoming, Nom_MoveRun, Nom_PositionOrdre, Nom_Vitesse, Nom_Syncro, Nom_Force, Nom_PositionReel, Nom_Position0, Nom_HomingDone, Nom_Etat, Nom_CodeErreur, Nom_Movement, Nom_EnCycle = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]

        for i in range(LongeurList):
            Nom_ID = Nom_ID + [NomPRG + "." + NomServoList[i] + "." + "iID"]
            Nom_ModeRotation = Nom_ModeRotation + [NomPRG + "." + NomServoList [i] + "." +"iModeRotation"]
            Nom_PosMin = Nom_PosMin + [NomPRG + "." + NomServoList [i] + "." +"iPositionMin"]
            Nom_PosMax = Nom_PosMax + [NomPRG + "." + NomServoList [i] + "." +"iPositionMax"]
            Nom_PosInit = Nom_PosInit + [NomPRG + "." + NomServoList [i] + "." + "diPositionInit"]
            Nom_Homing = Nom_Homing + [NomPRG + "." + NomServoList [i] + "." + "bHoming"]
            Nom_HomingONOFF = Nom_HomingONOFF + [NomPRG + "." + NomServoList [i] + "." + "bHomingONOFF"]
            Nom_HomingBasHaut = Nom_HomingBasHaut + [NomPRG + "." + NomServoList [i] + "." + "iHomingBasHaut"]
            Nom_CapteurHoming = Nom_CapteurHoming + [NomPRG + "." + NomServoList [i] +  "." +"bCANHoming"]
            Nom_VitesseHoming = Nom_VitesseHoming + [NomPRG + "." + NomServoList [i] +  "." +"iVitesseHoming"]
            Nom_ForceHoming = Nom_ForceHoming + [NomPRG + "." + NomServoList [i] +  "." +"iForceHoming"]
            Nom_PositionApresHoming = Nom_PositionApresHoming + [NomPRG + "." + NomServoList [i] + "." + "diPositionApresHoming"]
            Nom_MoveRun = Nom_MoveRun + [NomPRG + "." + NomServoList [i] + "." + "bMoveRun"]
            Nom_PositionOrdre = Nom_PositionOrdre + [NomPRG + "." + NomServoList [i] + "." + "diPositionOrdre"]
            Nom_Vitesse = Nom_Vitesse + [NomPRG + "." + NomServoList [i] + "." + "iVitesse"]
            Nom_Syncro = Nom_Syncro + [NomPRG + "." + NomServoList [i] + "." + "bSyncroMode"]
            Nom_Force = Nom_Force + [NomPRG + "." + NomServoList [i] + "." + "iForce"]
            Nom_PositionReel = Nom_PositionReel + [NomPRG + "." + NomServoList [i] + "." + "diPositionReel"]
            Nom_Position0 = Nom_Position0 + [NomPRG + "." + NomServoList [i] + "." + "diPosition0"]
            Nom_HomingDone = Nom_HomingDone + [NomPRG + "." + NomServoList [i] + "." + "bHomingDone"]
            Nom_Etat = Nom_Etat + [NomPRG + "." + NomServoList [i] + "." + "iEtatActuelle"]
            Nom_CodeErreur = Nom_CodeErreur + [NomPRG + "." + NomServoList [i] + "." + "iCodeErreur"]
            Nom_Movement = Nom_Movement + [NomPRG + "." + NomServoList [i] + "." + "bEnMouvement"]
            Nom_EnCycle =  Nom_EnCycle + [NomPRG + "." + NomServoList [i] + "." + "bEnCycle"]
        return Nom_ID, Nom_ModeRotation, Nom_PosMin, Nom_PosMax, Nom_PosInit, Nom_Homing, Nom_HomingONOFF, Nom_HomingBasHaut, Nom_CapteurHoming, Nom_VitesseHoming, Nom_ForceHoming, Nom_PositionApresHoming, Nom_MoveRun, Nom_PositionOrdre, Nom_Vitesse, Nom_Syncro, Nom_Force, Nom_PositionReel, Nom_Position0, Nom_HomingDone, Nom_Etat, Nom_CodeErreur, Nom_Movement, Nom_EnCycle

    def AllLitVariables(self, Nom_ListVariables):
        #Lit toute les variables a lire
        #Prendre la variable de sortie de la fonction CreationVariableList
        Nom_ID, Nom_ModeRotation, Nom_PosMin, Nom_PosMax, Nom_PosInit, Nom_Homing, Nom_HomingONOFF, Nom_HomingBasHaut, Nom_CapteurHoming, Nom_VitesseHoming, Nom_ForceHoming, Nom_PositionApresHoming, Nom_MoveRun, Nom_PositionOrdre, Nom_Vitesse, Nom_Syncro, Nom_Force, Nom_PositionReel, Nom_Position0, Nom_HomingDone, Nom_Etat, Nom_CodeErreur, Nom_Movement = Nom_ListVariables
        Val_ID = self.plc.read_list_by_name(Nom_ID)
        Val_ModeRotation = self.plc.read_list_by_name(Nom_ModeRotation)
        Val_PosMin = self.plc.read_list_by_name(Nom_PosMin)
        Val_PosMax = self.plc.read_list_by_name(Nom_PosMax)
        Val_PosInit = self.plc.read_list_by_name(Nom_PosInit)
        Val_Homing = self.plc.read_list_by_name(Nom_Homing)
        Val_HomingONOFF = self.plc.read_list_by_name(Nom_HomingONOFF)
        Val_HomingBasHaut = self.plc.read_list_by_name(Nom_HomingBasHaut)
        Val_CapteurHoming = self.plc.read_list_by_name(Nom_CapteurHoming)
        Val_VitesseHoming = self.plc.read_list_by_name(Nom_VitesseHoming)
        Val_ForceHoming = self.plc.read_list_by_name(Nom_ForceHoming)
        Val_PositionApresHoming = self.plc.read_list_by_name(Nom_PositionApresHoming)
        Val_MoveRun = self.plc.read_list_by_name(Nom_MoveRun)
        Val_PositionOrdre = self.plc.read_list_by_name(Nom_PositionOrdre)
        Val_Vitesse = self.plc.read_list_by_name(Nom_Vitesse)
        Val_Syncro = self.plc.read_list_by_name(Nom_Syncro)
        return Val_ID, Val_ModeRotation, Val_PosMin, Val_PosMax, Val_PosInit, Val_Homing, Val_HomingONOFF, Val_HomingBasHaut, Val_CapteurHoming, Val_VitesseHoming, Val_ForceHoming, Nom_PositionApresHoming, Val_MoveRun, Val_PositionOrdre, Val_Vitesse, Val_Syncro

    def FusionNomValeur(self, ListNom, ListVariable):
        #Fusione les noms et les valeurs des differentes variables
        #EX: ListVariable = [90, 91 ,92 , 93, 94, 95, 96, 97, 98, 99, 100]
        LongeurList = len(ListNom)
        Valeur_Nom_Variables = '{'
        for i in range(LongeurList):
            Valeur_Nom_Variables += f'"{ListNom[i]}": {ListVariable[i]}, '
        Valeur_Nom_Variables = Valeur_Nom_Variables[:-2] + '}'
        Valeur_Nom_Variables = json.loads(Valeur_Nom_Variables)
        return Valeur_Nom_Variables