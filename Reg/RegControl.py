

import sys
import os

# print(sys.path[0].replace('\\','/'))
#os.chdir(sys.path[0])

from LIB.ISP_FTDI import *
import tkinter
import tkinter.font
from tkinter.ttk import *
import threading
from time import *
import queue


class bitBT_1 ():
    def __init__(self, bitBT, index):
        self.Button_Wr=bitBT.Button_Wr
        self.button=tkinter.Button(bitBT.pan, width=1, text=("0"), relief='solid',borderwidth=0, command=self.Button_TG)
        # bt_font=tkinter.font.Font(size=8)
        self.btlabel=tkinter.ttk.Label(bitBT.pan, width=2, text=index)#, font=bt_font)
        self.mode = 0

    def Button_enable(self,mode):
        if(mode==0) :
            self.button.configure(fg='black', bg='#f0f0f0', borderwidth=1)
        elif(mode==1) :
            self.button.configure(fg='gray', bg='#f0f0f0',borderwidth=0)
        elif(mode==2) :
            self.button.configure(fg='#808080', bg='#f0f0f0',borderwidth=1)
        self.mode=mode
        # self.button.configure(state='normal')
        # self.button.config(style='TButton')

    # def Button_enable2(self):
    #     self.button.configure(fg='black', bg='#FFFFFF', borderwidth=1)
    #     # self.button.configure(state='normal')
    #     # self.button.config(style='TButton')

    # def Button_enable3(self):
    #     self.button.configure(fg='black', bg='#528080', borderwidth=1)
    #     # self.button.configure(state='normal')
    #     # self.button.config(style='TButton')

    def Button_stateget(self):
        return  self.mode

    def Button_statedis(self):
        return  self.mode==1

    def Button_get(self):
        return  int(self.button.configure('text')[4])

    def Button_geten(self):
        return  self.mode==0

    def Button_set(self,set_button):
        self.button.configure(text=set_button)

    def Button_TG(self):
        # set_button = self.RegPan[self.CADDR_get()].Read_Update()
        if(self.Button_get()==1)    : self.button.configure(text=0)
        else                        : self.button.configure(text=1)
        self.Button_Wr(self.mode)
        self.button.focus_set()

class bitBT ():
    def __init__(self,GUI_TOP):
        self.pan=GUI_TOP.pan
        self.RegPan=GUI_TOP.RegPan
        self.CADDR_get =GUI_TOP.CADDR_get
        # tkinter.ttk.Style().configure('TButton', foreground='black')
        # tkinter.ttk.Style().configure('Disable.TButton', foreground='gray')
        # tkinter.ttk.Style().configure('Disable2.TButton', foreground='white')

        self.incbox=tkinter.Spinbox(self.pan,width=2,justify='center',from_=0, to=31, command=self.Incbox_Set)
        self.incbox.place(x=573,y=3)
        self.incbox.bind("<Return>", self.Incbox_Set_E)
        self.incbox.bind("<Tab>", self.Incbox_Set_E)

        self.bitbutton=[]
        Xpos=570
        for i in range(0,32):
            if(i%8 == 0) :   Xpos = Xpos - 12
            if(i%4 == 0) :   Xpos = Xpos - 3
            self.bitbutton.append(bitBT_1(self,i))
            self.bitbutton[i].button.place(x=Xpos,y=0)
            self.bitbutton[i].btlabel.place(x=Xpos,y=25)
            Xpos = Xpos - 16



    def Incbox_Set_E(self,event):
        self.Incbox_Set()

    def Incbox_Set(self):
        incdata = int(self.incbox.get())
        addr = self.CADDR_get()&((1<<4)-1)
        self.RegPan[addr].writedata.config(increment=1<<incdata)
        for i in range(0,32):
            # if str(self.bitbutton[i].Button_stateget())!='gray' :
            # if(self.RegPan[addr].mnecombo['values'].index(self.RegPan[addr].mnecombo.get())==0):
            #     if(incdata<=0)   :
            #         # self.bitbutton[i].button.config(style='TButton')
            #         # self.bitbutton[i].button.config(fg='black')
            #         # self.bitbutton[i].Button_enable()
            #         incdata=incdata-1
            #     else            :
            #         # self.bitbutton[i].button.config(style='Disable.TButton')
            #         # self.bitbutton[i].button.config(fg='#808080')
            #         self.bitbutton[i].Button_enable(2)
            #         incdata=incdata-1
            # else:
            if not self.bitbutton[i].Button_statedis() :
                if(incdata<=0)   :
                    # self.bitbutton[i].button.config(style='TButton')
                    # self.bitbutton[i].button.config(fg='black')
                    self.bitbutton[i].Button_enable(0)
                    incdata=incdata-1
                else            :
                    # self.bitbutton[i].button.config(style='Disable.TButton')
                    # self.bitbutton[i].button.config(fg='#808080')
                    self.bitbutton[i].Button_enable(2)
                    incdata=incdata-1


    def Button_Wr(self,mode):
        get_button=0
        addr = self.CADDR_get()&((1<<4)-1)
        for i in range(0,32):
            get_button = get_button|int(self.bitbutton[i].Button_get())<<i
            # get_en = get_button|int(self.bitbutton[i].Button_geten())<<i
        # self.RegPan[self.CADDR_get()&((1<<4)-1)].Write_Hex(get_button,1)
        # self.RegPan[self.CADDR_get()&((1<<4)-1)].Write_Hex(get_button,0,0,get_en,0)
        # self.RegPan[self.CADDR_get()&((1<<4)-1)].Write_Update(get_button)
        index=self.RegPan[addr].mnecombo['values'].index(self.RegPan[addr].mnecombo.get())
        if(index==0):
            writedata = get_button
            # self.RegPan[addr].Write_Update(get_button)
            self.RegPan[addr].Write_Hex(writedata,1)
        else:
            en, bits, bit =self.RegPan[addr].Get_en(index)
            writedata = (get_button&en)>>bits
            # printh(writedata)
            # self.RegPan[addr].Write_Hex(writedata,0)
            self.RegPan[addr].Write_Hex(writedata,1,0,en,bits)
            self.RegPan[addr].Write_Update(get_button)


    def Button_Ld(self,set_button):
        # incdata = int(self.incbox.get())
        # print(incdata)
        for i in range(0,32):
            self.bitbutton[i].Button_set((set_button&(1<<i))>>i)
            set_button = (set_button>>i)<<i
        self.Incbox_Set()
        # printh(set_button)


class RegPannel():
    # Register address name & Read/data area
    def __init__(self,addr,name,GUI_TOP):
        # Top module variables
        self.pan = GUI_TOP.pan
        self.BitPan=GUI_TOP.BitPan
        self.RegPan=GUI_TOP.RegPan
        self.incbox=GUI_TOP.BitPan.incbox
        self.CADDR_set =GUI_TOP.CADDR_set
        # self.CADDR_get =GUI_TOP.CADDR_get
        self.Read_thread_set =GUI_TOP.Read_thread_set
        self.Read_thread_off =GUI_TOP.Read_thread_off
        self.mode =GUI_TOP.mode
        self.slv_addr =GUI_TOP.slv_addr
        self.Byte =GUI_TOP.Byte
        self.AByte =GUI_TOP.AByte
        self.LSB =GUI_TOP.LSB

        # initial address & data
        self.staddr=((addr>>4)<<4)
        self.addr=addr
        self.writereg=0

        # Widget initial
        self.addlabel=tkinter.Label(self.pan, width=6, text=addr)
        self.mnecombo=tkinter.ttk.Combobox(self.pan, width=76)
        self.readdata=tkinter.Label(self.pan,width=11, height=1,relief='groove')
        self.writedata=tkinter.Spinbox(self.pan,width=11, justify='center',from_=hex(-1), to=hex((1<<32)-1), command=self.Spin_Write_Hex)

        # event bind
        self.mnecombo.bind("<FocusIn>", self.Add_Sel_E)
        self.readdata.bind("<FocusIn>", self.Add_Sel_E)
        self.writedata.bind("<FocusIn>", self.Add_Sel_E)

        self.writedata.bind("<Return>", self.Spin_Write_Hex_E)
        self.writedata.bind("<Tab>", self.Spin_Write_Hex_E)
        self.readdata.bind("<Double-Button-1>", self.Read_Repeat_E)
        self.mnecombo.bind("<Button-3>", self.Drop_Down)
        self.mnecombo.bind("<<ComboboxSelected>>", self.Reg_Sel_E)
        # self.mnecombo.event_generate('<Down>')

        # Initial update
        self.Reg_Update(self.addr,name)

    def Drop_Down(self,event):
        self.mnecombo.event_generate('<Down>')

    def Read_Repeat_E(self, event):
        self.Read_thread_set(self.addr-self.staddr)

    def Read_Update(self,color='black'):
        read_data=ISP_Read(self.addr,self.mode,self.slv_addr,self.AByte,self.Byte,self.LSB)
        self.readdata.configure(text=hex(read_data))
        self.readdata.configure(foreground=color)
        return  read_data

    def Write_Update(self,data):
        # I2C Write
        ISP_WriteLog(self.addr,data,mode=self.mode,slv_addr=self.slv_addr,AByte=self.AByte,Byte=self.Byte,LSB=self.LSB)
    def writedata_reload(self):
        self.writedata.delete(0,tkinter.END)
        self.writedata.insert(0,hex(self.writereg))


    def Write_Hex(self,data,write,button=0,en=0xFFFFFFFF,bits=0):
        # Hex write to writedata(spin box)
        self.writedata.delete(0,tkinter.END)
        self.writedata.insert(0,hex(data))
        data=data<<bits
        
        self.writereg=(data&en)|(self.writereg&(~en))
        if(button==1)   :   self.BitPan.Button_Ld(self.writereg)
        if(write==1)    :   self.Write_Update(self.writereg)

    def Spin_Write_Hex_E(self,event):
        data=int(self.writedata.get(),base=16)
        index=self.mnecombo['values'].index(self.mnecombo.get())
        en, bits, bit =self.Get_en(index)
        # if(data>=(1<<bit)):
        #     data=0x0
        data = data & (en>>bits)
        self.Write_Hex(data,1,1,en,bits)

    def Spin_Write_Hex(self):
        # Spin box up & down event
        data=int(self.writedata.get())
        index=self.mnecombo['values'].index(self.mnecombo.get())
        en, bits, bit =self.Get_en(index)
        # if(data>=(1<<bit)):
        #     data=(1<<bit)-1
        data = data & (en>>bits)
        self.Write_Hex(data,1,1,en,bits)

    def Add_Sel_E(self,event):
        # Reg pannel click event(addr selection)
        index=self.mnecombo['values'].index(self.mnecombo.get())
        if(index==0):
            # for j in range(0,32):
            #     self.BitPan.bitbutton[j].Button_enable()
            self.Get_en(0)

        index=self.RegPan.index(self)
        for i in range(0,16):
            if(index!=i):
                self.RegPan[(self.staddr+i)&((1<<4)-1)].Add_Out()
                self.RegPan[(self.staddr+i)&((1<<4)-1)].mnecombo.current(0)
                self.RegPan[(self.staddr+i)&((1<<4)-1)].writedata_reload()

        self.addlabel.configure(foreground='#528080')
        self.readdata.configure(foreground='#528080')
        self.mnecombo.configure(foreground='#528080')
        self.writedata.configure(background='#345050')
        self.writedata.configure(foreground='white')


        tmp,CADDR = self.addlabel.config('text')[4].split('0x')
        CADDR=int(CADDR,base=16)

        self.addr=CADDR
        self.CADDR_set(CADDR)

        self.BitPan.Button_Ld(self.writereg)

    def Add_Out(self):
        self.addlabel.configure(foreground='black')
        self.mnecombo.configure(foreground='black')
        self.readdata.configure(foreground='black')
        self.writedata.configure(background='white')
        self.writedata.configure(foreground='black')

    def Get_en_l(self,index):
        name,bit=self.mnecombo['values'][index].split('[')
        bit=bit.replace(']','')
        if (bit.find(':')>-1):
            bite,bits=bit.split(':')
            bite,bits = int(bite),int(bits)
        else:
            bite,bits=int(bit),int(bit)
        bit=bite-bits+1
        en=0
        for i in range(0,32):
            if((i>=bits) & (i<=bite)):
                en = en+(1<<i)
                self.BitPan.bitbutton[i].Button_enable(0)
            else:
                self.BitPan.bitbutton[i].Button_enable(1)
        return en, bits, bit

    def Get_en(self,index):
        if(index==0):
            en=0x0
            bits=0
            bit=32
            # for i in range(0,32):
            #     self.BitPan.bitbutton[i].Button_enable()

            n=0
            # print(len(self.mnecombo['values']))
            # # print(self.mnecombo['values'])
            for i in range(len(self.mnecombo['values'])-1):
                en_t, bits_t, bit_t = self.Get_en_l(i+1)
                en=en+en_t
            # printh(en)
            for i in range(1,33):
                # print((en%(1<<i))>>(i-1))
                if((en%(1<<i))>>(i-1)==1):
                    # en = en+(1<<i)
                    self.BitPan.bitbutton[i-1].Button_enable(0)
                else:
                    self.BitPan.bitbutton[i-1].Button_enable(1)


        else:
           en, bits, bit = self.Get_en_l(index)
        return en, bits, bit

    def Reg_Sel_E(self,event):
        index=self.mnecombo['values'].index(self.mnecombo.get())
        self.Reg_Sel(index)
        # print(index)


    def Reg_Sel(self,index,write=0):
        en, bits, bit =self.Get_en(index)
        data=(self.writereg&en)>>bits
        self.mnecombo.current(index)
        self.Write_Hex(data,write,0,en,bits)


    def Reg_Update(self,addr,name):
        self.Read_thread_off()
        self.addr=addr
        self.staddr=((self.addr>>4)<<4)
        self.addlabel.configure(text=hex(self.addr))
        if(name==''):
            names=['']
        elif(name.find(',')!=-1):
            names=name.split(',')
            names.insert(0,name)
        else:
            names=[name+' ']
            names.insert(0,name)
        self.mnecombo['values'] = names
        self.mnecombo.current(0)
        for i in range(0,32):
            self.BitPan.bitbutton[i].Button_enable(0)

class Search:
    # Register Search box(Right)
    def __init__(self,mnedata,GUI_TOP):
        # Top module variables
        self.pan=GUI_TOP.pan
        self.Read_All=GUI_TOP.Read_All
        self.RegPan=GUI_TOP.RegPan
        self.mnedata=mnedata
        # self.mode=mode

        # Widget initial
        self.SearchET=tkinter.Entry(self.pan,width=21)
        self.SearchET.bind("<Return>", self.Find_Reg_E)
        self.SearchBT=tkinter.ttk.Button(self.pan,width=5,text=("Find"), command=self.Find_Reg)
        self.SearchLIST=tkinter.Listbox(self.pan,selectmode='browse',width=28,height=24,exportselection=0)
        self.SearchLIST.bind("<<ListboxSelect>>", self.Selection_LT_E)
        self.SearchLIST.bind("<Button-3>", self.Selection_LT_DOWN)
        self.SearchLIST.insert(0,'')


    def Selection_LT_DOWN(self,event):
        index=self.SearchLIST.curselection()[0]
        if self.SearchLIST.get(index).find('::') != -1:
            self.Selection_LT(1)

    def Selection_LT_E(self,event):
        # ListboxSelect event
        index=self.SearchLIST.curselection()[0]
        if self.SearchLIST.get(index).find('::') != -1:
            self.Selection_LT()

    def Selection_LT(self,down=0):
        # ListboxSelect (event & Find)
        index=self.SearchLIST.curselection()[0]
        addr, name = self.SearchLIST.get(index).split('::')
        addr=int(addr,base=16)
        for i in range(0,16):
            addr_tmp = ((addr>>4)<<4)+i
            addrh=hex(addr_tmp)
            # names=self.mnedata[addrh.replace('0x','')]
            names=self.mnedata.get(addrh.replace('0x',''),'')
            self.RegPan[i].Reg_Update(addr_tmp,names)
        addrh=hex(addr)
        # names=self.mnedata[addrh.replace('0x','')]
        names=self.mnedata.get(addrh.replace('0x',''),'')
        names=names.split(',')
        self.Read_All(self.RegPan)
        if(name==''):
            self.RegPan[addr&((1<<4)-1)].Reg_Sel(0)
        else:
            self.RegPan[addr&((1<<4)-1)].Reg_Sel(names.index(name)+1)
        if(down==1):
            self.RegPan[addr&((1<<4)-1)].mnecombo.focus_set()
            self.RegPan[addr&((1<<4)-1)].mnecombo.event_generate('<Down>')
        else:
            self.RegPan[addr&((1<<4)-1)].writedata.focus_set()


    def Find_Reg_E(self,event):
        # Find enter event
        self.Find_Reg()

    def Find_Reg(self):
        # Register Find
        TXT=self.SearchET.get()
        ADSerch=1
        try:
            int(TXT,base=16)
        except:
            ADSerch=0

        if TXT!='':
            c=0
            mnes=list(self.mnedata.items())
            # print(mnes)
            self.SearchLIST.delete(0,tkinter.END)
            if(ADSerch==1):
                addr=TXT
                # print(addr)

                self.SearchLIST.insert(c,addr+'::')
                c=c+1
            #Register name upper case only
            TXT=TXT.upper()

            for i in mnes:
                if (i[1].find(TXT)!=-1):
                    names=i[1].split(',')
                    addr=i[0]
                    for j in names:
                        if (j.find(TXT)!=-1):
                            # print(j)
                            self.SearchLIST.insert(c,addr+'::'+j)
                            c=c+1
            if(c!=0):
                self.SearchLIST.selection_set(0)
                self.Selection_LT()

class GUI_TOP:
    def __init__(self,mne,staddr,q,mode='IIC',slv_addr=0x6E,Title='ISP',AByte=2,Byte=4,LSB=1):
        self.pan = tkinter.Tk()
        self.pan.title(' - '.join(['Register Control Panel',Title]))
        self.RegPan=[]
        self.CADDR = 0
        self.Read_thread=None
        self.Read_thread_index=None
        self.Read_thread_flag=0
        self.mode=mode
        self.q=q
        self.slv_addr=slv_addr
        self.Byte=Byte
        self.AByte=AByte
        self.LSB=LSB
        # print('GUI Top')

        # Top 32bit button
        self.BitPan=bitBT(self)

        # Register address name & Read/data area
        i=0
        mnedata={}
        for line in mne:
            addr, name=line.split('\t')
            # name, tmp = name.split('\n')
            name.rstrip()
            if(name!=''):
                # print(name)
                mnedata[addr.lower()]=name
        # printh((int(sorted(mnedata)[0],base=16)))
        for dict in mnedata:
            if(staddr == 0):
                if((int(dict,base=16)>>4)==(int(sorted(mnedata)[0],base=16)>>4)):
                    self.RegPan.append(RegPannel(int(dict,base=16),mnedata[dict],self))
                    self.RegPan[i].addlabel.place(x=0,y=40+i*23)
                    self.RegPan[i].mnecombo.place(x=45,y=40+i*23)
                    self.RegPan[i].readdata.place(x=602,y=40+i*23)
                    self.RegPan[i].writedata.place(x=685,y=40+i*23)
                    i=i+1
                    addr=int(dict,base=16)
                    # print(addr)
            else:
                if((int(dict,base=16)>>4)==(staddr>>4)):
                    self.RegPan.append(RegPannel(int(dict,base=16),mnedata[dict],self))
                    self.RegPan[i].addlabel.place(x=0,y=40+i*23)
                    self.RegPan[i].mnecombo.place(x=45,y=40+i*23)
                    self.RegPan[i].readdata.place(x=602,y=40+i*23)
                    self.RegPan[i].writedata.place(x=685,y=40+i*23)
                    i=i+1
                addr=staddr
                    # print(dict,i)
            # print(dict)
        # print(mnedata)
        # addr = sorted(mnedata)[0]
        j=0
        for j in range(i,16):
            self.RegPan.append(RegPannel(((addr//16)*16)+j,'',self))
            self.RegPan[j].addlabel.place(x=0,y=40+j*23)
            self.RegPan[j].mnecombo.place(x=45,y=40+j*23)
            self.RegPan[j].readdata.place(x=602,y=40+j*23)
            self.RegPan[j].writedata.place(x=685,y=40+j*23)

        # print(j)
        # print(mnedata['7070'],hex(staddr))
        # Register read (initialization)
        self.Read_All_BT(self.RegPan,self.mode)

        # Read All button
        Read=tkinter.ttk.Button(self.pan, width=7,text=("Read All"),command=lambda : self.Read_All_BT(self.RegPan,mode))
        Read.place(x=600,y=0)

        # Write All button
        Write=tkinter.ttk.Button(self.pan, width=7,text=("Write All"),command=lambda : self.Write_All(self.RegPan))
        Write.place(x=658,y=0)

        # arrow
        left=tkinter.ttk.Button(self.pan, width=3,text=("<"),command=lambda : self.Left_page(self.RegPan,mnedata))
        left.place(x=716,y=0)
        right=tkinter.ttk.Button(self.pan, width=3,text=(">"),command=lambda : self.Right_page(self.RegPan,mnedata))
        right.place(x=746,y=0)

        # Register Search box(Right)
        self.SerchBox=Search(mnedata,self)
        self.SerchBox.SearchET.place(x=780,y=0)
        self.SerchBox.SearchBT.place(x=933,y=0)
        self.SerchBox.SearchLIST.place(x=780,y=23)
        self.pan.bind("<Escape>", self.Closewindow)
        self.pan.bind("<F5>", self.Newwindow)
        self.pan.bind("<Control-f>", self.Search)
        self.pan.bind("<Control-F>", self.Search)

    def Search(self,event):
        self.SerchBox.SearchET.focus_set()
        self.SerchBox.SearchET.select_range(0,tkinter.END)
        

    def Closewindow(self,event):
        self.q.put('exit')
        
    def Newwindow(self,event):
        # print("press F5")
        # lock.acquire()
        self.q.put(self.RegPan[0].staddr)
        # lock.release()

    def Read_All_BT(self,RegPan,mode):
        ISP_Init(mode)
        # sleep(0.1)
        self.Read_All(RegPan)

    def Read_All(self,RegPan):
        # Read register(staddr ~ staddr+15)
        for i in range(0,16):
            if(i==(self.CADDR&0xF)):
                data=RegPan[i].Read_Update()
                RegPan[i].Write_Hex(data,0,button=1)
            else:
                data=RegPan[i].Read_Update()
                RegPan[i].Write_Hex(data,0)
            RegPan[i].mnecombo.current(0)
        # self.RegPan[0].mnecombo.event_generate('<Down>')

    def Write_All(self,RegPan):
        # Write register(staddr ~ staddr+15)
        # ISP_Init()
        staddr=RegPan[0].staddr
        for i in range(0,16):
            addr=i+staddr
            data=int(RegPan[i].writedata.get(),base=16)
            ISP_WriteLog(addr,data,mode=self.mode,slv_addr=self.slv_addr,AByte=self.AByte,Byte=self.Byte,LSB=self.LSB)
            # que.put(ISP_WriteLog(addr,data))

    def Left_page(self,RegPan,mnedata):
        caddr=RegPan[0].addr
        if(caddr>0xf):
            naddr=caddr-0x10
            self.CADDR=self.CADDR-0x10
            for i in range(0,16):
                addr_tmp = naddr+i
                addrh=hex(addr_tmp)
                # names=mnedata[addrh.replace('0x','')]
                names=mnedata.get(addrh.replace('0x',''),'')
                self.RegPan[i].Reg_Update(addr_tmp,names)
            self.Read_All(self.RegPan)

    def Right_page(self,RegPan,mnedata):
        caddr=RegPan[0].addr
        naddr=caddr+0x10
        self.CADDR=self.CADDR+0x10
        for i in range(0,16):
            addr_tmp = naddr+i
            addrh=hex(addr_tmp)
            # names=mnedata[addrh.replace('0x','')]
            names=mnedata.get(addrh.replace('0x',''),'')
            self.RegPan[i].Reg_Update(addr_tmp,names)
        self.Read_All(self.RegPan)

    def Read_Repeat(self):
        # printh(self.RegPan[self.Read_thread_index].addr)
        for i in range(0,1<<10):
        # while(self.Read_thread_flag==0):
            sleep(0.05)
            if(self.Read_thread_flag==1):
            # if(flag.is_set()):
                # print('Read interrupted')
                # ret()
                self.Read_thread_flag = 0
                self.Read_thread_index = None
                return
            else:
                self.RegPan[self.Read_thread_index].Read_Update('red')
        self.RegPan[self.Read_thread_index].Read_Update('black')

    def Read_thread_off(self):
        if (self.Read_thread!=None and self.Read_thread.is_alive()) :
            self.RegPan[self.Read_thread_index].Read_Update('black')
            self.Read_thread_flag = 1

    def Read_thread_set(self, index):
        # print(index)
        # print(self.Read_thread_index)
        # event=threading.Event()
        if (self.Read_thread!=None and self.Read_thread.is_alive()) :
            self.RegPan[self.Read_thread_index].Read_Update('black')
            if(self.Read_thread_index!=index):
                # print('index!=index',self.Read_thread_index,index)
                self.Read_thread_index=index
            else:
                # print('index==index',self.Read_thread_index,index)
                self.Read_thread_flag = 1
        else:
            # print('First repeat',self.Read_thread_index,index)
            self.Read_thread_index=index
            self.Read_thread=threading.Thread(target=self.Read_Repeat,daemon=True)
            self.Read_thread.start()

    def CADDR_get(self):
        # Current activated address load
        return self.CADDR

    def CADDR_set(self,data):
        # Current activated address Update
        self.CADDR=data

    def CallGUI(self):
        # Main loop
        self.pan.geometry('980x'+str(16*23+40))
        # print('GUI Start')
        self.pan.mainloop()




def RegControl(mne,q,staddr=0,mode='IIC',slv_addr=0x6E,Title='ISP',AByte=2,Byte=4,LSB=1):

    # ISP_Init(mode)
    # print('RegControl')
    Reg_Pannel=GUI_TOP(mne,staddr,q,mode,slv_addr,Title,AByte,Byte,LSB)
    Reg_Pannel.CallGUI()



    # ISP_deInit(mode)

def New_window(mne,n,q,pan,mode,slv_addr=0x6E,Title='ISP',AByte=2,Byte=4,LSB=1):

    while True:
        # lock.acquire()
        sleep(0.1)
        if(not q.empty()):
            qdata = q.get()
            if(qdata=='exit'):
                for i in range(0,n):
                    pan[i].destory()
            else :
                n=n+1
                pan.append(threading.Thread(target=RegControl, args=(mne,q,qdata,mode,slv_addr,Title,AByte,Byte,LSB,), daemon=True))
                pan[n].start()
        # lock.release()

def Top_Window(mode,mne_dir,slv_addr=0x6E,Title='ISP',AByte=2,Byte=4,LSB=1):
    q=queue.Queue(3)


    f=open('RegControl.log','w')
    f.close()
    mnefile=open(mne_dir,'r')
    mne=mnefile.readlines()
    mnefile.close()

    pan=[]
    i=0
    # RegControl(mne,0x0,mode)
    pan.append(threading.Thread(target=RegControl, args=(mne,q,0x0,mode,slv_addr,Title,AByte,Byte,LSB,)))
    pan[i].start()
    

    tsk=threading.Thread(target=New_window,args=(mne,i,q,pan,mode,slv_addr,Title,AByte,Byte,LSB,),daemon=True)
    tsk.start()
    # pan[0].join()


if __name__ == '__main__':
    mode='IIC'

    # mnefile=open('ISP.mne','r')
    # mne=mnefile.readlines()
    # mnefile.close()


    print(sys.path[0].replace('\\','/'))

    ISP_Init(mode)
    Top_Window(mode,'../Rtl/Top/ISP.mne')
    # q=queue.Queue(3)

    # pan=[]
    # i=0
    # # RegControl(mne,0x0,mode)
    # pan.append(threading.Thread(target=RegControl, args=(mne,0x7070,mode,)))
    # pan[i].start()


    # tsk=threading.Thread(target=New_window,args=(mode,i,),daemon=True)
    # tsk.start()


    # print('test')
    # pan[0].join()


    ISP_deInit(mode)
