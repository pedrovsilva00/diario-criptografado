import hashlib
import datetime
import cryptocode
import PySimpleGUI as gui


class texto ():
    def criar(self,cc): # criar arquivo com md5 na data
        try:
            cata = (str(cc) + '.txt')
            self.arq = open (cata,'w')
            #print ('Arquivo ',cata,' criado com sucesso')
        except Exception as e:
            m = "Erro " + e 
            gui.popup_ok(e,title= 'Erro',font='Arial 14',button_color=('white','#1C1C1C' ))
    def ler(self,cc): # ler arquivo
        try:
            cata = (str(cc) + '.txt')
            self.arq = open(cata, "r+")
            leitura = self.arq.readline()
        except Exception as e:
            leitura = ''
        return leitura

    def fechar(self):
        self.arq.close()
        #return print('Arquivo fechado com sucesso')

    def encripto (txt,ha):
        msg_encry = cryptocode.encrypt(txt,ha)
        return msg_encry
    def desencry (txt,ha):
        msg = list([])
        for msg in txt:
            m = cryptocode.decrypt(txt,ha)
            msg = m + msg
        return msg
    def dia ():
        dat = datetime.date.today()
        new_d = format(dat, "%d-%m-%Y")
        print (new_d)
        hh = hashlib.md5(new_d.encode())
        didi = hh.hexdigest()
        return didi

class janela(texto):
    def __init__ (self):
        gui.theme('DarkGrey1')
        sen = gui.popup_get_text('Senha de Acesso: ',password_char='*',font='Arial 14',button_color=('white','#1C1C1C' ),size=(14,20))
        self.k ='5ec713ba26c0b1afb766143ed3fa4beab0d56dc8863c7817a46f911257e764de0311fbef58e5b23fde281432bb422de4da3a808e92221488196cd4959822a0a1'
        if sen != '':
            hm = hashlib.sha512(sen.encode())
            hashs = hm.hexdigest()
            if hashs == self.k:
                self.xxx = True
                janela.window(self)
            else:
                gui.popup_ok('Senha Incorreta',title= 'Erro',font='Arial 14',button_color=('white','#1C1C1C' ))
                self.xxx = False

    def window(self):
        gui.theme('DarkGrey1')
        fontex='Arial 15 '
        fontb ='Arial 12 '
        lay1 = [    [gui.Text('Querido diario...',font=fontex)],
                    [gui.Multiline('',font=fontb,key='texto', no_scrollbar=True,size=(100,28) )],
                    [gui.Button('Procurar por dia',font=fontex,button_color=('white','#1C1C1C' ),key='procurab',auto_size_button=True,expand_x=True),gui.Button('Finalizar',font=fontex,button_color=('white','#1C1C1C' ),key='fim',auto_size_button=True,expand_x=True)]
                ]
        win= gui.Window('Diario', lay1 ,finalize=True,size=(350,600))
        while self.xxx == True:
            event,values =win.read()
            if  event == gui.WIN_CLOSED:
                self.xxx = False
                break
            elif event == 'procurab': # botao p/ procurar
                janela.win_procu(self)
            elif event == 'fim':
                d = texto.dia()
                if values['texto'] == '':
                    gui.popup_ok('Falta texto',title= 'Erro',font='Arial 14',button_color=('white','#1C1C1C' ))
                    self.xxx = True
                else: 
                    tt = values['texto']
                    temp = texto.encripto(tt,self.k)
                    texto.criar(self,d)
                    self.arq.write(temp)
                    texto.fechar(self)
                    self.xxx = False
                    break
    def win_procu(self):
        gui.theme('DarkGrey1')
        fontt='Arial 14 '
        fontx = 'Arial 13'
        lay2= [     [gui.Text('Dia',justification='left',s=3,font=fontt,expand_x=True),gui.Text('Mês',justification='center',s=3,font=fontt,expand_x=True),gui.Text('Ano',justification='right',s=3,font=fontt,expand_x=True)],
                    [gui.InputText('',justification='left',s=4,font=fontx,k='tdia',expand_x=True),gui.InputText('',justification='center',s=4,font=fontx,k='tmes',expand_x=True),gui.InputText('',justification='right',s=4,font=fontx,k='tano',expand_x=True)],
                    [gui.Button('Procurar',auto_size_button=True,font=fontt,k='bprocu',button_color=('white','#1C1C1C' ),expand_x=True)]

        ]
        win2 = gui.Window('Procura por Dia',lay2)
        while self.xxx == True:
            event,values =win2.read()
            if event == gui.WIN_CLOSED:
                self.xxx = False
                break
            elif event == 'bprocu' and values['tdia'] != '' and values['tmes'] != '' and values['tano'] != '':
                sen = gui.popup_get_text('Senha Desbloqueio ',password_char='*',font='Arial 14',button_color=('white','#1C1C1C' ),size=(15,20))
                if sen != '':
                    hm = hashlib.sha512(sen.encode())
                    hashs = hm.hexdigest()
                    if hashs == self.k:
                        self.xxx = True
                        diap = values['tdia'] + '-' + values['tmes'] + '-' + values['tano']
                        hd = hashlib.md5(diap.encode())
                        haxi = hd.hexdigest()
                        temp = texto.ler(self,haxi)
                        if temp == '':
                            gui.popup_ok('Arquivo não encontrado',title= 'Erro',font='Arial 14',button_color=('white','#1C1C1C' ))
                            janela.window(self)
                        else:
                            msg = texto.desencry(temp,hashs)
                            janela.mostra_txt(self,diap,msg)
                    else: 
                        gui.popup_ok('Algo de errado não está certo',title= 'Erro',font='Arial 14',button_color=('white','#1C1C1C' ))
                        self.xxx = False
    def mostra_txt(self,dd,mm):
        gui.theme('DarkGrey1')
        fontt='Arial 12 '
        fontx = 'Arial 13'
        temp = ('Texto desencriptografado da data: '+ dd) 
        lay3 = [    [gui.Text(text=temp,font=fontt)],
                    [gui.Multiline(default_text=mm,s=50,font=fontx, k='tlimpo',no_scrollbar=True,size=(100,27))],
                    [gui.Button('Sair',auto_size_button=True,font=fontt,k='sair',button_color=('white','#1C1C1C' ),expand_x=True)]

        ]
        win3 = gui.Window('Diario decifrado',lay3,size=(375,600))
        while self.xxx == True:
            event,values =win3.read()
            if event == gui.WIN_CLOSED or event == 'sair':
                self.xxx = False
                texto.fechar(self)
                break
if __name__ == "__main__":

    inicio  = janela()
