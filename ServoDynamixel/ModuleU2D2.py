""" Auteur: Luca Freund
    Date:   14.12.2022

    Ce Moudule simplifie l envoi et la reception de trame via Dynamixel U2D2
"""
from dynamixel_sdk import *
import os
import msvcrt


PROTOCOL_VERSION        = 2.0       #Protocol de Communication, les Servos XC, XL etc... utilise le protocol de Dynamixel 2.0

BAUDRATE                = 1000000  #Vitesse de Communication
DEVICENAME              = 'COM3'    #Port ou le U2D2 est brancher

ADDR_OPERATING_MODE         = 11    #Adresse du Mode de Rotation
ADDR_MIN_POSITION           = 52    #Adresse de la Position Min
ADDR_MAX_POSITION           = 48    #Adresse de la Position Max
ADDR_PRO_TORQUE_ENABLE      = 64    #Adresse du Torque
ADDR_PRO_PRESENT_VELOCITY   = 112   #Adresse de la Vitesse Actuelle
ADDR_PRO_GOAL_POSITION      = 116   #Adresse de la Position Goal
ADDR_PRO_MOVING             = 122   #Adresse si le Servo bouge (Attention a base vitesse plus lent que 40 le servo peut detecter que le servo ne bouge pas)
ADDR_PRESENT_LOAD           = 126   #Adresse de la force actuelle du servo
ADDR_PRO_PRESENT_POSITION   = 132   #Adresse de la Position Actuelle du Servo

TORQUE_ENABLE               = 1     #Torque Activer
TORQUE_DISABLE              = 0     #Torque Desactiver

LEN_PRO_GOAL_POSITION       = 4     #Declaration de la longeur de la trame pour bouger en position Syncro



class Dxl():
    def __init__(self):
        #Ouvre le Port, change la vitesse de communication, puis mais le torque a 0, IDSeconday est une l´ ID definie par le logiciel dynamixel Wizard 2.0
        self.PositionReel = None
        self.Bouge = None
        self.Force = None
        self.dxl_comm_result = None
        self.dxl_error = None
        self.Erreur = None

        self.portHandler = PortHandler(DEVICENAME)

        self.packetHandler = PacketHandler(PROTOCOL_VERSION)

        self.groupSyncWrite = GroupSyncWrite(self.portHandler, self.packetHandler, ADDR_PRO_GOAL_POSITION, LEN_PRO_GOAL_POSITION)


        if self.portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            getch()
            quit()

        if self.portHandler.setBaudRate(BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            getch()
            quit()

        time.sleep(0.5)
        return print("Fin Config")

    def TorqueOFF(self, ID):
        #le Torque est mit a 0
        self.dxl_comm_result, self.dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler,ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
        if self.dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(self.dxl_comm_result))
            self.Erreur = True
        elif self.dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(self.dxl_error))
            self.Erreur = True
        return self.Erreur

    def TorqueON(self, ID):
        #Le Torque est mit a 1
        self.dxl_comm_result, self.dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        if self.dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(self.dxl_comm_result))
            self.Erreur = True
        elif self.dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(self.dxl_error))
            self.Erreur = True
        return self.Erreur

    def ModeRot(self, ID, Mode):
        #Definit le mode de rotation
        self.dxl_comm_result, self.dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, ID, ADDR_OPERATING_MODE, Mode)
        if self.dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(self.dxl_comm_result))
            self.Erreur = True
        elif self.dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(self.dxl_error))
            self.Erreur = True
        return self.Erreur

    def PositionMin(self, ID, PositionMin):
        #Definit la position Min du Servo (le torque doit etre a 0)
        self.dxl_comm_result, self.dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler,  ID, ADDR_MIN_POSITION, PositionMin)
        if self.dxl_comm_result != COMM_SUCCESS:
            self.Erreur = True
            print("%s" % self.packetHandler.getTxRxResult(self.dxl_comm_result))
        elif self.dxl_error != 0:
            self.Erreur = True
            print("%s" % self.packetHandler.getRxPacketError(self.dxl_error))
        return self.Erreur

    def PositionMax(self, ID, PositionMax):
        #Definit la position Max du Servo (le torque doit etre a 0)
        self.dxl_comm_result, self.dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler,  ID, ADDR_MAX_POSITION, PositionMax)
        if self.dxl_comm_result != COMM_SUCCESS:
            self.Erreur = True
            print("%s" % self.packetHandler.getTxRxResult(self.dxl_comm_result))
        elif self.dxl_error != 0:
            self.Erreur = True
            print("%s" % self.packetHandler.getRxPacketError(self.dxl_error))
        return self.Erreur

    def EcrireVitesse(self, ID, Vitesse):
        #Ecrit la Vitesse
        self.dxl_comm_result, self.dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, ID, ADDR_PRO_PRESENT_VELOCITY, Vitesse)
        if self.dxl_comm_result != COMM_SUCCESS:
            self.Erreur = True
            print("%s" % self.packetHandler.getTxRxResult(self.dxl_comm_result))
        elif self.dxl_error != 0:
            self.Erreur = True
            print("%s" % self.packetHandler.getRxPacketError(self.dxl_error))
        return self.Erreur

    def PositionGoal(self, ID, PositionGoal):
        #Position Goal du Servo
        self.dxl_comm_result, self.dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, ID, ADDR_PRO_GOAL_POSITION, PositionGoal)
        if self.dxl_comm_result != COMM_SUCCESS:
            self.Erreur = True
            print("%s" % self.packetHandler.getTxRxResult(self.dxl_comm_result))
        elif self.dxl_error != 0:
            self.Erreur = True
            print("%s" % self.packetHandler.getRxPacketError(self.dxl_error))
        return self.Erreur

    def LirePosition(self, ID):
        #Position Actuelle du Servo, il peut avoir une différence entre la position goal et la position réel, si le servo supporte une force la différence peut etre plus importante
        self.PositionReel, self.dxl_comm_result, self.dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, ID, ADDR_PRO_PRESENT_POSITION)
        if self.dxl_comm_result != COMM_SUCCESS:
            self.Erreur = True
            print("%s" % self.packetHandler.getTxRxResult(self.dxl_comm_result))
        elif self.dxl_error != 0:
            self.Erreur = True
            print("%s" % self.packetHandler.getRxPacketError(self.dxl_error))
        return self.Erreur ,self.PositionReel

    def LirePostionList(self, ListID):
        LongeurList = len(ListID)
        Val_PositionReel,Erreur = [],[]
        for i in range(LongeurList):
            self.PositionReel, self.dxl_comm_result, self.dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, ListID[i], ADDR_PRO_PRESENT_POSITION)
            if self.dxl_comm_result != COMM_SUCCESS:
                self.Erreur = True
                print("%s" % self.packetHandler.getTxRxResult(self.dxl_comm_result))
            elif self.dxl_error != 0:
                self.Erreur = True
                print("%s" % self.packetHandler.getRxPacketError(self.dxl_error))
            Erreur.append(self.Erreur)
            Val_PositionReel.append(self.PositionReel)
        return Erreur, Val_PositionReel


    def EnMouvement(self, ID):
        #Si le Servo bouge ou non, ATTENTION une vitesse trops faible peut ne pas activer cette variable
        self.Bouge, self.dxl_comm_result, self.dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, ID, ADDR_PRO_MOVING)
        if self.dxl_comm_result != COMM_SUCCESS:
            self.Erreur = True
            print("%s" % self.packetHandler.getTxRxResult(self.dxl_comm_result))
        elif self.dxl_error != 0:
            self.Erreur = True
            print("%s" % self.packetHandler.getRxPacketError(self.dxl_error))
        return self.Erreur, self.Bouge

    def ForceActuelle(self, ID):
        #Force Actuelle du Servo
        self.Force, self.dxl_comm_result, self.dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, ID, ADDR_PRESENT_LOAD)
        if self.dxl_comm_result != COMM_SUCCESS:
            self.Erreur = True
            print("%s" % self.packetHandler.getTxRxResult(self.dxl_comm_result))
        elif self.dxl_error != 0:
            self.Erreur = True
            print("%s" % self.packetHandler.getRxPacketError(self.dxl_error))
        return self.Erreur, self.Force

    def StockPosition(self,ID, PositionGoal):
        #Stock Position Goal
        Param_PositionGoal = [DXL_LOBYTE(DXL_LOWORD(PositionGoal)), DXL_HIBYTE(DXL_LOWORD(PositionGoal)), DXL_LOBYTE(DXL_HIWORD(PositionGoal)), DXL_HIBYTE(DXL_HIWORD(PositionGoal))]
        dxl_addparam_result = self.groupSyncWrite.addParam(ID, Param_PositionGoal)
        if dxl_addparam_result != True:
            self.Erreur = True
            print("[ID:%03d] groupSyncWrite addparam failed" % ID)
        return self.Erreur

    def MoveSyncro(self):
        #Lance le Mouvement du Syncro
        self.dxl_comm_result = self.groupSyncWrite.txPacket()
        if self.dxl_comm_result != COMM_SUCCESS:
            self.Erreur = True
            print("%s" % self.packetHandler.getTxRxResult(self.dxl_comm_result))
        self.groupSyncWrite.clearParam()
        return self.Erreur
