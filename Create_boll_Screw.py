# -*- coding: utf-8 -*-
import os

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism, BRepPrimAPI_MakeRevol
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeChamfer
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax1, gp_Dir
from OCC.Core.TopoDS import TopoDS_Shape,TopoDS_Builder,TopoDS_Compound,topods_CompSolid
from OCC.Extend.DataExchange import read_step_file,write_step_file
from OCC.Core.ChFi2d import ChFi2d_ChamferAPI
from OCC.Core.STEPControl import STEPControl_Reader,STEPControl_Writer
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Ax1, gp_Dir

class Create_boll_SCcrew(object):
    def __init__(self):#初始化参数
        pass
        #螺母参数初始化---------------------------
        self.SFU01204_4_dict ={"d":12,"I":4,"Da":2.500,"D":24,"A":40,"B":10,"L":40,
                                    "W":32,"H":30,"X":4.5,"Q":"-","N":"1x4","Ca":902,"Coa":1884,"kgf/um":26}#
        self.SFU01604_4_dict = {"d":16,"I":4,"Da":2.381,"D":28,"A":48,"B":10,"L":40,
                                    "W":38,"H":40,"X":5.5,"Q":"M6","N":"1x4","Ca":973,"Coa":2406,"kgf/um":32}#
        self.SFU01605_4_dict = {"d":16,"I":5,"Da":3.175,"D":28,"A":48,"B":10,"L":50,
                                    "W":38,"H":40,"X":5.5,"Q":"M6","N":"1x4","Ca":1380,"Coa":3052,"kgf/um":32}#
        self.SFU01610_4_dict = {"d":16,"I":10,"Da":3.175,"D":28,"A":48,"B":10,"L":57,
                                    "W":38,"H":40,"X":5.5,"Q":"M6","N":"1x3","Ca":1103,"Coa":2401,"kgf/um":26}#
        self.SFU02004_4_dict = {"d":20,"I":4,"Da":2.381,"D":36,"A":58,"B":10,"L":42,
                                    "W":47,"H":44,"X":6.6,"Q":"M6","N":"1x4","Ca":1066,"Coa":2987,"kgf/um":38}
        self.SFU02005_4_dict = {"d":20,"I":5,"Da":3.175,"D":36,"A":58,"B":10,"L":51,
                                    "W":47,"H":44,"X":6.6,"Q":"M6","N":"1x4","Ca":1551,"Coa":3875,"kgf/um":39}
        self.SFU02504_4_dict = {"d":25,"I":4,"Da":2.381,"D":40,"A":62,"B":10,"L":42,
                                    "W":51,"H":48,"X":6.6,"Q":"M6","N":"1x4","Ca":1180,"Coa":3795,"kgf/um":43}
        self.SFU02505_4_dict = {"d":25, "I":5, "Da":3.175, "D":40, "A":62, "B":10, "L":51,
                               "W":51, "H":48, "X":6.6, "Q":"M6", "N":"1x4", "Ca":1724, "Coa":4904, "kgf/um":45}
        self.SFU02506_4_dict = {"d":25, "I":6, "Da":3.969, "D":40, "A":62, "B":10, "L":54,
                               "W":51, "H":48, "X":6.6, "Q":"M6", "N":"1x4", "Ca":2318, "Coa":6057, "kgf/um":47}
        self.SFU02508_4_dict = {"d":25, "I":8, "Da":4.762, "D":40, "A":62, "B":10, "L":63,
                               "W":51, "H":48, "X":6.6, "Q":"M6", "N":"1x4", "Ca":2963, "Coa":7313, "kgf/um":49}
        self.SFU02510_4_dict = {"d":25, "I":10, "Da":4.762, "D":40, "A":62, "B":12, "L":85,
                               "W":51, "H":48, "X":6.6, "Q":"M6", "N":"1x4", "Ca":2954, "Coa":7295, "kgf/um":50}
        self.SFU03204_4_dict = {"d":32, "I":4, "Da":2.381, "D":50, "A":80, "B":12, "L":44,
                               "W":65, "H":62, "X":9.0, "Q":"M6", "N":"1x4", "Ca":1296, "Coa":4838, "kgf/um":51}
        self.SFU03205_4_dict = {"d":32, "I":5, "Da":2.381, "D":50, "A":80, "B":12, "L":52,
                               "W":65, "H":62, "X":9.0, "Q":"M6", "N":"1x4", "Ca":1922, "Coa":6343, "kgf/um":54}
        self.SFU03206_4_dict = {"d":32, "I":6, "Da":3.969, "D":50, "A":80, "B":12, "L":57,
                               "W":65, "H":62, "X":9.0, "Q":"M6", "N":"1x4", "Ca":2632, "Coa":7979, "kgf/um":57}
        self.SFU03208_4_dict = {"d":32, "I":8, "Da":3.969, "D":50, "A":80, "B":12, "L":65,
                               "W":65, "H":62, "X":9.0, "Q":"M6", "N":"1x4", "Ca":3387, "Coa":9622, "kgf/um":60}
        self.SFU03210_4_dict = {"d":32, "I":10, "Da":3.969, "D":50, "A":80, "B":12, "L":90,
                               "W":65, "H":62, "X":9.0, "Q":"M6", "N":"1x4", "Ca":4805, "Coa":12208, "kgf/um":61}
        self.SFU04005_4_dict = {"d":40, "I":5, "Da":3.175, "D":63, "A":93, "B":14, "L":55,
                               "W":78, "H":70, "X":9.0, "Q":"M6", "N":"1x4", "Ca":2110, "Coa":7988, "kgf/um":63}
        self.SFU04006_4_dict = {"d":40, "I":6, "Da":3.969, "D":63, "A":93, "B":14, "L":60,
                               "W":78, "H":70, "X":9.0, "Q":"M6", "N":"1x4", "Ca":2873, "Coa":9913, "kgf/um":66}
        self.SFU04008_4_dict = {"d":40, "I":8, "Da":4.762, "D":63, "A":93, "B":14, "L":67,
                               "W":78, "H":70, "X":9.0, "Q":"M6", "N":"1x4", "Ca":3712, "Coa":11947, "kgf/um":70}
        self.SFU04010_4_dict = {"d":40, "I":10, "Da":6.325, "D":63, "A":93, "B":14, "L":93,
                               "W":78, "H":70, "X":9.0, "Q":"M6", "N":"1x4", "Ca":5399, "Coa":15500, "kgf/um":73}
        self.SFU05010_4_dict = {"d":50, "I":10, "Da":6.325, "D":75, "A":110, "B":16, "L":93,
                               "W":93, "H":85, "X":11, "Q":"M6", "N":"1x4", "Ca":6004, "Coa":19614, "kgf/um":85}
        self.SFU05020_4_dict = {"d":50, "I":20, "Da":7.144, "D":75, "A":110, "B":16, "L":138,
                               "W":93, "H":85, "X":11, "Q":"M6", "N":"1x4", "Ca":7142, "Coa":22588, "kgf/um":94}
        self.SFU06310_4_dict = {"d":63, "I":10, "Da":6.325, "D":90, "A":125, "B":18, "L":98,
                               "W":108, "H":95, "X":11, "Q":"M6", "N":"1x4", "Ca":6719, "Coa":25358, "kgf/um":99}
        self.SFU06320_4_dict = {"d":63, "I":10, "Da":9.525, "D":95, "A":135, "B":20, "L":149,
                               "W":115, "H":100, "X":13.5, "Q":"M6", "N":"1x4", "Ca":11444, "Coa":36653, "kgf/um":112}
        self.SFU08010_4_dict = {"d":80, "I":10, "Da":6.325, "D":95, "A":105, "B":20, "L":98,
                               "W":125, "H":110, "X":13.5, "Q":"M6", "N":"1x4", "Ca":7346, "Coa":31953, "kgf/um":109}
        self.SFU08020_4_dict = {"d":80, "I":20, "Da":9.525, "D":125, "A":165, "B":25, "L":154,
                               "W":145, "H":130, "X":13.5, "Q":"M6", "N":"1x4", "Ca":12911, "Coa":47747, "kgf/um":138}
        self.SFU10020_4_dict = {"d":100, "I":20, "Da":9.525, "D":125, "A":150, "B":30, "L":180,
                               "W":170, "H":155, "X":13.5, "Q":"M6", "N":"1x4", "Ca":14303, "Coa":60698, "kgf/um":162}
        self.SFU_serise_dict={"SFU01204_4":self.SFU01204_4_dict,"SFU01604_4":self.SFU01604_4_dict,"SFU01605_4":self.SFU01605_4_dict,
                       "SFU01610_4":self.SFU01610_4_dict,"SFU02004_4":self.SFU02004_4_dict,"SFU02005_4":self.SFU02005_4_dict,
                       "SFU02505_4":self.SFU02505_4_dict,"SFU02506_4":self.SFU02506_4_dict,"SFU02508_4":self.SFU02508_4_dict,
                       "SFU02510_4":self.SFU02510_4_dict,"SFU03204_4":self.SFU03204_4_dict,"SFU03205_4":self.SFU03205_4_dict,
                       "SFU03206_4":self.SFU03206_4_dict,"SFU03208_4":self.SFU03208_4_dict,"SFU03210_4":self.SFU03210_4_dict,
                       "SFU04005_4":self.SFU04005_4_dict,"SFU04006_4":self.SFU04006_4_dict,"SFU04008_4":self.SFU04008_4_dict,"SFU04010_4":self.SFU04010_4_dict,
                        "SFU05010_4":self.SFU05010_4_dict,"SFU05020_4":self.SFU05020_4_dict,"SFU06310_4":self.SFU06310_4_dict,
                        "SFU06320_4":self.SFU06320_4_dict,"SFU08010_4":self.SFU08010_4_dict,"SFU08020_4":self.SFU08020_4_dict,
                        "SFU10020_4":self.SFU10020_4_dict}
        #丝杆参数初始化----------------------------------
        #-------------BKBF系列--------------------------
        self.BK_10_dict={"D1":8.,"D2":10.,"D3":12,"D4":8,"D5":7.0,"L1":15,"L2":16,"L3":39,"L4":10,
                         "L5":7.9,"L6":0.9,"C1":0.5,"C2":0.5,"C3":0.5}# ok
        self.BK_12_dict = {"D1": 10., "D2": 12., "D3": 16, "D4": 10, "D5": 9.6, "L1": 15, "L2": 14, "L3": 39, "L4": 11,
                           "L5": 9.15, "L6": 1.15,"C1":0.5,"C2":0.5,"C3":0.5}#ok
        self.BK_15_dict = {"D1": 12., "D2": 15., "D3": 20, "D4": 15, "D5": 14.3, "L1": 20, "L2": 12, "L3": 40, "L4": 13,
                           "L5": 10.15, "L6": 1.15,"C1":0.5,"C2":0.5,"C3":0.5}#ok
        self.BK_17_dict = {"D1": 15., "D2": 17., "D3": 20, "D4": 17, "D5": 16.2, "L1": 23, "L2": 17, "L3": 53, "L4": 16,
                           "L5": 13.15, "L6": 1.15,"C1":0.5,"C2":0.5,"C3":0.5}#ok
        self.BK_20_dict = {"D1": 17., "D2": 20., "D3": 25, "D4": 20, "D5": 16.2, "L1": 25, "L2": 15, "L3": 53, "L4": 16,
                           "L5": 13.35, "L6": 1.35, "C1": 0.5, "C2": 0.5, "C3": 0.5}#ok
        self.BK_25_dict = {"D1": 20., "D2": 25., "D3": 30, "D4": 25, "D5": 23.9, "L1": 30, "L2": 18, "L3": 65, "L4": 20,
                           "L5": 16.35, "L6": 1.35, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.BK_30_dict = {"D1": 25., "D2": 30., "D3": 35, "D4": 30, "D5": 28.6, "L1": 38, "L2": 25, "L3": 72, "L4": 21,
                           "L5": 17.75, "L6": 1.75, "C1": 0.5, "C2": 0.7, "C3": 1.0}#ok
        self.BK_35_dict = {"D1": 30., "D2": 35., "D3": 40, "D4": 35, "D5": 33, "L1": 45, "L2": 28, "L3": 83, "L4": 22,
                           "L5": 18.75, "L6": 1.75, "C1": 0.5, "C2": 1.0, "C3": 1.0}  # ok
        self.BK_40_dict = {"D1": 35., "D2": 40., "D3": 50, "D4": 40, "D5": 38, "L1": 50, "L2": 35, "L3": 98, "L4": 23,
                           "L5": 19.95, "L6": 1.95, "C1": 0.5, "C2": 1.0, "C3": 1.0}#ok
        self.BK_serise_dict={"BKBF10":self.BK_10_dict,"BKBF12":self.BK_12_dict,"BKBF15":self.BK_15_dict,"BKBF17":self.BK_17_dict,
                             "BKBF20":self.BK_20_dict,"BKBF25":self.BK_25_dict,"BKBF30":self.BK_30_dict,"BKBF35":self.BK_35_dict,
                             "BKBF40":self.BK_40_dict}
        # -------------EKEF系列--------------------------
        self.EK_06_dict = {"D1": 8., "D2": 6., "D3": 6, "D4":6, "D5": 5.7, "L1": 8, "L2": 10, "L3": 30, "L4": 9,
                           "L5": 6.8, "L6": 0.8, "C1": 0.3, "C2": 0.3, "C3": 0.3}  # ok
        self.EK_08_dict = {"D1": 6., "D2": 8., "D3": 10, "D4": 6, "D5": 5.7, "L1": 9, "L2": 10, "L3": 35, "L4": 9,
                           "L5": 6.8, "L6": 0.8, "C1": 0.3, "C2": 0.3, "C3": 0.3}  # ok
        self.EK_10_dict = {"D1": 8., "D2": 10., "D3": 12, "D4": 8, "D5": 7.6, "L1": 15, "L2": 11, "L3": 36, "L4": 10,
                           "L5": 7.9, "L6": 0.9, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.EK_12_dict = {"D1": 10., "D2": 12., "D3": 15, "D4": 10, "D5": 9.6, "L1": 15, "L2": 11, "L3": 36, "L4": 11,
                           "L5": 9.15, "L6": 1.15, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.EK_15_dict = {"D1": 12., "D2": 15., "D3": 18, "D4": 15, "D5": 14.3, "L1": 20, "L2": 11, "L3": 49, "L4": 13,
                           "L5": 10.15, "L6": 1.15, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.EK_20_dict = {"D1": 17., "D2": 20., "D3": 25, "D4": 20, "D5": 19, "L1": 25, "L2": 17, "L3": 64, "L4": 19,
                           "L5": 15.35, "L6": 1.35, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.EK_25_dict = {"D1": 20., "D2": 25., "D3": 32, "D4": 25, "D5": 23.9, "L1": 30, "L2": 18, "L3": 65, "L4": 20,
                           "L5": 16.35, "L6": 1.35, "C1": 0.5, "C2": 0.7, "C3": 0.1}  # ok
        self.EK_serise_dict = {"EKEF06": self.EK_06_dict, "EKEF08": self.EK_08_dict, "EKEF10": self.EK_10_dict,
                               "EKEF12": self.EK_12_dict,
                               "EKEF15": self.EK_15_dict, "EKEF20": self.EK_20_dict, "EKEF25": self.EK_25_dict}
        # -------------FKFF系列--------------------------
        self.FK_08_dict = {"D1": 6., "D2": 8., "D3": 10, "D4": 6, "D5": 5.7, "L1": 9, "L2": 15, "L3": 25, "L4": 9,
                           "L5": 6.8, "L6": 0.8, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.FK_10_dict = {"D1": 8., "D2": 10., "D3": 12, "D4": 8, "D5": 5.6, "L1": 15, "L2": 11, "L3": 36, "L4": 10,
                           "L5": 7.9, "L6": 0.9, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.FK_12_dict = {"D1": 10., "D2": 12., "D3": 15, "D4": 10, "D5": 9.6, "L1": 15, "L2": 11, "L3": 36, "L4": 11,
                           "L5": 9.15, "L6": 1.15, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.FK_15_dict = {"D1": 12., "D2": 15., "D3": 18, "D4": 15, "D5": 14.3, "L1": 20, "L2": 13, "L3": 36, "L4": 13,
                           "L5": 10.15, "L6": 1.15, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.FK_20_dict = {"D1": 17., "D2": 20., "D3": 25, "D4": 20, "D5": 19, "L1": 25, "L2": 17, "L3": 64, "L4": 19,
                           "L5": 15.75, "L6": 1.35, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.FK_25_dict = {"D1": 20., "D2": 25., "D3": 32, "D4": 25, "D5": 23.9, "L1": 30, "L2": 20, "L3": 76, "L4": 20,
                           "L5": 16.35, "L6": 1.35, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.FK_30_dict = {"D1": 25., "D2": 30., "D3": 40, "D4": 30, "D5": 28.6, "L1": 38, "L2": 25, "L3": 72, "L4": 21,
                           "L5": 17.75, "L6": 1.75, "C1": 0.5, "C2": 0.5, "C3": 0.5}  # ok
        self.FK_serise_dict = {"FKFF08": self.FK_08_dict, "FKFF10": self.FK_10_dict, "FKFF15": self.FK_15_dict,
                               "FKFF20": self.FK_20_dict,
                               "FKFF25": self.FK_25_dict, "FKFF30": self.FK_30_dict}


        #复合体初始化---------------------------------
        self.shape=TopoDS_Shape()
        self.new_build = TopoDS_Builder()  # 建立一个TopoDS_Builder()
        self.aCompound = TopoDS_Compound()  # 定义一个复合体
        self.new_build.MakeCompound(self.aCompound)  # 生成一个复合体DopoDS_shape

    def Create_Bk(self,filename="SFU01204-4",ss="BKBF10",L=1000):
        pass
        "获取选择零件名称  获取路径"
        # 获取零件名称
        try:
            pass
            new_shape = TopoDS_Shape()
            #filename = "SFU2005-4"
            # 获取相应零件的路径***************************************
            self.partpath = os.getcwd()
            self.partpath = self.partpath + "\\3Ddata" + "\\STP" + "\\" + filename + ".stp"
            self.shape = read_step_file(self.partpath)
            self.shape.Free(True)  # 先释放shape
            # self.new_build.Add(self.aCompound,shape123)#将shaoe添加入复合体
            self.new_build.Add(self.aCompound, self.shape)
            #绘制丝杆**************************************************
            if int(filename[3:6])==12 or int(filename[3:6])==14 or int(filename[3:6])==15:
                ss="BKBF10"
            elif int(filename[3:6])==14 or int(filename[3:6])==15 or int(filename[3:6])==16 or int(filename[3:6])==18 :
                pass
                ss="BKBF12"
            elif int(filename[3:6])==18 or int(filename[3:6])==20:
                ss="BKBF15"
            elif int(filename[3:6])==20 or int(filename[3:6])==25:
                ss="BKBF17"
            elif int(filename[3:6])==25 or int(filename[3:6])==28:
                ss="BKBF20"
            elif int(filename[3:6])==32 or int(filename[3:6])==36:
                ss="BKBF25"
            elif int(filename[3:6])==36 or int(filename[3:6])==40:
                ss="BKBF30"
            elif int(filename[3:6])==40 or int(filename[3:6])==45 or int(filename[3:6])==50:
                ss="BKBF35"
            elif int(filename[3:6])==50 or int(filename[3:6])==55:
                ss="BKBF40"
            self.BK_serise_dict[ss]["D3"]=int(filename[3:6])#重新设置丝杆直径

            #print(filename[3:6])
            #PL = (L - 15 - 39 - 10) / 2
            '''
            PL = (L - self.BK_serise_dict[ss]["L1"] - self.BK_serise_dict[ss]["L3"]
                  - self.BK_serise_dict[ss]["L4"]) / 2
            '''
            #Center_point=filename[0:]
            PL=L/2
            #P1 = [0, 0, PL + 39 + 15]
            P1 = [0, 0, PL + self.BK_serise_dict[ss]["L3"] + self.BK_serise_dict[ss]["L1"]]
            #P2 = [0, 4, PL + 39 + 15]
            P2 = [0, self.BK_serise_dict[ss]["D1"]/2, PL + self.BK_serise_dict[ss]["L3"]
                  + self.BK_serise_dict[ss]["L1"]]
            #P3 = [0, 4, PL + 39]
            P3 = [0, self.BK_serise_dict[ss]["D1"]/2, PL + self.BK_serise_dict[ss]["L3"]]
            #P4 = [0, 5, PL + 39]
            P4 = [0, self.BK_serise_dict[ss]["D2"]/2, PL + self.BK_serise_dict[ss]["L3"]]
            #P5 = [0, 5, PL]
            P5 = [0, self.BK_serise_dict[ss]["D2"]/2, PL]
            #P6 = [0, 6, PL]
            P6 = [0, self.BK_serise_dict[ss]["D3"]/2, PL]
            #P7 = [0, 6, -PL]
            P7 = [0, self.BK_serise_dict[ss]["D3"]/2, -PL]
            #P8 = [0, 4, -PL]
            P8 = [0, self.BK_serise_dict[ss]["D4"]/2, -PL]
            #P9 = [0, 4, -PL - 7.9]
            P9 = [0, self.BK_serise_dict[ss]["D4"]/2, -PL - self.BK_serise_dict[ss]["L5"]]
            #P10 = [0, 4 - 0.2, -PL - 7.9]
            P10 = [0, self.BK_serise_dict[ss]["D5"]/2, -PL - self.BK_serise_dict[ss]["L5"]]
            #P11 = [0, 4 - 0.2, -PL - 7.9 - 0.8]
            P11 = [0, self.BK_serise_dict[ss]["D5"]/2, -PL - self.BK_serise_dict[ss]["L5"] -
                   self.BK_serise_dict[ss]["L6"]]
            #P12 = [0, 4, -PL - 7.9 - 0.8]
            P12 = [0, self.BK_serise_dict[ss]["D4"]/2, -PL - self.BK_serise_dict[ss]["L5"] -
                   self.BK_serise_dict[ss]["L6"]]
            #P13 = [0, 4, -PL - 10]
            P13 = [0, self.BK_serise_dict[ss]["D4"]/2, -PL - self.BK_serise_dict[ss]["L4"]]
            #P14 = [0, 0, -PL - 10]
            P14 = [0, 0, -PL - self.BK_serise_dict[ss]["L4"]]
            E11 = BRepBuilderAPI_MakeEdge(gp_Pnt(P1[0], P1[1], P1[2]), gp_Pnt(P2[0], P2[1], P2[2])).Edge()
            E12 = BRepBuilderAPI_MakeEdge(gp_Pnt(P2[0], P2[1], P2[2]), gp_Pnt(P3[0], P3[1], P3[2])).Edge()
            E13 = BRepBuilderAPI_MakeEdge(gp_Pnt(P3[0], P3[1], P3[2]), gp_Pnt(P4[0], P4[1], P4[2])).Edge()
            E14 = BRepBuilderAPI_MakeEdge(gp_Pnt(P4[0], P4[1], P4[2]), gp_Pnt(P5[0], P5[1], P5[2])).Edge()
            E15 = BRepBuilderAPI_MakeEdge(gp_Pnt(P5[0], P5[1], P5[2]), gp_Pnt(P6[0], P6[1], P6[2])).Edge()
            E16 = BRepBuilderAPI_MakeEdge(gp_Pnt(P6[0], P6[1], P6[2]), gp_Pnt(P7[0], P7[1], P7[2])).Edge()
            E17 = BRepBuilderAPI_MakeEdge(gp_Pnt(P7[0], P7[1], P7[2]), gp_Pnt(P8[0], P8[1], P8[2])).Edge()
            E18 = BRepBuilderAPI_MakeEdge(gp_Pnt(P8[0], P8[1], P8[2]), gp_Pnt(P9[0], P9[1], P9[2])).Edge()
            E19 = BRepBuilderAPI_MakeEdge(gp_Pnt(P9[0], P9[1], P9[2]), gp_Pnt(P10[0], P10[1], P10[2])).Edge()
            E20 = BRepBuilderAPI_MakeEdge(gp_Pnt(P10[0], P10[1], P10[2]), gp_Pnt(P11[0], P11[1], P11[2])).Edge()
            E21 = BRepBuilderAPI_MakeEdge(gp_Pnt(P11[0], P11[1], P11[2]), gp_Pnt(P12[0], P12[1], P12[2])).Edge()
            E22 = BRepBuilderAPI_MakeEdge(gp_Pnt(P12[0], P12[1], P12[2]), gp_Pnt(P13[0], P13[1], P13[2])).Edge()
            E23 = BRepBuilderAPI_MakeEdge(gp_Pnt(P13[0], P13[1], P13[2]), gp_Pnt(P14[0], P14[1], P14[2])).Edge()
            E24 = BRepBuilderAPI_MakeEdge(gp_Pnt(P14[0], P14[1], P14[2]), gp_Pnt(P1[0], P1[1], P1[2])).Edge()

            new_charme = ChFi2d_ChamferAPI()
            new_charme.Init(E11,E12)
            new_charme.Perform()
            E25 = new_charme.Result(E11, E12, self.BK_serise_dict[ss]["C1"], self.BK_serise_dict[ss]["C1"])#倒角1

            new_charme.Init(E13,E14)
            new_charme.Perform()
            E26=new_charme.Result(E13,E14,self.BK_serise_dict[ss]["C2"],self.BK_serise_dict[ss]["C2"])#倒角2

            new_charme.Init(E15,E16)
            new_charme.Perform()
            E27=new_charme.Result(E15,E16,self.BK_serise_dict[ss]["C3"],self.BK_serise_dict[ss]["C3"])#倒角3

            new_charme.Init(E16, E17)
            new_charme.Perform()
            E28 = new_charme.Result(E16, E17, self.BK_serise_dict[ss]["C3"], self.BK_serise_dict[ss]["C3"])  # 倒角4

            new_charme.Init(E22, E23)
            new_charme.Perform()
            E29 = new_charme.Result(E22, E23, self.BK_serise_dict[ss]["C1"], self.BK_serise_dict[ss]["C1"])  # 倒角5

            #print(type(E11))
            #print(E29.IsNull())

            W1 = BRepBuilderAPI_MakeWire(E11, E25,E12).Wire()
            W2 = BRepBuilderAPI_MakeWire(E13, E26, E14).Wire()
            W3 = BRepBuilderAPI_MakeWire(E15, E27, E16).Wire()
            W4 = BRepBuilderAPI_MakeWire(E16, E28, E17).Wire()
            W5 = BRepBuilderAPI_MakeWire(E18, E19, E20,E21).Wire()
            W6 = BRepBuilderAPI_MakeWire(E22, E29, E23, E24).Wire()
            #print("succeed")


            mkWire = BRepBuilderAPI_MakeWire()
            mkWire.Add(W1)
            mkWire.Add(W2)
            mkWire.Add(W3)
            mkWire.Add(W4)
            mkWire.Add(W5)
            mkWire.Add(W6)
            Rob = BRepPrimAPI_MakeRevol(BRepBuilderAPI_MakeFace(mkWire.Wire()).Face(),
                                      gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))).Shape()
            #倒角-----------------------------
            #MF=BRepFilletAPI_MakeChamfer(Rob)
            #MF.Add()
            #移动
            ls_filename=filename[0:8]+"_4"
            move_distance=0.5*L-(L-float(self.SFU_serise_dict[ls_filename]["L"]))/2
            cone = TopoDS_Shape(Rob)
            T = gp_Trsf()
            T.SetTranslation(gp_Vec(0, 0, -move_distance))
            loc = TopLoc_Location(T)
            cone.Location(loc)
            self.new_build.Add(self.aCompound, cone)
            print(type(self.aCompound))
            return self.aCompound


        except:
            return False
    def Create_Ek(self,filename="SFU01204-4",ss="EKEF10",L=100):
        pass
        if int(filename[3:6]) == 6 or int(filename[3:6]) == 8:
            ss = "EKEF06"
        elif int(filename[3:6]) == 10 or int(filename[3:6]) == 12:
            ss = "EKEF08"
        elif int(filename[3:6]) == 12 or int(filename[3:6]) == 14 or int(filename[3:6]) == 15:
            ss = "EKEF10"
        elif int(filename[3:6]) == 14 or int(filename[3:6]) == 15 or int(filename[3:6]) == 16:
            ss = "EKEF12"
        elif int(filename[3:6]) == 18 or int(filename[3:6]) == 20:
            ss = "EKEF15"
        elif int(filename[3:6]) == 25 or int(filename[3:6]) == 28 or int(filename[3:6]) == 32:
            ss = "EKEF20"
        elif int(filename[3:6]) == 32 or int(filename[3:6]) == 36:
            ss = "EKEF25"
        "获取选择零件名称  获取路径"
        # 获取零件名称
        try:
            pass
            new_shape = TopoDS_Shape()
            #filename = "SFU2005-4"
            # 获取相应零件的路径***************************************
            self.partpath = os.getcwd()
            self.partpath = self.partpath + "\\3Ddata" + "\\STP" + "\\" + filename + ".stp"
            self.shape = read_step_file(self.partpath)
            self.shape.Free(True)  # 先释放shape
            # self.new_build.Add(self.aCompound,shape123)#将shaoe添加入复合体
            self.new_build.Add(self.aCompound, self.shape)
            #绘制丝杆**************************************************
            self.EK_serise_dict[ss]["D3"]=int(filename[3:6])#重新设置丝杆直径
            #print(filename[3:6])
            #PL = (L - 15 - 39 - 10) / 2
            PL = (L - self.EK_serise_dict[ss]["L1"] - self.EK_serise_dict[ss]["L2"]
                  - self.EK_serise_dict[ss]["L4"]) / 2
            #P1 = [0, 0, PL + 39 + 15]
            P1 = [0, 0, PL + self.EK_serise_dict[ss]["L3"] + self.EK_serise_dict[ss]["L1"]]
            #P2 = [0, 4, PL + 39 + 15]
            P2 = [0, self.EK_serise_dict[ss]["D1"]/2, PL + self.EK_serise_dict[ss]["L3"]
                  + self.EK_serise_dict[ss]["L1"]]
            #P3 = [0, 4, PL + 39]
            P3 = [0, self.EK_serise_dict[ss]["D1"]/2, PL + self.EK_serise_dict[ss]["L3"]]
            #P4 = [0, 5, PL + 39]
            P4 = [0, self.EK_serise_dict[ss]["D2"]/2, PL + self.EK_serise_dict[ss]["L3"]]
            #P5 = [0, 5, PL]
            P5 = [0, self.EK_serise_dict[ss]["D2"]/2, PL]
            #P6 = [0, 6, PL]
            P6 = [0, self.EK_serise_dict[ss]["D3"]/2, PL]
            #P7 = [0, 6, -PL]
            P7 = [0, self.EK_serise_dict[ss]["D3"]/2, -PL]
            #P8 = [0, 4, -PL]
            P8 = [0, self.EK_serise_dict[ss]["D1"]/2, -PL]
            #P9 = [0, 4, -PL - 7.9]
            P9 = [0, self.EK_serise_dict[ss]["D1"]/2, -PL - self.EK_serise_dict[ss]["L5"]]
            #P10 = [0, 4 - 0.2, -PL - 7.9]
            P10 = [0, self.EK_serise_dict[ss]["D5"]/2, -PL - self.EK_serise_dict[ss]["L5"]]
            #P11 = [0, 4 - 0.2, -PL - 7.9 - 0.8]
            P11 = [0, self.EK_serise_dict[ss]["D5"]/2, -PL - self.EK_serise_dict[ss]["L5"] -
                   self.EK_serise_dict[ss]["L6"]]
            #P12 = [0, 4, -PL - 7.9 - 0.8]
            P12 = [0, self.EK_serise_dict[ss]["D1"]/2, -PL - self.EK_serise_dict[ss]["L5"] -
                   self.EK_serise_dict[ss]["L6"]]
            #P13 = [0, 4, -PL - 10]
            P13 = [0, self.EK_serise_dict[ss]["D1"]/2, -PL - self.EK_serise_dict[ss]["L4"]]
            #P14 = [0, 0, -PL - 10]
            P14 = [0, 0, -PL - self.EK_serise_dict[ss]["L4"]]
            E11 = BRepBuilderAPI_MakeEdge(gp_Pnt(P1[0], P1[1], P1[2]), gp_Pnt(P2[0], P2[1], P2[2])).Edge()
            E12 = BRepBuilderAPI_MakeEdge(gp_Pnt(P2[0], P2[1], P2[2]), gp_Pnt(P3[0], P3[1], P3[2])).Edge()
            E13 = BRepBuilderAPI_MakeEdge(gp_Pnt(P3[0], P3[1], P3[2]), gp_Pnt(P4[0], P4[1], P4[2])).Edge()
            E14 = BRepBuilderAPI_MakeEdge(gp_Pnt(P4[0], P4[1], P4[2]), gp_Pnt(P5[0], P5[1], P5[2])).Edge()
            E15 = BRepBuilderAPI_MakeEdge(gp_Pnt(P5[0], P5[1], P5[2]), gp_Pnt(P6[0], P6[1], P6[2])).Edge()
            E16 = BRepBuilderAPI_MakeEdge(gp_Pnt(P6[0], P6[1], P6[2]), gp_Pnt(P7[0], P7[1], P7[2])).Edge()
            E17 = BRepBuilderAPI_MakeEdge(gp_Pnt(P7[0], P7[1], P7[2]), gp_Pnt(P8[0], P8[1], P8[2])).Edge()
            E18 = BRepBuilderAPI_MakeEdge(gp_Pnt(P8[0], P8[1], P8[2]), gp_Pnt(P9[0], P9[1], P9[2])).Edge()
            E19 = BRepBuilderAPI_MakeEdge(gp_Pnt(P9[0], P9[1], P9[2]), gp_Pnt(P10[0], P10[1], P10[2])).Edge()
            E20 = BRepBuilderAPI_MakeEdge(gp_Pnt(P10[0], P10[1], P10[2]), gp_Pnt(P11[0], P11[1], P11[2])).Edge()
            E21 = BRepBuilderAPI_MakeEdge(gp_Pnt(P11[0], P11[1], P11[2]), gp_Pnt(P12[0], P12[1], P12[2])).Edge()
            E22 = BRepBuilderAPI_MakeEdge(gp_Pnt(P12[0], P12[1], P12[2]), gp_Pnt(P13[0], P13[1], P13[2])).Edge()
            E23 = BRepBuilderAPI_MakeEdge(gp_Pnt(P13[0], P13[1], P13[2]), gp_Pnt(P14[0], P14[1], P14[2])).Edge()
            E24 = BRepBuilderAPI_MakeEdge(gp_Pnt(P14[0], P14[1], P14[2]), gp_Pnt(P1[0], P1[1], P1[2])).Edge()

            new_charme = ChFi2d_ChamferAPI()
            new_charme.Init(E11,E12)
            new_charme.Perform()
            E25 = new_charme.Result(E11, E12, self.EK_serise_dict[ss]["C1"], self.EK_serise_dict[ss]["C1"])#倒角1

            new_charme.Init(E13,E14)
            new_charme.Perform()
            E26=new_charme.Result(E13,E14,self.EK_serise_dict[ss]["C2"],self.EK_serise_dict[ss]["C2"])#倒角2

            new_charme.Init(E15,E16)
            new_charme.Perform()
            E27=new_charme.Result(E15,E16,self.EK_serise_dict[ss]["C3"],self.EK_serise_dict[ss]["C3"])#倒角3

            new_charme.Init(E16, E17)
            new_charme.Perform()
            E28 = new_charme.Result(E16, E17, self.EK_serise_dict[ss]["C3"], self.EK_serise_dict[ss]["C3"])  # 倒角4

            new_charme.Init(E22, E23)
            new_charme.Perform()
            E29 = new_charme.Result(E22, E23, self.EK_serise_dict[ss]["C1"], self.EK_serise_dict[ss]["C1"])  # 倒角5


            #print(type(E11))
            #print(E29.IsNull())

            W1 = BRepBuilderAPI_MakeWire(E11, E25,E12).Wire()
            W2 = BRepBuilderAPI_MakeWire(E13, E26, E14).Wire()
            W3 = BRepBuilderAPI_MakeWire(E15, E27, E16).Wire()
            W4 = BRepBuilderAPI_MakeWire(E16, E28, E17).Wire()
            W5 = BRepBuilderAPI_MakeWire(E18, E19, E20,E21).Wire()
            W6 = BRepBuilderAPI_MakeWire(E22, E29, E23, E24).Wire()
            #print("succeed")


            mkWire = BRepBuilderAPI_MakeWire()
            mkWire.Add(W1)
            mkWire.Add(W2)
            mkWire.Add(W3)
            mkWire.Add(W4)
            mkWire.Add(W5)
            mkWire.Add(W6)
            Rob = BRepPrimAPI_MakeRevol(BRepBuilderAPI_MakeFace(mkWire.Wire()).Face(),
                                      gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))).Shape()
            #倒角-----------------------------
            #MF=BRepFilletAPI_MakeChamfer(Rob)
            #MF.Add()
            # 移动
            ls_filename = filename[0:8] + "_4"
            move_distance = 0.5 * L - (L - float(self.SFU_serise_dict[ls_filename]["L"])) / 2
            cone = TopoDS_Shape(Rob)
            T = gp_Trsf()
            T.SetTranslation(gp_Vec(0, 0, -move_distance))
            loc = TopLoc_Location(T)
            cone.Location(loc)
            self.new_build.Add(self.aCompound, cone)
            print(type(self.aCompound))
            return self.aCompound

        except:
            return False

    def Create_Fk(self,filename="SFU01204-4",ss="FKFF8",L=100):
        pass
        if int(filename[3:6]) == 10 or int(filename[3:6]) == 12:
            ss = "FKFF08"
        if int(filename[3:6]) == 12 or int(filename[3:6]) == 14 or int(filename[3:6]) == 15 :
            ss = "FKFF10"
        if int(filename[3:6]) == 14 or int(filename[3:6]) == 15 or int(filename[3:6]) == 16 :
            ss = "FKFF12"
        if int(filename[3:6]) == 18 or int(filename[3:6]) == 20:
            ss = "FKFF15"
        if int(filename[3:6]) == 25 or int(filename[3:6]) == 28:
            ss = "FKFF20"
        if int(filename[3:6]) == 32 or int(filename[3:6]) == 36:
            ss = "FKFF25"
        if int(filename[3:6]) == 40 or int(filename[3:6]) == 50:
            ss = "FKFF30"
        "获取选择零件名称  获取路径"
        # 获取零件名称
        try:
            pass
            new_shape = TopoDS_Shape()
            #filename = "SFU2005-4"
            # 获取相应零件的路径***************************************
            self.partpath = os.getcwd()
            self.partpath = self.partpath + "\\3Ddata" + "\\STP" + "\\" + filename + ".stp"
            self.shape = read_step_file(self.partpath)
            self.shape.Free(True)  # 先释放shape
            # self.new_build.Add(self.aCompound,shape123)#将shaoe添加入复合体
            self.new_build.Add(self.aCompound, self.shape)
            #绘制丝杆**************************************************
            self.BK_serise_dict[ss]["D3"]=int(filename[3:6])#重新设置丝杆直径
            #print(filename[3:6])
            #PL = (L - 15 - 39 - 10) / 2
            PL = (L - self.BK_serise_dict[ss]["L1"] - self.BK_serise_dict[ss]["L2"]
                  - self.BK_serise_dict[ss]["L4"]) / 2
            #P1 = [0, 0, PL + 39 + 15]
            P1 = [0, 0, PL + self.BK_serise_dict[ss]["L3"] + self.BK_serise_dict[ss]["L1"]]
            #P2 = [0, 4, PL + 39 + 15]
            P2 = [0, self.BK_serise_dict[ss]["D1"]/2, PL + self.BK_serise_dict[ss]["L3"]
                  + self.BK_serise_dict[ss]["L1"]]
            #P3 = [0, 4, PL + 39]
            P3 = [0, self.BK_serise_dict[ss]["D1"]/2, PL + self.BK_serise_dict[ss]["L3"]]
            #P4 = [0, 5, PL + 39]
            P4 = [0, self.BK_serise_dict[ss]["D2"]/2, PL + self.BK_serise_dict[ss]["L3"]]
            #P5 = [0, 5, PL]
            P5 = [0, self.BK_serise_dict[ss]["D2"]/2, PL]
            #P6 = [0, 6, PL]
            P6 = [0, self.BK_serise_dict[ss]["D3"]/2, PL]
            #P7 = [0, 6, -PL]
            P7 = [0, self.BK_serise_dict[ss]["D3"]/2, -PL]
            #P8 = [0, 4, -PL]
            P8 = [0, self.BK_serise_dict[ss]["D1"]/2, -PL]
            #P9 = [0, 4, -PL - 7.9]
            P9 = [0, self.BK_serise_dict[ss]["D1"]/2, -PL - self.BK_serise_dict[ss]["L5"]]
            #P10 = [0, 4 - 0.2, -PL - 7.9]
            P10 = [0, self.BK_serise_dict[ss]["D5"]/2, -PL - self.BK_serise_dict[ss]["L5"]]
            #P11 = [0, 4 - 0.2, -PL - 7.9 - 0.8]
            P11 = [0, self.BK_serise_dict[ss]["D5"]/2, -PL - self.BK_serise_dict[ss]["L5"] -
                   self.BK_serise_dict[ss]["L6"]]
            #P12 = [0, 4, -PL - 7.9 - 0.8]
            P12 = [0, self.BK_serise_dict[ss]["D1"]/2, -PL - self.BK_serise_dict[ss]["L5"] -
                   self.BK_serise_dict[ss]["L6"]]
            #P13 = [0, 4, -PL - 10]
            P13 = [0, self.BK_serise_dict[ss]["D1"]/2, -PL - self.BK_serise_dict[ss]["L4"]]
            #P14 = [0, 0, -PL - 10]
            P14 = [0, 0, -PL - self.BK_serise_dict[ss]["L4"]]
            E11 = BRepBuilderAPI_MakeEdge(gp_Pnt(P1[0], P1[1], P1[2]), gp_Pnt(P2[0], P2[1], P2[2])).Edge()
            E12 = BRepBuilderAPI_MakeEdge(gp_Pnt(P2[0], P2[1], P2[2]), gp_Pnt(P3[0], P3[1], P3[2])).Edge()
            E13 = BRepBuilderAPI_MakeEdge(gp_Pnt(P3[0], P3[1], P3[2]), gp_Pnt(P4[0], P4[1], P4[2])).Edge()
            E14 = BRepBuilderAPI_MakeEdge(gp_Pnt(P4[0], P4[1], P4[2]), gp_Pnt(P5[0], P5[1], P5[2])).Edge()
            E15 = BRepBuilderAPI_MakeEdge(gp_Pnt(P5[0], P5[1], P5[2]), gp_Pnt(P6[0], P6[1], P6[2])).Edge()
            E16 = BRepBuilderAPI_MakeEdge(gp_Pnt(P6[0], P6[1], P6[2]), gp_Pnt(P7[0], P7[1], P7[2])).Edge()
            E17 = BRepBuilderAPI_MakeEdge(gp_Pnt(P7[0], P7[1], P7[2]), gp_Pnt(P8[0], P8[1], P8[2])).Edge()
            E18 = BRepBuilderAPI_MakeEdge(gp_Pnt(P8[0], P8[1], P8[2]), gp_Pnt(P9[0], P9[1], P9[2])).Edge()
            E19 = BRepBuilderAPI_MakeEdge(gp_Pnt(P9[0], P9[1], P9[2]), gp_Pnt(P10[0], P10[1], P10[2])).Edge()
            E20 = BRepBuilderAPI_MakeEdge(gp_Pnt(P10[0], P10[1], P10[2]), gp_Pnt(P11[0], P11[1], P11[2])).Edge()
            E21 = BRepBuilderAPI_MakeEdge(gp_Pnt(P11[0], P11[1], P11[2]), gp_Pnt(P12[0], P12[1], P12[2])).Edge()
            E22 = BRepBuilderAPI_MakeEdge(gp_Pnt(P12[0], P12[1], P12[2]), gp_Pnt(P13[0], P13[1], P13[2])).Edge()
            E23 = BRepBuilderAPI_MakeEdge(gp_Pnt(P13[0], P13[1], P13[2]), gp_Pnt(P14[0], P14[1], P14[2])).Edge()
            E24 = BRepBuilderAPI_MakeEdge(gp_Pnt(P14[0], P14[1], P14[2]), gp_Pnt(P1[0], P1[1], P1[2])).Edge()

            new_charme = ChFi2d_ChamferAPI()
            new_charme.Init(E11,E12)
            new_charme.Perform()
            E25 = new_charme.Result(E11, E12, 1.0, 1.0)#倒角1

            new_charme.Init(E13,E14)
            new_charme.Perform()
            E26=new_charme.Result(E13,E14,0.5,0.5)#倒角2

            new_charme.Init(E15,E16)
            new_charme.Perform()
            E27=new_charme.Result(E15,E16,0.5,0.5)#倒角3

            new_charme.Init(E16, E17)
            new_charme.Perform()
            E28 = new_charme.Result(E16, E17, 0.5, 0.5)  # 倒角4

            new_charme.Init(E22, E23)
            new_charme.Perform()
            E29 = new_charme.Result(E22, E23, 0.5, 0.5)  # 倒角5

            #print(type(E11))
            #print(E29.IsNull())

            W1 = BRepBuilderAPI_MakeWire(E11, E25,E12).Wire()
            W2 = BRepBuilderAPI_MakeWire(E13, E26, E14).Wire()
            W3 = BRepBuilderAPI_MakeWire(E15, E27, E16).Wire()
            W4 = BRepBuilderAPI_MakeWire(E16, E28, E17).Wire()
            W5 = BRepBuilderAPI_MakeWire(E18, E19, E20,E21).Wire()
            W6 = BRepBuilderAPI_MakeWire(E22, E29, E23, E24).Wire()
            #print("succeed")


            mkWire = BRepBuilderAPI_MakeWire()
            mkWire.Add(W1)
            mkWire.Add(W2)
            mkWire.Add(W3)
            mkWire.Add(W4)
            mkWire.Add(W5)
            mkWire.Add(W6)
            Rob = BRepPrimAPI_MakeRevol(BRepBuilderAPI_MakeFace(mkWire.Wire()).Face(),
                                      gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))).Shape()
            #倒角-----------------------------
            #MF=BRepFilletAPI_MakeChamfer(Rob)
            #MF.Add()
            # 移动
            ls_filename = filename[0:8] + "_4"
            move_distance = 0.5 * L - (L - float(self.SFU_serise_dict[ls_filename]["L"])) / 2
            cone = TopoDS_Shape(Rob)
            T = gp_Trsf()
            T.SetTranslation(gp_Vec(0, 0, -move_distance))
            loc = TopLoc_Location(T)
            cone.Location(loc)
            self.new_build.Add(self.aCompound, cone)
            print(type(self.aCompound))
            return self.aCompound

        except:
            return False






