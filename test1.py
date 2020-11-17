# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 19:15:11 2020

@author: Iris
"""

# -*- coding: utf-8 -*-

import wx
import pandas as pd
import os
import numpy as np
import re
import PIL.Image as Image
import cv2
from matplotlib import pyplot as plt
from matplotlib_venn import venn2
#from PIL import Image 
from matplotlib.backends.backend_agg import FigureCanvasAgg

class MainWindow(wx.Frame):
    """We simply derive a new class of Frame."""
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title = title, size = (400, 600)) 
            #the size of the frame
       #self.control = wx.TextCtrl(self, style = wx.TE_MULTILINE, 
       #                           size = (600, 200))
            #wx.TE_MULTILINE Allows multi-line editing
            ##self.control (control is replaceable)      \
            ##   wx.TextCtrl Declare a simple text editor
        self.CreateStatusBar()    #创建位于窗口的底部的状态栏
        
        #设置菜单
        filemenu1 = wx.Menu()

        #wx.ID_ABOUT和wx.ID_EXIT是wxWidgets提供的标准ID
        menuabout = filemenu1.Append(wx.ID_ABOUT, 'about', 
                                     'info about this app')  
        #u"关于"显示在菜单栏中，  u"关于程序的信息"显示在窗口底部的状态栏
        filemenu1.AppendSeparator()
        menuexit = filemenu1.Append(wx.ID_EXIT, 'exit', "terminate the app")

        #创建菜单栏  
        #一个界面理论上应该只设置一个菜单栏
        #菜单栏下的菜单设置多个时，使用menubar.append添加
        menuBar = wx.MenuBar() #在frame中添加菜单栏 
        menuBar.Append(filemenu1, 'file') #在菜单栏中添加file menu1
        self.SetMenuBar(menuBar)


        #创建控件
        #sizer 1  raw data sizer: 2 buttons   1 listbox
        self.statictext1 = wx.StaticText(parent = self, label = 'raw data')
        self.buttonPD = wx.Button(self, -1, "PD load")
        self.buttonMQ = wx.Button(self, -1, "MQ load")
        self.listBoxraw = wx.ListBox(self, -1, size = (80, 120), choices = [],
                                  style = wx.LB_MULTIPLE) #?
        #sizer fasta
        #fasta file：每次load frame时自动load两个fasta文件，因此写在init里
        #read fasta file
        fastapath_human = 'D:\IRIS\SLST\shui\data_processing_interface\ResultsFromMQandPD\Fasta-Human-Total-UP000005640-20200601.fasta'
        with open(fastapath_human, 'r') as f:
            fasta = f.readlines()
        fasta_human = {}
        for line in fasta:
            if line.startswith('>'):
                name = line.split('|')[1]
                fasta_human[name] = ''
                lines = ''
            else:
                lines = lines + line.strip('\n')
                fasta_human[name] = lines
        fastapath_mouse = 'D:\IRIS\SLST\shui\data_processing_interface\ResultsFromMQandPD\Fasta-Mouse-Total-17038-20200520.fasta'
        with open(fastapath_mouse, 'r') as f:
            fasta = f.readlines()
        fasta_mouse = {}
        for line in fasta:
            if line.startswith('>'):
                name = line.split('|')[1]
                fasta_mouse[name] = ''
                lines = ''
            else:
                lines = lines + line.strip('\n')
                fasta_mouse[name] = lines
        #创建dict0， 储存fastaname 和fastafile
        self.dict0 = {}
        self.dict0['fasta_human'] = fasta_human
        self.dict0['fasta_mouse'] = fasta_mouse
        fastaname = ['fasta_human', 'fasta_mouse']
        self.listboxfasta = wx.ListBox(self, -1, size = (250, 40), 
                                       choices = fastaname,
                                       style = wx.LB_SINGLE)
        self.statictext4 = wx.StaticText(parent = self, label = 'FASTA file')
        
        #sizer 2 processed data sizer: 1 button   1 listbox
        self.statictext2 = wx.StaticText(parent = self, 
                                         label = 'processed data')
        self.buttonProcess = wx.Button(self, -1, "process")
        self.listboxprcsd = wx.ListBox(self, -1, size = (80, 120), 
                                       choices = [], style = wx.LB_MULTIPLE) #?
        #sizer 3 output sizer: 3 buttons
        self.statictext3 = wx.StaticText(parent = self, label = 'results')
        self.buttonSave = wx.Button(self, -1, "save files") #?
        self.buttonCompare = wx.Button(self, -1, "compare results")#?
        self.buttonSaveall = wx.Button(self, -1, "save all") #?
        
        #设计sizer布局
        vbox = wx.BoxSizer(wx.VERTICAL) #放sizer1 sizerfasta sizer2 and sizer3
        
        #sizer1
        vbox1 = wx.BoxSizer(wx.VERTICAL) #放buttonPD and buttonMQ
        hbox1 = wx.BoxSizer(wx.HORIZONTAL) #放2 buttons and listboxraw
        vbox1.Add(self.buttonPD, proportion = 1, flag = wx.LEFT | wx.TOP, 
                  border = 5)
        vbox1.Add(self.buttonMQ, proportion = 1, flag = wx.LEFT | wx.TOP, 
                  border = 5)
        hbox1.Add(vbox1, proportion =1, flag = wx.LEFT | wx.TOP, border = 10)
        hbox1.Add(self.listBoxraw, proportion = 3, flag = wx.LEFT | wx.TOP | 
                  wx.RIGHT, border = 10)
        vboxstatic1 = wx.BoxSizer(wx.VERTICAL)
        vboxstatic1.Add(self.statictext1, proportion = 1, flag = wx.TOP | 
                        wx.ALIGN_CENTER_HORIZONTAL, border = 20)
        vbox.Add(vboxstatic1, proportion = 0, flag = wx.TOP | 
                 wx.ALIGN_CENTER_HORIZONTAL, border = 0)
        vbox.Add(hbox1, proportion = 0, flag = wx.TOP, border = 0) 
                #将sizer1加入到vbox中
        #sizerfasta
        fastavbox = wx.BoxSizer(wx.VERTICAL)
        vboxstatic1 = wx.BoxSizer(wx.VERTICAL)
        fastavbox.Add(self.listboxfasta, proportion = 1, flag = wx.LEFT,
                      border = 5)
        vboxstatic1.Add(self.statictext4, proportion = 1, flag = wx.LEFT, 
                        border = 5)
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        hbox5.Add(vboxstatic1, proportion = 1, flag = wx.LEFT, border = 10)
        hbox5.Add(fastavbox, proportion = 3, flag = wx.RIGHT, border = 30)
        vbox.Add(hbox5, proportion = 0, flag = wx.TOP, border = 5)
        
        #sizer2
        hbox2 = wx.BoxSizer(wx.HORIZONTAL) #放buttonProcess and listboxprcsd
        vbox3 = wx.BoxSizer(wx.VERTICAL) #放buttonProcess
        vbox3.Add(self.buttonProcess, proportion = 1, flag = wx.LEFT | wx.TOP, 
                  border = 5)
        hbox2.Add(vbox3, proportion = 1, flag = wx.LEFT | wx.TOP, border = 10)
        hbox2.Add(self.listboxprcsd, proportion = 3, flag = wx.LEFT | wx.TOP | 
                  wx.RIGHT, border = 10)
        vboxstatic2 = wx.BoxSizer(wx.VERTICAL)
        vboxstatic2.Add(self.statictext2, proportion = 1, flag = wx.TOP | 
                        wx.ALIGN_CENTER_HORIZONTAL, border = 25)
        vbox.Add(vboxstatic2, proportion = 0, flag = wx.TOP | 
                 wx.ALIGN_CENTER_HORIZONTAL, border = 0)
        vbox.Add(hbox2, proportion = 0, flag = wx.TOP, border = 0) 
                #将sizer2放入vbox中
        #sizer3
        vbox4 = wx.BoxSizer(wx.VERTICAL)  #放3 buttons
        hbox3 = wx.BoxSizer(wx.HORIZONTAL) #放buttonsave
        hbox4 = wx.BoxSizer(wx.HORIZONTAL) #放buttonsave and button compare
        hbox3.Add(self.buttonSave, proportion = 1, flag = wx.LEFT, border = 50)
        hbox31 = wx.BoxSizer(wx.HORIZONTAL)
        hbox31.Add(self.buttonCompare, proportion = 1, flag = wx.RIGHT, 
                   border = 50)
        hbox4.Add(hbox3, proportion = 1, flag = wx.RIGHT, border = 20)
        hbox4.Add(hbox31, proportion = 1, flag = wx.LEFT, border = 20)
        vbox4.Add(hbox4, proportion = 1, flag = wx.TOP | wx.BOTTOM| 
                  wx.ALIGN_CENTER_HORIZONTAL, border = 15)
        vbox4.Add(self.buttonSaveall, proportion = 1, flag = wx.TOP | 
                  wx.ALIGN_CENTER_HORIZONTAL, border = 5)
        vboxstatic3 = wx.BoxSizer(wx.VERTICAL)
        vboxstatic3.Add(self.statictext3, proportion = 1, flag = wx.TOP | 
                        wx.ALIGN_CENTER_HORIZONTAL, border = 25)
        vbox.Add(vboxstatic3, proportion = 0, flag = wx.TOP | 
                 wx.ALIGN_CENTER_HORIZONTAL, border = 0)
        vbox.Add(vbox4, proportion = 0, flag = wx.TOP | wx.BOTTOM, border = 0)
        
        self.SetSizer(vbox)

        #创建dict1 储存filename 和 file
        self.dict1 = {}
        #创建list1 储存第二个listbox中得到的第一个listbox中的index
        #因为getsselections得到的是index。取dict1中的部分file做process后filename
        #存入第二个listbox时，index又从0开始，与dict1中的index无法对上
        #因此要创建一个新的list，储存在dict1中selected data的index
        self.key_idx_list1 = [] #储存所有在listboxraw中选中的idx
        #创建一个变量，用来储存venn diagram
        self.venn_diagram = None
        
        #设置events
        self.Bind(wx.EVT_MENU, self.Onabout, menuabout) 
        #wx.EVT_MENU 指定事件为菜单事件  self.Onabout 指定事件处理的方法为Onabout
        #menuabout 事件的来源 即控件
        
        ##2 buttons pd and mq   func: load files
        self.Bind(wx.EVT_MENU, self.Onexit, menuexit)
        
        self.Bind(wx.EVT_BUTTON, self.OnopenPD, self.buttonPD)
        self.Bind(wx.EVT_BUTTON, self.OnopenMQ, self.buttonMQ)
        
        ##1 button process   func: process the selected data
        #self.Bind(wx.EVT_LISTBOX, self.process, self.listBoxraw)
        self.Bind(wx.EVT_BUTTON, self.processbutton, self.buttonProcess)
        
        #1 button save  func: save the selected data
        self.Bind(wx.EVT_BUTTON, self.save_files, self.buttonSave)
        
        #1 button compare  func: compare the selected data
        #(the number of selected data should be <=3)
        self.Bind(wx.EVT_BUTTON, self.compare, self.buttonCompare)
        
        #self.Show(True)
        
    def Onabout(self, event):
        # 创建一个带"OK"按钮的对话框。wx.OK是wxWidgets提供的标准ID
        dlg = wx.MessageDialog(self, "a small editor.",\
                               "about sample editor", wx.OK)
            #grammar: (self, content, title, ID)   wx.OK可省略
        dlg.ShowModal()  #展示对话框
        dlg.Destroy()   #当结束之后关闭对话框
        
    def Onexit(self, event):
        self.Close(True)  #close the whole frame
    
    def OnopenPD(self, event):
        #open a PD file
        dlg = wx.FileDialog(None, 'wxpython Notebook', style = wx.FD_OPEN) 
           #in new version of python, use wx.FD_OPEN instead of wx.OPEN
        if dlg.ShowModal() == wx.ID_OK:
            file_path = dlg.GetPath()          
            n = len(self.dict1) + 1
            filename = dlg.GetFilename()
            filename = filename.rstrip('.xlsx')
            self.filename = f'{filename}_PD_{str(n)}'          
            ppdd = PD(filepath = file_path)
            #self.dict1[name0].raw_data  进入这个类的实例后可以直接调用里面的参数
            #调用class PD里的变量时用这个 因为dict的value中存的是class PD的实例
            self.dict1[self.filename] = ppdd
            self.listBoxraw.Append(self.filename)
            
        dlg.Destroy()
        
    def OnopenMQ(self, event):
        #open a PD file
        dlg = wx.FileDialog(None, 'wxpython Notebook', style = wx.FD_OPEN) 
           #in the new version of wxpython, use wx.FD_OPEN instead of wx.OPEN
        if dlg.ShowModal() == wx.ID_OK:
            file_path = dlg.GetPath()
            n = len(self.dict1) + 1
            filename = dlg.GetFilename()
            filename = filename.rstrip('.txt')
            self.filename = f'{filename}_MQ_{str(n)}'
            mmqq = MQ(filepath = file_path)
            self.dict1[self.filename] = mmqq
            self.listBoxraw.Append(self.filename)
            
        dlg.Destroy()
        
    def processbutton(self, e):
        self.file_key_index = self.listBoxraw.GetSelections()
        self.key_idx_list1.extend(self.file_key_index)
        #self.key_idx_list1 = list(chain.from_iterable(self.key_idx_list1))
            #2d--->1d
        self.key_idx_list1 = list(set(self.key_idx_list1)) #去重
        self.key_idx_list1.sort(reverse = False) #idx从小到大排序
        fastafilename = self.listboxfasta.GetStringSelection()
        file_key_index = self.file_key_index
        print(file_key_index)
        print(f'self.key_idx_list1 = {self.key_idx_list1}')
        for idx in file_key_index:
            #可能选中了多个raw data
            file_key = list(self.dict1.keys())[idx] #返回key
            self.dict1[file_key].process(seq = self.dict0[fastafilename])
            self.listboxprcsd.Append(file_key)
            #self.list1.Append()
            print(file_key)
        
        print(fastafilename)
    
    def save_files(self, event):
        #save selected files
        self.dir_name = '' #储存路径
        #fd = wx.FileDialog(self, 'path', self.dir_name, '.txt', \
         #                  'TEXT file(*.txt)|*.txt', wx.FD_SAVE)
        fd = wx.FileDialog(self, 'path', self.dir_name, '.xlsx', \
                           'EXCEL file(*.xlsx)|*.xlsx', wx.FD_SAVE)
        if fd.ShowModal() == wx.ID_OK:    
            selected_idx = self.listboxprcsd.GetSelections() #返回的是listbox2的index
            for idx in selected_idx:
                dict1_idx = self.key_idx_list1[idx]  
                    #根据listbox2的index来取listbox1的index
                dict1_key = list(self.dict1.keys())[dict1_idx] #返回key
                filecontent = self.dict1[dict1_key].returnprocessdata()
                self.file_name =  f'{dict1_key}_result' #文件名
                self.dir_name = fd.GetDirectory()
                try:
                    #with open(os.path.join(self.dir_name, self.file_name), \
                     #         'w', encoding = 'utf-8') as f:
                      #  f.to_csv(filecontent)                   
                    filecontent.to_excel(os.path.join(self.dir_name, f'{self.file_name}.xlsx'))
                except FileNotFoundError:
                    save_msg = wx.MessageDialog(self, 'AN ERROR OCCURED', \
                                                'ERROR')
                    save_msg.ShowModal()
                    save_msg.Destroy()
            
    def compare(self, event):
        selected_idx = self.listboxprcsd.GetSelections()
        sel = []
        print(self.file_key_index)
        print(selected_idx)
        if len(selected_idx) == 1 :
            warn_msg = wx.MessageDialog(self, 
            'The number of selected data must be over 1 but no more than 3')
            warn_msg.ShowModal()
            warn_msg.Destroy()
        if len(selected_idx) > 3 :
            warn_msg = wx.MessageDialog(self, 
            'The number of selected data must be over 1 but no more than 3')
            warn_msg.ShowModal()
            warn_msg.Destroy()
        if len(selected_idx) == 2:
            keys = []
            for idx in selected_idx:
                dict1_idx = self.key_idx_list1[idx]
                dict1_key = list(self.dict1.keys())[dict1_idx] #返回key
                keys.append(dict1_key)
                sel.append(self.dict1[dict1_key].returnprocessdata()) 
                    #sel储存选取的processed data                
            sel_phosprotein = []
            sel_phospeptide = []
            sel_phossite = []
            for i in range(len(sel)):
                sel_phosprotein.append(sel[i]['PhosProtein'])
                sel_phospeptide.append(sel[i]['PhosPeptide'])
                sel_phossite.append(sel[i]['PhosSite'])
                print(i)
            napos_pro = []
            diff_pro = [] #protein 和site的index是一样的
            accessions = []
            sites = []
            for i in range(len(sel_phosprotein)):
                napos = sel_phosprotein[i][sel_phosprotein[i].isnull()].index.tolist()
                napos_pro.append(napos)
                diff = list(set(list(range(len(sel_phosprotein[i])))).difference(set(napos)))
                diff_pro.append(diff)
                accession = np.unique(sel_phosprotein[i][diff])
                accessions.append(accession)
                site = sel_phossite[i][diff].str.split(';')
                ss = []
                for p in site:
                    print(p)
                    if len(p) == 1:
                        ss.append(p[0])
                    else:
                        for w in p:
                            ss.append(w)
                site = np.unique(ss)                
                sites.append(site)
                
            napos_pep = []
            diff_pep = []
            modiseqs = []
            for i in range(len(sel_phospeptide)):
                napos = sel_phospeptide[i][sel_phospeptide[i].isnull()].index.tolist()
                napos_pep.append(napos)
                diff = list(set(list(range(len(sel_phospeptide[i])))).difference(set(napos)))
                diff_pep.append(diff)
                modiseq = np.unique(sel_phospeptide[i][diff])
                modiseqs.append(modiseq)
            print(len(sites[0]))
            
            fig,axs=plt.subplots(1,3, figsize=(6,3),dpi=300)
            #fig.suptitle("Comparison")
            axs[0].set_title("PhosProtein")
            axs[1].set_title("PhosPeptide")
            axs[2].set_title("PhosSite")
            """
            v = venn2(subsets = [set(accessions[0]), set(accessions[1])],
                      set_labels = (keys[0], keys[1]),
                      set_colors = ('b', 'g'),
                      alpha = 0.6,
                      normalize_to = 1.0,
                      ax = axs[0])
            v = venn2(subsets = [set(modiseqs[0]), set(modiseqs[1])],
                      set_labels = (keys[0], keys[1]),
                      set_colors = ('b', 'g'),
                      alpha = 0.6,
                      normalize_to = 1.0,
                      ax = axs[1])
            v = venn2(subsets = [set(sites[0]), set(sites[1])],
                      set_labels = (keys[0], keys[1]),
                      set_colors = ('b', 'g'),
                      alpha = 0.6,
                      normalize_to = 1.0,
                      ax = axs[2])
            """
            # fig.tight_layout()
            plt.show()

            #vd = np.array(v)
            #print(vd.shape, vd.dtype)
            w_h = fig.canvas.get_width_height()
            print(w_h)
            print(np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8).shape)
            buf = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8).reshape(*w_h, 3)
            buf = np.roll(buf, 3, axis = 2)
            im = Image.frombytes("RGB", w_h, buf.tostring())
            im = np.asarray(im)
            
            #self.venn_diagram = im
            f2 = subwindow(None, title = 'diagram', image = im)#self.venn_diagram)
            
            f2.Show(True)
                
            
class PD(object):
    def __init__(self, filepath):
        self.file_path = filepath
        self.pd_raw = self.read_data()
        
        self.pd_process = None
    
    def read_data(self):
        #with open(self.file_path, 'r') as f:
        pd_data = pd.read_excel(self.file_path)
        return pd_data
    
    def process(self, seq):
        pd_data = self.pd_raw
        bestphossite = pd_data['ptmRS: Best Site Probabilities'] 
                     #ptmRS: Phospho Site Probabilities
        PhosProtein = pd.Series("", index = list(range(pd_data.shape[0])))
        PhosPeptide = pd.Series("", index = list(range(pd_data.shape[0])))
        PhosSite = pd.Series("", index = list(range(pd_data.shape[0])))
    
        semicolon = bestphossite.str.split(';')
        napos = semicolon[semicolon.isnull()].index.tolist() #score == nan
        diff = list(set(list(range(len(semicolon)))).difference(set(napos)))
    
        accession = pd_data['Protein Accessions']
        accession = accession.str.split(';')
        for q in diff:
            #如果accession中有两个，取前一个
            accession[q] = accession[q][0]
         
        modification = pd_data['Modifications'].str.split(';')
        car = 'Carbamidomethyl'
        for v in diff:
            vv = modification[v]
            uu = []
            for u in range(len(vv)):
                if vv[u].find(car) != -1:
                    uu.append(u) #car的index
            uu.sort(reverse = True)
            for uuu in uu:
                del vv[uuu]
            modification[v] = vv
    
        for j in diff:
            print(j)
            row_j = semicolon[j]
            scores = []
            for k in row_j:
                begin = k.find(':')
                score = float(k[begin + 2 : len(k)]) #type str
                scores.append(score)
        
            scores = np.array(scores)
            score75 = scores > 75
            if score75.any(): 
                #存在score>75% phosprotein 和phossite都进行操作
                #phossite  format : accession-S/T/Y-site
                #pro_seq = seq[accession[j]]
                pro_seq = seq.get(accession[j], 0)
            
                if pro_seq != 0:
                    PhosProtein[j] = accession[j] #phosprotein
                    pep_seq = pd_data['Sequence'][j]
                    pep_loc = pro_seq.find(pep_seq) 
                        #the loc of pep_seq in pro_seq
                    phos_site = []
            
                    index75 = np.argwhere(score75 == True)
                    index75 = index75.tolist()
                    from itertools import chain
                    index75 = list(chain.from_iterable(index75))
            
                    row_j75 = row_j[index75[0] : index75[len(index75) - 1] + 1]
                    for x in row_j75:
                        sty = re.findall('S|T|Y', x)[0] 
                        site = int(x[x.find(sty) + 1 : x.find('(')])
                        pro_loc = pep_loc + site  #-1 #phos site in protein
                        phossite_x = f'{accession[j]}-{sty}{pro_loc}' 
                        phos_site.append(phossite_x)
                    phos_site = ';'.join(phos_site)
                    PhosSite[j] = phos_site
            
                    if score75.all():
                        #存在all score>75% phospeptide进行操作
                        modi = modification[j] 
                            #already delete the condition of car
                
                        acetyl = 'N-Term(Prot)(Acetyl)'
                        phos = '(Phospho)'
                        oxi = '(Oxidation)'
                
                            #condition 1: acetyl exists
                        phos_index = [] 
                        oxi_index = []
                        for u in modi:
                            if u.find(phos) != -1:
                                sty = re.findall('S|T|Y', u)[0]
                                loc = int(u[u.find(sty) + 1 : u.find('(')])
                                phos_index.append(loc)
                            elif u.find(oxi) != -1:
                                loc = int(u[u.find('M') + 1 : u.find('(')])
                                oxi_index.append(loc)
                        phos_index.sort(reverse = True)
                        oxi_index.sort(reverse = True)
                
                        phos_dict = dict(zip(phos_index,['(Phospho (STY))'] * 
                                             len(phos_index)))
                        oxi_dict = dict(zip(oxi_index,['(Oxidation (M))'] * 
                                            len(oxi_index)))
                        phos_oxi_dict = {}
                        phos_oxi_dict.update(phos_dict)
                        phos_oxi_dict.update(oxi_dict)
                        phos_oxi_dict=sorted(phos_oxi_dict.items(),
                                             key=lambda x:x[0],reverse = True)
                
                        modseq = list(pep_seq)
                        for u in phos_oxi_dict:
                            loc = u[0]
                            modseq.insert(loc,u[1])
                        modseq = ''.join(modseq)
                        if any(acetyl in s for s in modi):
                            modseq = f'(Acetyl (Protein N-term)){modseq}'
                        modseq = f'_{modseq}_'
                
                        PhosPeptide[j] = modseq
        pd_data['PhosProtein'] = PhosProtein
        pd_data['PhosPeptide'] = PhosPeptide
        pd_data['PhosSite'] = PhosSite

        self.pd_process = pd_data
        
    def returnprocessdata(self):
        reprcsddata = self.pd_process
        return reprcsddata
        
class MQ(object):
    def __init__(self, filepath):
        self.file_path = filepath
        self.mq_raw = self.read_data()
        self.mq_process = None
        
    def read_data(self):
        #with open(self.file_path, 'r') as f:
         #   mq_data = f.readlines()
        mq_data = pd.read_csv(self.file_path, sep='\t')
        return mq_data
    
    def process(self, seq):
        mq_data = self.mq_raw
        mod_seq = mq_data['Modified sequence']
        phosprobability = mq_data['Phospho (STY) Probabilities']
        
        PhosProtein = pd.Series("", index = list(range(mq_data.shape[0])))
        PhosPeptide = pd.Series("", index = list(range(mq_data.shape[0])))
        PhosSite = pd.Series("", index = list(range(mq_data.shape[0])))
        
        accession = mq_data['Proteins']
        accession = accession.str.split(';')
        napos = list(set(phosprobability[phosprobability.isnull()].index.tolist()).
                     union(set(accession[accession.isnull()].index.tolist())))
        diff = list(set(list(range(len(mod_seq)))).difference(set(napos)))
        
        for q in diff:
            accession[q] = accession[q][0]
            
        for j in diff:
            print(j)
            mod_seq_j = mod_seq[j].split('_')[1]
            if mod_seq_j.find('(Acetyl (Protein N-term))') != -1:
                #除去acetyl以避免其对之后对sty进行处理时造成的影响
                mod_seq_j = mod_seq_j.replace('(Acetyl (Protein N-term))', '', 1)
            while mod_seq_j.find('(Oxidation (M))') != -1:
                #用while是因为不知道oxi的个数，但是n端acetyl只有一个，可以直接用if
                mod_seq_j = mod_seq_j.replace('(Oxidation (M))', '', 1)
            
            phosprobab_j = phosprobability[j]
            sites = [] #储存需要去phosprobab中查询分数的site的位置
            site_fraction = {}
            while mod_seq_j.find('(Phospho (STY))') != -1:
                site = mod_seq_j.find('(Phospho (STY))') -1 #从0开始
                sty = f'{mod_seq_j[site]}{site}'
                mod_seq_j = mod_seq_j.replace('(Phospho (STY))', '', 1)    
                sites.append(sty)
                
            while phosprobab_j.find('(') != -1:
                begin = phosprobab_j.find('(') +1
                end = phosprobab_j.find(')')
                fraction = float(phosprobab_j[begin : end])
                site = f'{phosprobab_j[begin-2]}{begin - 2}' #从0开始
                site_fraction[site] = fraction
                patterns = re.search('(\(.*?\))', phosprobab_j).group()
                phosprobab_j = phosprobab_j.replace(patterns, '', 1)
                
            pro_seq = seq.get(accession[j], 0)
            
            if pro_seq != 0:
                pep_loc = pro_seq.find(mod_seq_j) #the loc of pep_seq in pro_seq
                phos_site = []
                count75 = [] #计数mod_seq中分数大于0.75的个数
                for k in sites:
                    if site_fraction[k] > 0.75:
                        count75.append(k)
                        pro_loc = pep_loc + int(k[1 : len(k)]) + 1  
                        #最终在protein上的位置从1开始计数
                        sty = k[0]
                        phossite_k = f'{accession[j]}-{sty}{pro_loc}'
                        phos_site.append(phossite_k)
                phos_site = ';'.join(phos_site)
                PhosSite[j] = phos_site #phossite
                if len(count75) > 0:
                    PhosProtein[j] = accession[j] #phosprotein
                    if len(count75) == len(sites):
                        #如果这两者数值相等，说明在mod_seq中的所有位点均大于0.75
                        #可以进行phospeptide操作
                        PhosPeptide[j] = mod_seq[j]
        mq_data['PhosProtein'] = PhosProtein
        mq_data['PhosPeptide'] = PhosPeptide
        mq_data['PhosSite'] = PhosSite

        self.mq_process = mq_data
        
    def returnprocessdata(self):
        reprcsddata = self.mq_process
        print(reprcsddata['PhosProtein'][1])
        return reprcsddata
        
#app = wx.App(False)
#frame = MainWindow(None, title = u"data processing")
#app.MainLoop()
class subwindow(wx.Frame):
   def __init__(self, parent, title, image):
       wx.Frame.__init__(self, parent, title = title, size = (300, 200))
       self.statictext = wx.StaticText(parent = self, 
                                       label = 'The comparison of two files')
       #从mainwindow中传入的image的type是ndarray
       #将ndarray图像转换为cv图像并显示
       img = cv2.cvtColor(np.uint8(image), cv2.COLOR_BGR2RGB)
       h, w = img.shape[:2]
           #get the height and width of the source image for buffer construction
       #wxbmp = wx.BitmapFromBuffer(w, h, img)
       wxbmp = wx.Bitmap.FromBuffer(w, h, img)
       #wxbmp = wx.Bitmap.FromBufferAndAlpha(w, h, img)
           #make a wx style bitmap using the buffer converter
       #image = wx.Image(image, wx.BITMAP_TYPE_PNG)
       #img = Image.fromarray(image*255.0/9999)
       #img = img.convert('L')
       #temp = image.ConvertToBitmap()
       self.bmp = wx.StaticBitmap(parent = self, bitmap = wxbmp)
       #mainwindow = MainWindow(None, title = 'data processing')
       #self.vedi = mainwindow.venn_diagram
       
       self.buttonsavevd = wx.Button(self, -1, "save")
       
       #布局
       vbox1 = wx.BoxSizer(wx.VERTICAL) #总的box
       hbox1 = wx.BoxSizer(wx.HORIZONTAL) #statictext
       hbox2 = wx.BoxSizer(wx.HORIZONTAL) #image
       hbox3 = wx.BoxSizer(wx.HORIZONTAL) #buttonsavevd
       hbox1.Add(self.statictext, proportion = 1, flag = wx.TOP, border = 10)
       hbox2.Add(self.bmp, proportion = 1, flag = wx.TOP, border = 10)
       hbox3.Add(self.buttonsavevd, proportion = 1, flag = wx.TOP, border = 10)
       vbox1.Add(hbox1, proportion = 1, flag = wx.ALIGN_CENTER_HORIZONTAL, 
                 border = 10)
       vbox1.Add(hbox2, proportion = 3, flag = wx.ALIGN_CENTER_HORIZONTAL,
                 border = 10)
       vbox1.Add(hbox3, proportion = 1, flag = wx.ALIGN_CENTER_HORIZONTAL,
                 border = 10)
       
       self.SetSizer(vbox1)
       #self.Show(True)
       #temp = self.vedi.ConvertToBitmap()    
       #size = temp.GetWidth(), temp.GetHeight()         
       #self.bmp = wx.StaticBitmap(parent=self, bitmap=temp)     
       
      
class MyApp(wx.App):
    def OnInit(self):
        self.myframe = MainWindow(None, title = 'data processing')
        #mainwindow = MainWindow(None, title = 'data processing')
        #self.vedi = mainwindow.venn_diagram
        #self.myframe2 = subwindow(None, title = 'diagram', image = mainwindow.venn_diagram)
        self.SetTopWindow(self.myframe)
        
        self.myframe.Show(True)
        #self.myframe2.Show(True)
        return True

if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()







